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
from functools import wraps

max_nonce = 2 ** 32 # 4 billion

def profile(function_pointer):
    @wraps(function_pointer)
    def with_profiling(*args, **kwargs):
        start_time = time()
        ret = function_pointer(*args, **kwargs)
        elapsed_time = time() - start_time

        print(' >>> Function {:} called with {:} execution time!'.format(
            function_pointer.__name__, elapsed_time))

        return ret

    return with_profiling

@profile
def proof_of_work(header, difficulty_bits):
    """Return a valid none as proof of work."""
    # calculate the difficulty target
    target = 2 ** (256-difficulty_bits)

    for nonce in range(max_nonce):
        string_object = str(header)+str(nonce)
        byte_object = string_object.encode()

        hash_result = hashlib.sha256(byte_object).hexdigest()

        # check if this is a valid result, below the target
        if int(hash_result, 16) < target:
            return nonce, hash_result

    raise(RuntimeError('Maximum nonce limit reached!'))

class Blockchain():
    def __init__(self, difficulty=16):
        self.difficulty = difficulty
        self._chain = []
        self._pending_transactions = []

        nonce, hash_result = proof_of_work('root_hash', self.difficulty)
        self.new_block(proof=nonce, previous_hash=hash_result)

    def add_transaction(self, sender, recipient, amount):
        """Add a new transaction to the pending transactions."""
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        self._pending_transactions.append(transaction)

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

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
            'previous_hash': previous_hash or self.hash(self.last_block),
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

if __name__ == '__main__':

    blockchain = Blockchain(difficulty=23)

    blockchain.add_transaction("Satoshi", "Mike", 1)
    blockchain.add_transaction("Mike", "Satoshi", 1)
    blockchain.add_transaction("Satoshi", "Hal Finney", 5)

    hash_block = blockchain.hash(blockchain.last_block)
    nonce, _ = proof_of_work(hash_block, blockchain.difficulty)
    blockchain.new_block(nonce)

    print(blockchain.last_block)

    blockchain.add_transaction("Mike", "Alice", 1)
    blockchain.add_transaction("Alice", "Bob", 0.5)
    blockchain.add_transaction("Bob", "Mike", 0.2)

    hash_block = blockchain.hash(blockchain.last_block)
    nonce, _ = proof_of_work(hash_block, blockchain.difficulty)
    blockchain.new_block(nonce)

    print(blockchain.last_block)