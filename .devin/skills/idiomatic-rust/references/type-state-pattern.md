# Type state pattern

The type-state pattern models system states as distinct types at compile time. By representing states through types and consuming values during transitions, illegal operations become compilation errors rather than runtime exceptions.

Operations are implemented only on the state types where they are valid: builders cannot produce outputs before mandatory fields are populated, and finished states cannot repeat initialization.

## Invariant enforcement and runtime cost

Encoding state transitions into the type system provides distinct structural advantages:

* Elimination of runtime checks: Methods valid only in a specific state do not require defensive conditional checks or `Option` unwrapping.
* API discovery: Autocomplete and compiler diagnostics show only the operations relevant to the current lifecycle phase.
* Zero storage overhead for markers: Zero-sized types (ZSTs) used as state markers take up zero bytes of memory (`size_of::<State>() == 0`), adding no overhead to data layouts.
* Runtime operations still execute: While zero-sized markers require no storage, state transitions that perform I/O, validation, or resource transformation execute normal runtime logic. Real network states require validated protocol outcomes (such as verified handshakes or parsed protocol frames), not a marker cast.
* Transition ownership: Transition methods consume `self` by value and return the subsequent state type, preventing use-after-transition and stale state retention.

## Lifecycle transitions and standard library types

Standard library types often already enforce lifecycle invariants through RAII. For example, `std::fs::File` already represents an open file handle; it is obtained through fallible operations (`File::open`, `File::create`) and automatically released on drop. Wrapping `File` solely to demonstrate `Closed` and `Open` type states adds boilerplate without enforcing any distinct invariant that the standard library does not already guarantee.

Adopt the typestate pattern only when domain invariants require tracking distinct lifecycle states or resource acquisitions that existing types do not enforce.

### Fallible transition ownership

When a state transition can fail, consuming `self` by value means that a signature returning `Result<NextState, Error>` consumes the current state. If the caller needs to inspect the failure, retry the operation, or safely recover the resource, return the original state in the error variant:

```rust
pub struct UnconnectedSocket {
    address: std::net::SocketAddr,
}

pub struct ConnectedSocket {
    stream: std::net::TcpStream,
}

impl UnconnectedSocket {
    pub fn new(address: std::net::SocketAddr) -> Self {
        Self { address }
    }

    pub fn connect(self) -> Result<ConnectedSocket, (Self, std::io::Error)> {
        match std::net::TcpStream::connect(self.address) {
            Ok(stream) => Ok(ConnectedSocket { stream }),
            Err(err) => Err((self, err)),
        }
    }
}
```

Returning `(Self, std::io::Error)` preserves transition ownership on failure, allowing the caller to retain the socket configuration without recreating it.

## Multi-parameter state builders

When constructing objects with multiple mandatory fields, the type-state pattern ensures every required property is provided before construction completes, regardless of the order in which setters are called.

```rust
pub struct MissingHost;
pub struct HostSet(String);

pub struct MissingPort;
pub struct PortSet(u16);

pub struct ServerConfig {
    pub host: String,
    pub port: u16,
    pub max_connections: usize,
}

pub struct ServerConfigBuilder<H, P> {
    host_state: H,
    port_state: P,
    max_connections: usize,
}

impl ServerConfigBuilder<MissingHost, MissingPort> {
    pub fn new() -> Self {
        Self {
            host_state: MissingHost,
            port_state: MissingPort,
            max_connections: 1024,
        }
    }
}

impl<H, P> ServerConfigBuilder<H, P> {
    pub fn max_connections(mut self, max: usize) -> Self {
        self.max_connections = max;
        self
    }
}

impl<P> ServerConfigBuilder<MissingHost, P> {
    pub fn host(self, host: impl Into<String>) -> ServerConfigBuilder<HostSet, P> {
        ServerConfigBuilder {
            host_state: HostSet(host.into()),
            port_state: self.port_state,
            max_connections: self.max_connections,
        }
    }
}

impl<H> ServerConfigBuilder<H, MissingPort> {
    pub fn port(self, port: u16) -> ServerConfigBuilder<H, PortSet> {
        ServerConfigBuilder {
            host_state: self.host_state,
            port_state: PortSet(port),
            max_connections: self.max_connections,
        }
    }
}

impl ServerConfigBuilder<HostSet, PortSet> {
    pub fn build(self) -> ServerConfig {
        ServerConfig {
            host: self.host_state.0,
            port: self.port_state.0,
            max_connections: self.max_connections,
        }
    }
}
```

Callers can provide required fields in any sequence:

```rust
let config = ServerConfigBuilder::new()
    .host("localhost")
    .port(8080)
    .max_connections(500)
    .build();

let config = ServerConfigBuilder::new()
    .port(443)
    .host("example.com")
    .build();
```

Omitting `host` or `port` leaves the builder in an incomplete type state where `.build()` does not exist. Attempting to build an incomplete configuration results in a compile-time failure. Each setter consumes `self` by value, preventing reuse or mutation of intermediate builder states. Per-state resources (`HostSet` and `PortSet`) hold populated data, while `MissingHost` and `MissingPort` require zero storage.

## Practical trade-offs and guidelines

### When to adopt type states

* Enforcing sequential order where calling operations out of order causes data corruption or logic errors.
* Mandatory builder parameters where multiple required fields must be supplied before instantiation.
* Linear resource management where operations are invalid after transition.

### When to avoid type states

* Runtime-dependent transitions: When transitions are determined by external runtime data (such as network packet types handled in an event loop), an `enum` matched at runtime provides greater clarity and flexibility.
* Standard library coverage: When standard types (such as `std::fs::File`) already model resource acquisition and release via RAII.
* Combinatorial state growth: When independent state axes multiply, type parameter counts become unwieldy.
* Heterogeneous collections: Storing multiple instances in collections requires dynamic dispatch or enum wrapping, which counteracts compile-time state specificity.

For balancing compile-time specialization against runtime flexibility, see [Generics, static dispatch, and dynamic dispatch](./generics-and-dispatch.md).
