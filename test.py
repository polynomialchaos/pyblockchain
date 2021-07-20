# MIT License

# Copyright (c) 2021 Florian Eigentler

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import hashlib
import json
from time import time

class Blockchain():
    def __init__(self):
        self._chain = []
        self._pending_transactions = []

        self.new_block(previous_hash="root_block", proof=0)

    def _hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    def add_transaction(self, sender, recipient, amount):
        """Add a new transaction to the pending transactions."""
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        self._pending_transactions.append(transaction)

    @property
    def last_block(self):
        """Return the most recent block."""
        return self._chain[-1]

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': self.number_blocks,
            'timestamp': time(),
            'transactions': self._pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self._hash(self.last_block),
        }

        self._chain.append(block)
        self._pending_transactions = []

    @property
    def number_blocks(self):
        """Return the number of pending transactions."""
        return len(self._chain)

    @property
    def number_pending_transactions(self):
        """Return the number of pending transactions."""
        return len(self._pending_transactions)

blockchain = Blockchain()
blockchain.add_transaction("Satoshi", "Mike", 1)
blockchain.add_transaction("Mike", "Satoshi", 1)
blockchain.add_transaction("Satoshi", "Hal Finney", 5)
blockchain.new_block(12345)

print(blockchain.last_block)
print(blockchain._hash(blockchain.last_block))

# t4 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
# t5 = blockchain.new_transaction("Alice", "Bob", '0.5 BTC')
# t6 = blockchain.new_transaction("Bob", "Mike", '0.5 BTC')
# blockchain.new_block(6789)

# print("Genesis block: ", blockchain.chain)