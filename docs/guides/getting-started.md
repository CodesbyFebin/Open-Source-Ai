# Getting Started

## Clone

```bash
git clone https://github.com/CodesbyFebin/Open-Source-Ai
cd Open-Source-Ai
# fetch one category only (recommended; the full set is many GB)
git submodule update --init --depth 1 stacks/code-review
# or everything
git submodule update --init --depth 1
```

## Update pinned stacks to the latest upstream

```bash
git submodule update --init --remote --depth 1 stacks/<category>
```

Next: [Run a full local stack](full-stack.md).
