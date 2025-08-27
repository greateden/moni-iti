"""Core blockchain implementation for storing word transactions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from time import time
from typing import List, Optional, Set
from urllib.parse import urlparse

import requests

from .utils import word_value


@dataclass
class Block:
    index: int
    timestamp: float
    transactions: List[dict]
    proof: int
    previous_hash: str


class Blockchain:
    """Simple blockchain to track words and their numeric values."""

    def __init__(self) -> None:
        self.current_transactions: List[dict] = []
        self.chain: List[Block] = []
        self.nodes: Set[str] = set()

        # Create the genesis block
        self.new_block(proof=100, previous_hash="1")

    # -- node management -------------------------------------------------
    def register_node(self, address: str) -> None:
        """Add a new node address to the network."""
        parsed = urlparse(address)
        if parsed.netloc:
            self.nodes.add(parsed.netloc)
        elif parsed.path:
            # Accept URL without scheme like '192.168.0.5:5000'
            self.nodes.add(parsed.path)
        else:
            raise ValueError("Invalid URL")

    def valid_chain(self, chain: List[Block]) -> bool:
        """Check if a blockchain is valid."""
        for index in range(1, len(chain)):
            block = chain[index]
            prev = chain[index - 1]

            if block.previous_hash != self.hash(prev):
                return False
            if not self.valid_proof(prev.proof, block.proof, self.hash(prev)):
                return False
        return True

    def resolve_conflicts(self) -> bool:
        """Consensus algorithm resolving conflicts by replacing our chain with the longest valid chain in the network."""
        neighbours = self.nodes
        new_chain: Optional[List[Block]] = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f"http://{node}/chain")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = [Block(**b) for b in response.json()["chain"]]
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        return False

    # -- block and transaction management --------------------------------
    def new_block(self, proof: int, previous_hash: Optional[str] = None) -> Block:
        """Create a new block and add it to the chain."""
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.hash(self.chain[-1]),
        )

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, word: str, sender: str, recipient: str, value: Optional[int] = None) -> int:
        """Add a new word transaction to the list of transactions.

        Returns the index of the block that will hold this transaction."""
        tx_value = word_value(word) if value is None else value

        self.current_transactions.append(
            {
                "word": word,
                "value": tx_value,
                "sender": sender,
                "recipient": recipient,
            }
        )

        return self.last_block.index + 1

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    @staticmethod
    def hash(block: Block) -> str:
        """Create SHA-256 hash of a Block."""
        block_dict = {
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": block.transactions,
            "proof": block.proof,
            "previous_hash": block.previous_hash,
        }
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int, last_hash: str) -> int:
        """Simple proof-of-work algorithm:

        - Find a number p' such that hash(pp' + last_hash) contains leading 4 zeros.
        - p is the previous proof, and last_hash is the hash of the previous block."""
        proof = 0
        while not self.valid_proof(last_proof, proof, last_hash):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int, last_hash: str) -> bool:
        guess = f"{last_proof}{proof}{last_hash}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
