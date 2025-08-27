"""Flask application exposing the Wordchain network API."""

from __future__ import annotations

import json
from uuid import uuid4
from flask import Flask, jsonify, request

from .blockchain import Blockchain

# Instantiate the node
app = Flask(__name__)

# Generate a globally unique address for this node
NODE_IDENTIFIER = str(uuid4()).replace("-", "")

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route("/mine", methods=["GET"])
def mine():
    """Endpoint to mine a new block."""
    last_block = blockchain.last_block
    last_hash = blockchain.hash(last_block)
    proof = blockchain.proof_of_work(last_block.proof, last_hash)

    # Reward for mining: create a new transaction with sender "0"
    blockchain.new_transaction(
        word="MINING",
        sender="0",
        recipient=NODE_IDENTIFIER,
        value=1,
    )

    block = blockchain.new_block(proof, last_hash)

    response = {
        "message": "New Block Forged",
        "index": block.index,
        "transactions": block.transactions,
        "proof": block.proof,
        "previous_hash": block.previous_hash,
    }
    return jsonify(response), 200


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()

    required = ["word", "sender", "recipient"]
    if not values or not all(k in values for k in required):
        return "Missing values", 400

    index = blockchain.new_transaction(values["word"], values["sender"], values["recipient"])

    response = {"message": f"Transaction will be added to Block {index}"}
    return jsonify(response), 201


@app.route("/chain", methods=["GET"])
def full_chain():
    chain = [block.__dict__ for block in blockchain.chain]
    response = {"chain": chain, "length": len(chain)}
    return jsonify(response), 200


@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    values = request.get_json()
    nodes = values.get("nodes") if values else None
    if nodes is None or not isinstance(nodes, list):
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        "message": "New nodes have been added",
        "total_nodes": list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route("/nodes/resolve", methods=["GET"])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {"message": "Our chain was replaced", "new_chain": [b.__dict__ for b in blockchain.chain]}
    else:
        response = {"message": "Our chain is authoritative", "chain": [b.__dict__ for b in blockchain.chain]}

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
