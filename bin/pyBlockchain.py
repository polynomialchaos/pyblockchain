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
import os
from json import load
from pyblockchain import Blockchain, proof_of_work

def main():

    export_file = 'blockchain.json'
    blockchain = Blockchain(difficulty=16, load=export_file if os.path.exists(export_file) else None)

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

    blockchain.write(export_file, indent=4)

if __name__ == '__main__':

    main()
