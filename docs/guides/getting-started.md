# Getting Started
## Clone
```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
# fetch one category only (recommended, the full set is many GB)
git submodule update --init --depth 1 stacks/gateways-routing
# or everything
git submodule update --init --depth 1 --recursive
```
## Update all stacks
```bash
git submodule update --remote --depth 1
```
Next: [Build a full local stack](full-stack.md).
