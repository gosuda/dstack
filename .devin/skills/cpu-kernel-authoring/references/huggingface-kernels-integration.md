# Hugging Face kernels integration (CPU)

How to load and publish CPU kernels with the Hugging Face kernels library.

The [Hugging Face kernels](https://huggingface.co/docs/kernels/en/index) library loads pre-compiled kernels from the Hugging Face Hub at run time. CPU kernels are compiled with `kernel-builder` and distributed as platform-specific wheels.

What the library gives a CPU kernel:

- No local compilation: the user downloads a built wheel.
- Version pinning: `get_kernel` loads a named revision.
- One API for CUDA, XPU, and CPU kernels.
- The wheel is matched to the user's PyTorch build.

## Install the loader

```bash
pip install kernels torch
```

## Load a kernel by repo and version

```python
from kernels import get_kernel

kernel = get_kernel("kernels-community/rmsnorm", version=1)
```

## Check availability before loading

```python
from kernels import has_kernel

if has_kernel("kernels-community/rmsnorm", version=1):
    kernel = get_kernel("kernels-community/rmsnorm", version=1)
```

## Load from a local checkout while developing

```python
from pathlib import Path
from kernels import get_local_kernel

# Load from local build (requires Path object and package name)
kernel = get_local_kernel(Path("/path/to/my-kernel"), "my_kernel")
```

## Run RMSNorm on CPU

```python
import torch
from kernels import get_kernel, has_kernel

repo_id = "kernels-community/rmsnorm"

if has_kernel(repo_id, version=1):
    rmsnorm_kernel = get_kernel(repo_id, version=1)

    x = torch.randn(2, 1024, 2048, dtype=torch.bfloat16)  # CPU tensor
    weight = torch.ones(2048, dtype=torch.bfloat16)

    # CPU dispatch happens automatically via torch_binding.cpp
    out = rmsnorm_kernel.apply_rms_norm_forward(x, weight, eps=1e-6)
```

## Patch a Transformers model to use the kernel

```python
import torch
from kernels import get_kernel, has_kernel

repo_id = "kernels-community/rmsnorm"

if has_kernel(repo_id, version=1):
    rmsnorm_kernel = get_kernel(repo_id, version=1)

    def patch_rmsnorm(model):
        """Patch model's RMSNorm to use CPU kernel."""
        patched = 0
        for name, module in model.named_modules():
            if 'RMSNorm' in type(module).__name__:
                eps = getattr(module, 'variance_epsilon', None) or getattr(module, 'eps', 1e-6)

                def make_forward(mod, epsilon):
                    def forward(hidden_states):
                        return rmsnorm_kernel.apply_rms_norm_forward(hidden_states, mod.weight, eps=epsilon)
                    return forward

                module.forward = make_forward(module, eps)
                patched += 1
        return patched
```

## Ship a CPU kernel

Build the wheel, try it locally, then publish the source so the Hub CI can build per-backend wheels.

Build with kernel-builder:

```bash
cd my-kernel/
kernel-builder build --release
# Produces dist/my_kernel-*.whl
```

Try the wheel locally:

```bash
pip install dist/*.whl --force-reinstall
python -c "from pathlib import Path; from kernels import get_local_kernel; k = get_local_kernel(Path('.'), 'my_kernel'); print(dir(k))"
```

Create the Hub repository:

```bash
# Create repo on huggingface.co/kernels-community/
# Upload the kernel source and build.toml
```

One kernel repo can serve CUDA, XPU, and CPU. The `build.toml` defines all backends:

```toml
# CUDA sections
[kernel.my_kernel_cuda]
backend = "cuda"
# ...

# CPU sections
[kernel.my_kernel_cpu]
backend = "cpu"
# ...
```

The kernel-builder CI builds wheels for each backend. `get_kernel()` automatically selects the right wheel for the user's hardware.

## What the Hub repo contains

```
my-kernel/
├── build.toml              # Multi-target build config
├── torch-ext/
│   └── torch_binding.cpp   # Op registration (registration.h)
├── my_kernel_cpu/           # CPU implementation
│   ├── cpu_features.hpp
│   ├── my_kernel_cpu.cpp
│   ├── my_kernel_cpu.hpp
│   ├── my_kernel_cpu_torch.cpp
│   ├── my_kernel_avx512.cpp
│   └── my_kernel_avx512.hpp
├── csrc/                    # CUDA implementation (if any)
│   └── ...
└── README.md
```

## Dispatch and platform facts worth remembering

- CPU kernels use the same `torch_binding.cpp` and `registration.h` pattern as CUDA/XPU kernels
- The `ops.impl("forward", torch::kCPU, &func)` call ensures CPU dispatch (element-wise kernels such as rmsnorm instead register with `c10::DispatchKey::CompositeExplicitAutograd`)
- Multi-device kernels use `#if defined(CPU_KERNEL)` / `#elif defined(CUDA_KERNEL)` guards
- CPU wheels are built for x86_64 Linux; ARM/macOS may require source builds
