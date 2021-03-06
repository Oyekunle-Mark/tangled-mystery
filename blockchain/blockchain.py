import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from typing import NewType, Dict, Any

BlockType = NewType('BlockType', Dict[str, Any])


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof: int, previous_hash=None) -> BlockType:
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block: BlockType) -> str:
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        block_string = json.dumps(block, sort_keys=True).encode()

        # TODO: Hash this string using sha256

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> BlockType:
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string: str, proof: int) -> bool:
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        # set a initial guess concatenates block string and proof then encode them
        guess = f"{block_string}{proof}".encode()
        # create a guess hash and hexdigest it
        guess_hash = hashlib.sha256(guess).hexdigest()
        # then return True if the guess hash has the valid number of leading zeros otherwise return False
        return guess_hash[:6] == "000000"

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        """
        new_transaction that adds a new transaction to the list of transactions:

        :param sender: <str> Address of the Recipient
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the `block` that will hold this transaction
        """
        # create the transaction
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }
        # add the transaction to the current_transactions
        self.current_transactions.append(transaction)

        # return the number of the `block` that will hold this transaction
        return len(self.chain) + 1


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()

    # require the proof and id to be present
    required = ['proof', 'id']

    # if the values from data are not in required
    if not all(k in data for k in required):
        # then send a json message of missing values
        response = {'message': "Missing Values"}
        # return a 400 error
        return jsonify(response), 400

    proof = data["proof"]
    id = data["id"]

    # get the last block
    last_block = blockchain.last_block
    # stringify it and sort the keys
    last_block = json.dumps(last_block, sort_keys=True)
    # verify if the proof sent is valid
    is_valid = blockchain.valid_proof(last_block, proof)

    # if proof is valid
    if is_valid:
        # reward the miner for work so it can be part of the new block
        blockchain.new_transaction("0", id, 1)
        # make a new block
        new_block = blockchain.new_block(proof)

        # return a message to the miner
        return jsonify({
            "message": "New Block Forged",
            "block": new_block
        }), 200
    # otherwise
    else:
        # send a message that the proof is not valid
        return jsonify({"message": "Invalid proof."}), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        "length": len(blockchain.chain),
        "chain": blockchain.chain
    }

    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def get_last_block():
    return jsonify({
        "last_block": blockchain.last_block
    }), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()

    required = ['sender', 'recipient', 'amount']

    if not all(k in data for k in required):
        return 'Missing Values', 400

    # create a new transaction
    index = blockchain.new_transaction(
        data.get('sender'), data.get('recipient'), data.get('amount'))
    response = {'message': f'Transaction will be added to Block {index}'}

    return jsonify(response), 201


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
