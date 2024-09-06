# Autonomy Dev

Tooling to speed up autonomy development.

## Usage

### Contracts

We can scaffold a new contract using the `adev scaffold contract` command. This will create a new directory with;
- open-aea contract component
    - open-aea contract component class 🎉
    - open-aea contract component function generation 🚧
    - open-aea contract component test generation 🚧


```bash
adev scaffold contract 0xc939df369C0Fc240C975A6dEEEE77d87bCFaC259 beyond_pricer \
      --block-explorer-api-key $BLOCK_EXPLORER_API_KEY \
      --block-explorer-url "https://api-goerli.arbiscan.io"
```


## Installation

```bash
pip install autonomy-dev[all]
```
## Release

```bash
checkout main
git pull
adev release
```


# Project Status Badges
[![Code Quality](https://github.com/8ball030/auto_dev/actions/workflows/common_check.yaml/badge.svg)](https://github.com/8ball030/auto_dev/actions/workflows/common_check.yaml)
