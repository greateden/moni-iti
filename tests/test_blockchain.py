from wordchain.blockchain import Blockchain


def test_new_transaction_and_block():
    bc = Blockchain()
    index = bc.new_transaction("chatgpt", sender="alice", recipient="bob")
    assert index == bc.last_block.index + 1
    # Mine the block
    last_block = bc.last_block
    proof = bc.proof_of_work(last_block.proof, bc.hash(last_block))
    bc.new_block(proof)
    # Check that transaction was recorded with computed value
    transactions = bc.chain[-1].transactions
    assert transactions[0]["word"] == "chatgpt"
    # c=3 h=8 a=1 t=20 g=7 p=16 t=20 => sum
    assert transactions[0]["value"] == 3 + 8 + 1 + 20 + 7 + 16 + 20
