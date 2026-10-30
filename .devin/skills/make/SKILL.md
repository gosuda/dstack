---
name: make
description: 'Use when writing or debugging Makefiles, understanding pattern rules and automatic dependency generation, managing CFLAGS/LDFLAGS, or diagnosing incremental build, phony targets, or recursive make.'
---

# GNU Make

Idiomatic Makefile patterns for C/C++ projects: phony targets, pattern rules, automatic dependency generation, and incremental build hygiene. Grounded against GNU Make 4.4.1.

Tell me the source layout (where `.c`/`.cpp` files and headers live). Name the compiler and flags (`CC`, `CFLAGS`, `LDFLAGS`, `LDLIBS`) when they cannot be inferred, and any build variants or install prefix. Everything here stays local: the skill writes `Makefile`/`*.mk` files and local build outputs, and rollback is version control plus `make clean`.

## Write a minimal correct Makefile

Recipes start with a tab, never spaces. `make` should build and `make clean` should remove outputs.

```makefile
CC      := gcc
CFLAGS  := -std=c23 -Wall -Wextra -g -O2
LDFLAGS :=
LDLIBS  :=

SRCS    := $(wildcard src/*.c)
OBJS    := $(SRCS:src/%.c=build/%.o)
TARGET  := build/prog

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

build/%.o: src/%.c | build
	$(CC) $(CFLAGS) -c -o $@ $<

build:
	mkdir -p build

clean:
	rm -rf build
```

Automatic variables used above: `$@` is the target, `$<` the first prerequisite, `$^` all prerequisites deduplicated, `$*` the pattern stem, `$(@D)` the target directory part.

## Track header dependencies automatically

Without dependency files, editing a header rebuilds nothing. `-MMD` writes a `.d` file per object. `-MP` adds phony targets for headers so deleting one does not break the build.

```makefile
DEPFLAGS = -MMD -MP
DEPS    := $(OBJS:.o=.d)

build/%.o: src/%.c | build
	$(CC) $(CFLAGS) $(DEPFLAGS) -MF $(@:.o=.d) -c -o $@ $<

-include $(DEPS)   # leading - ignores missing .d files on first build
```

Touch a header and confirm exactly its dependents rebuild.

## Cover repeated transforms with pattern rules

```makefile
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

%.s: %.c
	$(CC) $(CFLAGS) -S -o $@ $<
```

One rule should cover each source to output shape.

## Split debug and release builds

```makefile
BUILD ?= release
ifeq ($(BUILD),debug)
  CFLAGS += -g -Og -DDEBUG
else
  CFLAGS += -O2 -DNDEBUG
endif

Q := $(if $(V),,@)
build/%.o: src/%.c | build
	@echo "  CC  $<"
	$(Q)$(CC) $(CFLAGS) -c -o $@ $<
```

`make BUILD=debug` should switch flags and `make V=1` should show full commands.

## Stage installs with prefix variables

```makefile
PREFIX ?= /usr/local

install: $(TARGET)
	install -d $(DESTDIR)$(PREFIX)/bin
	install -m 0755 $(TARGET) $(DESTDIR)$(PREFIX)/bin/
```

`make install DESTDIR=/tmp/stage` should stage the tree.

## Include fragments instead of recursing

Recursive make fragments the dependency graph and breaks parallelism. One top level Makefile should see every prerequisite.

```makefile
# Makefile
include lib/module.mk
include src/app.mk
```

```makefile
# lib/module.mk
LIB_SRCS := $(wildcard lib/*.c)
LIB_OBJS := $(LIB_SRCS:lib/%.c=build/lib_%.o)
OBJS     += $(LIB_OBJS)

build/lib_%.o: lib/%.c
	$(CC) $(CFLAGS) -c -o $@ $<
```

A tree already using `$(MAKE) -C` converts by including the child `.mk` files from the top Makefile.

## Diagnose failures against the table

| Error | Cause | Fix |
|---|---|---|
| `No rule to make target 'foo.o'` | Missing source or rule | Check the source path and pattern rule |
| `Nothing to be done for 'all'` | Targets up to date | Touch a source or run `make clean` |
| `Circular dependency dropped` | Target depends on itself | Trace the prerequisite chain |
| `missing separator` | Spaces where a tab belongs | Recipes need a literal tab |
| `multiple target patterns` | Bad pattern rule syntax | Check `%` placement |
| Rebuilds everything | Wrong timestamps or missing `.PHONY` | Check `date`; mark `all` and `clean` phony |
| Header edit rebuilds nothing | No dependency tracking | Add `-MMD -MP` and `-include $(DEPS)` |

Useful flags: `make -j"$(nproc)"` for parallel builds, `make -O` to synchronize output, `make -n` for a dry run, `make -B` to force rebuild, `make -k` to keep going, `make -p` to print the rule database, `make --warn-undefined-variables` to catch typos. The full variable, function, and special target reference lives in `references/cheatsheet.md`.

Parallel build races come from a missing order only prerequisite or an undeclared generated header. Declare the real dependency and never serialize to hide it. A variable expanding empty is usually `=` against `:=`: `=` defers expansion to use time while `:=` expands at definition, so pick `:=` unless late expansion is the point. `::=` is the POSIX immediate form, available in GNU Make 4.4 and later.

Hand back a Makefile that builds incrementally, tracks header dependencies, supports `clean` and `install`, and survives `make -j`. A second run should report nothing to do. For debugging tasks, hand back the diagnosed cause and the minimal fix.
