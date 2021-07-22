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
from .utils import profile

max_nonce = 2 ** 32 # 4 billion

@profile
def proof_of_work(header, difficulty_bits):
    """Return a valid none as proof of work."""
    # calculate the difficulty target
    target = 2 ** (256-difficulty_bits)

    # loop until max_nonce
    for nonce in range(max_nonce):
        string_object = str(header)+str(nonce)
        byte_object = string_object.encode()

        hash_result = hashlib.sha256(byte_object).hexdigest()

        # check if this is a valid result, below the target
        if int(hash_result, 16) < target:
            return nonce, hash_result

    raise(RuntimeError('Maximum nonce limit reached!'))