# Moni-Iti Wordchain

Moni-Iti is an experimental open-source cryptocurrency where **words have value**.
Each transaction stores a word on a tiny blockchain. The numeric value of a word
is the sum of the alphabetical positions of its letters (`a=1`, `b=2`, ...).
Blocks are linked using a proof-of-work scheme and nodes can share their chains
for cooperative storage and retrieval.

This repository contains a reference implementation written in Python.

## Features

- Word value is calculated deterministically.
- REST API for submitting words and mining blocks.
- Simple peer-to-peer node registration and conflict resolution.
- Demonstration tests.

## Installation

Create a Python environment using [conda](https://docs.conda.io/):

```bash
conda env create -f environment.yml
conda activate wordchain
```

## Usage

Run a node:

```bash
python -m wordchain.node
```

Submit a word transaction:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"word": "hello", "sender": "alice", "recipient": "bob"}' \
     http://localhost:5000/transactions/new
```

Mine a block to store pending transactions:

```bash
curl http://localhost:5000/mine
```

Retrieve the full chain:

```bash
curl http://localhost:5000/chain
```

## Testing

After activating the environment, run tests with:

```bash
pytest
```

## License

This project is released under the terms of the MIT license. See `LICENSE` for details.
