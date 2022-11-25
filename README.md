# Goat
`goat` is the C/C++ toolchain you deserve, and the one you need right now.\
The idea is inherited from Rust's `cargo`, but has it's own style within that original idea.

`goat` has three main targets:
- Compilation
- Package managment
- Testing

Our goal, and also where we differ from other all-in-one solution attempts you may find online, is to not build our own utilities for the different targets.\
In order to do that, we use conan for package managment gtest for testing.

The bottom line - we are perfectly usable from day zero, no popularity needed!

# Usage Example

```bash
# Create a new project
> goat create PROJECT_NAME
> cd PROJECT_NAME

# Build commands
> goat build # the same as --release
> goat build --debug
> goat build --test

# Run commands
> goat run
> goat test

# Clean objectfiles & binaries
> goat clean
```