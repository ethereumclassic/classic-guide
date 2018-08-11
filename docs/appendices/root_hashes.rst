.. _app_root_hashes:

Root Hashes
================================================================================

The Ethereum Classic (ETC) blockchain contains "root hashes" that help maintain
the integrity of various components of the ETC system. I will describe these
root hashes including how to calculate them.

Some important ETC data structures are sets of key value pairs that are stored
as Merkle Patricia tries. Tries are trees of nodes. The top nodes correspond to
the "roots" of the trees. Therefore, hashes associated with the top nodes of
Merkle Patricia tries are referred to as root hashes. Specifically, root hashes
are the Keccak 256 hashes of the Recursive Length Prefix (RLP) encodings of the
top nodes.

ETC block headers contain root hashes for states, transaction lists and receipt
lists. ETC block headers also implicitly specify storage root hashes in the
state root hashes.

Here is Python code that implements RLP encoding and decoding:

.. sourcecode:: python

   import math

   BYTE_LEN = 8

   def n_bytes(integer):
           """
           Finds the numbers of bytes needed to represent integers.
           """

           return math.ceil(integer.bit_length() / BYTE_LEN)

   def get_len(input, extra):
           """
           Finds the lengths of the longest inputs using the given extra values.
           """

           n_bytes = input[0] - extra

           return 1 + n_bytes + int.from_bytes(input[2:2 + n_bytes], "big")

   def encode(input):
           """
           Recursive Length Prefix encodes inputs.
           """

           if isinstance(input, bytes):
                   body = input
                   if   (len(body) == 1) and (body[0] < 128):
                           header = bytes([])
                   elif len(body) < 56:
                           header = bytes([len(body) + 128])
                   else:
                           len_   = len(body)
                           len_   = len_.to_bytes(n_bytes(len_), "big")
                           header = bytes([len(len_) + 183]) + len_
                   result = header + body
           else:
                   body = bytes([])
                   for e in input:
                           body += encode(e)
                   if len(body) < 56:
                           header = bytes([len(body) + 192])
                   else:
                           len_   = len(body)
                           len_   = len_.to_bytes(n_bytes(len_), "big")
                           header = bytes([len(len_) + 247]) + len_
                   result = header + body

           return result

   def decode(input):
           """
           Recursive Length Prefix decodes inputs.
           """

           if   input[0] < 128:
                   result = input
           elif input[0] < 184:
                   result = input[1:]
           elif input[0] < 192:
                   result = input[1 + (input[0] - 183):]
           else:
                   result = []
                   if input[0] < 248:
                           input = input[1:]
                   else:
                           input = input[1 + (input[0] - 247):]
                   while input:
                           if   input[0] < 128:
                                   len_ = 1
                           elif input[0] < 184:
                                   len_ = 1 + (input[0] - 128)
                           elif input[0] < 192:
                                   len_ = get_len(input, 183)
                           elif input[0] < 248:
                                   len_ = 1 + (input[0] - 192)
                           else:
                                   len_ = get_len(input, 247)
                           result.append(decode(input[:len_]))
                           input = input[len_:]

           return result

Here is Python code that calculates root hashes using the PySHA3 package. It
requires the RLP code above to be saved to an accessible location with the file
name rlp.py. Invoke the root_hash function on Python dictionaries representing
sets of ETC key value pairs. All keys and key values must be Python byte
strings:

.. sourcecode:: python

   import sha3
   import rlp

   HASH_LEN = 32
   HEXADEC  = 16

   def remove(dict_, segment):
           """
           Removes initial key segments from the keys of dictionaries.
           """

           return {k[len(segment):] : v for k, v in dict_.items()}

   def select(dict_, segment):
           """
           Selects dictionary elements with given initial key segments.
           """

           return {k : v for k, v in dict_.items() if k.startswith(segment)}

   def find(dict_):
           """
           Finds common initial segments in the keys of dictionaries.
           """

           segment = ""
           for i in range(min([len(e) for e in dict_.keys()])):
                   if len({e[i] for e in dict_.keys()}) > 1:
                           break
                   segment += list(dict_.keys())[0][i]

           return segment

   def patricia_r(dict_):
           """
           Creates Patricia tries that begin with regular nodes.
           """

           pt = (HEXADEC + 1) * [None]
           if "" in dict_:
                   pt[-1] = dict_[""]
                   del(dict_[""])
           for e in {e[0] for e in dict_.keys()}:
                   pt[int(e, HEXADEC)] = patricia(remove(select(dict_, e), e))

           return pt

   def patricia_s(dict_):
           """
           Creates Patricia tries composed of one key ending special node.
           """

           pt = list(dict_.items())[0]
           if len(pt[0]) % 2 == 0:
                   pt = (bytes.fromhex("20" + pt[0]), pt[1])
           else:
                   pt = (bytes.fromhex("3"  + pt[0]), pt[1])

           return pt

   def patricia(dict_):
           """
           Creates Patricia tries from dictionaries.
           """

           segment = find(dict_)
           if   len(dict_) == 1:
                   pt = patricia_s(dict_)
           elif segment:
                   dict_ = remove(dict_, segment)
                   if len(segment) % 2 == 0:
                           pt = [bytes.fromhex("00" + segment), patricia_r(dict_)]
                   else:
                           pt = [bytes.fromhex("1"  + segment), patricia_r(dict_)]
           else:
                   pt = patricia_r(dict_)

           return pt

   def merkle(element):
           """
           Encodes Patricia trie elements using Keccak 256 hashes and RLP.
           """

           if   not element:
                   merkle_ = b""
           elif isinstance(element, str):
                   merkle_ = bytes.fromhex(element)
           elif isinstance(element, bytes):
                   merkle_ = element
           else:
                   merkle_ = [merkle(e) for e in element]
                   rlp_    = rlp.encode(merkle_)
                   if len(rlp_) >= HASH_LEN:
                           merkle_ = sha3.keccak_256(rlp_).digest()

           return merkle_

   def merkle_patricia(dict_):
           """
           Creates Merkle Patricia tries from dictionaries.
           """

           return [merkle(e) for e in patricia(dict_)]

   def root_hash(dict_):
           """
           Calculates root hashes of Merkle Patricia tries from dictionaries.
           """

           dict_ = {k.hex() : v for k, v in dict_.items()}

           return sha3.keccak_256(rlp.encode(merkle_patricia(dict_))).hexdigest()

Here are sample calculations for all of the root hash types found in the ETC
blockchain. They require the root hash code above to be saved to an accessible
location with the file name root_hash.py. The RLP code above must be saved to an
accessible location with the file name rlp.py. Lastly, the following code to
convert integers to Python byte strings must be saved to an accessible location
with the file name int_to_bytes.py:

.. sourcecode:: python

   def int_to_bytes(number):
           if number:
                   hex_ = hex(number)[2:]
                   if len(hex_) % 2 != 0:
                           hex_ = "0" + hex_
                   result = bytes.fromhex(hex_)
           else:
                   result = b""

           return result

For state root hash calculations, the keys of the Python dictionaries must be
the Keccak 256 hashes of the account addresses. The key values must be the RLP
encodings of lists containing the corresponding account nonces, balances,
storage root hashes, and, smart contract hashes. One way to obtain state
information is with an ETC Geth node. For example, the following ETC Geth node
command prints the state information for block 1,000,000:

geth dump 1000000

Here is the beginning of the voluminous output:

.. sourcecode:: javascript

   {
       "root": "0e066f3c2297a5cb300593052617d1bca5946f0caa0635fdb1b85ac7e5236f34",
       "accounts": {
           "843fd22c88d59e57ae1856a871a5d95e95b0a656": {
               "balance": "52500000000000",
               "nonce": 1,
               "root": "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
               "codeHash":
               "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
                 ,
               "code": "",
               "storage": {}
           },
           "dcd0b6fa4f0a26a7b12325b0d09b5b809c5aef84": {
               "balance": "9375377890126000",
               "nonce": 1,
               "root": "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
               "codeHash":
               "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
                 ,
               "code": "",
               "storage": {}
           },
           "7d62878a7235e95d56f802f80835543cac711f90": {
               "balance": "204544100000000000",
               "nonce": 0,
               "root": "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
               "codeHash":
               "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
                 ,
               "code": "",
               "storage": {}
           },
           "67db390312dc02a140c358add4f37966c7775096": {
               "balance": "0",
               "nonce": 2,
               "root": "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
               "codeHash":
               "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
                 ,
               "code": "",
               "storage": {}
           },

   ...etc.

The following code prints the state root hash for block 1,000,000 which is
0x0e066f3c2297a5cb300593052617d1bca5946f0caa0635fdb1b85ac7e5236f34. It requires
the aforementioned state information to be saved to an accessible location with
the file name state_1000000:

.. sourcecode:: python

   import root_hash
   import sha3
   import rlp
   import int_to_bytes

   dict_ = {}
   state = eval(open("state_1000000", "r").read())
   for address in state["accounts"]:
           account    = state["accounts"][address]
           account    = [int_to_bytes.int_to_bytes(int(account["nonce"])),
                         int_to_bytes.int_to_bytes(int(account["balance"])),
                         bytes.fromhex(account["root"]),
                         bytes.fromhex(account["codeHash"])]
           key        = sha3.keccak_256(bytes.fromhex(address)).digest()
           value      = rlp.encode(account)
           dict_[key] = value

   print(root_hash.root_hash(dict_))

For transaction list root hash calculations, the keys of the Python dictionaries
must be the RLP encodings of the transaction indices starting from zero. The key
values must be the RLP encodings of lists containing the corresponding
transaction nonces, gas prices, gas usage maxima, destination addresses, ether
sent, data sent and digital signature components. The following code prints the
transaction list root hash for the transactions in block 4,000,003 which is
0xad79d498b7e407d3a2b32c13a380ee93635da2b3e0696c39563cbd5c32d368b2:

.. sourcecode:: python

   import root_hash
   import sha3
   import rlp
   import int_to_bytes

   key_1     = rlp.encode(int_to_bytes.int_to_bytes(0))

   nonce     = int_to_bytes.int_to_bytes(1514565)
   gas_price = int_to_bytes.int_to_bytes(20000000000)
   gas_max   = int_to_bytes.int_to_bytes(50000)
   dest      = 0x7b96a5006d5fc86d05f8799fe1fc6f7d23b24969
   dest      = int_to_bytes.int_to_bytes(dest)
   ether     = int_to_bytes.int_to_bytes(1001525814273650153)
   data      = b""
   v         = int_to_bytes.int_to_bytes(157)
   r         = 0x8815ebbcdb56717a30193db4629fa7565d2fb06c6fba2aaf0db06deaf932955d
   r         = int_to_bytes.int_to_bytes(r)
   s         = 0x4dbd4dcb648114859f57122d804b85c2dd60d0b502fb93d0ef770d50bfa3a59d
   s         = int_to_bytes.int_to_bytes(s)
   trans     = [nonce, gas_price, gas_max, dest, ether, data, v, r, s]
   value_1   = rlp.encode(trans)

   key_2     = rlp.encode(int_to_bytes.int_to_bytes(1))

   nonce     = int_to_bytes.int_to_bytes(43565)
   gas_price = int_to_bytes.int_to_bytes(20000000000)
   gas_max   = int_to_bytes.int_to_bytes(21000)
   dest      = 0x7ccfb3028404225e4e9da860f85274e30ccc9275
   dest      = int_to_bytes.int_to_bytes(dest)
   ether     = int_to_bytes.int_to_bytes(109404508089999998976)
   data      = b""
   v         = int_to_bytes.int_to_bytes(28)
   r         = 0x8d6e2fcfe032d2612d2ea56da6d07b6a94004a4ec7cbe2c3f086db1a194aa679
   r         = int_to_bytes.int_to_bytes(r)
   s         = 0x6ed1333497c12b4549e55d117977bf60bb96872dfb05816fb7ce25c7396ef23a
   s         = int_to_bytes.int_to_bytes(s)
   trans     = [nonce, gas_price, gas_max, dest, ether, data, v, r, s]
   value_2   = rlp.encode(trans)

   print(root_hash.root_hash({key_1 : value_1, key_2 : value_2}))

For receipt list root hash calculations, the keys of the Python dictionaries
must be the RLP encodings of the receipt indices starting from zero. The key
values must be the RLP encodings of lists containing the corresponding receipt
state root hashes, cumulative gas amounts, log Bloom filters and logs. The
following code prints the receipt list root hash for the receipts in block
4,000,003 which is
0x4b3b43affc2927a152b9d6f18e378cf33671f8606e8549de292ae36b8a691584:

.. sourcecode:: python

   import root_hash
   import sha3
   import rlp
   import int_to_bytes

   key_1   = rlp.encode(int_to_bytes.int_to_bytes(0))

   state   = "abca6dd8fb332962c1c14c02d13b2082aee152496dc809d9642e2deca07fb7c2"
   gas     = 0x5208
   bloom   = 256 * "00"
   logs    = []
   receipt = [bytes.fromhex(state),
              int_to_bytes.int_to_bytes(gas),
              bytes.fromhex(bloom),
              logs]
   value_1 = rlp.encode(receipt)

   key_2   = rlp.encode(int_to_bytes.int_to_bytes(1))

   state   = "029b0eb2c76ff08a1cf47aba4be53ff1c20b01026206eca248b47e0657f97524"
   gas     = 0xa410
   bloom   = 256 * "00"
   logs    = []
   receipt = [bytes.fromhex(state),
              int_to_bytes.int_to_bytes(gas),
              bytes.fromhex(bloom),
              logs]
   value_2 = rlp.encode(receipt)

   print(root_hash.root_hash({key_1 : value_1, key_2 : value_2}))

For storage root hash calculations, the keys of the Python dictionaries must be
the Keccak 256 hashes of the storage indices for all nonzero storage values. The
key values must be the RLP encodings of the corresponding storage values. The
following code prints the storage root hash for the account with the address
0xd4eae4ae8565f3ecf218191fb267941d98a2c77a which is
0x9f630ea9c8cc6e9f7ecbc08cb7f9e901c14b788cc8f2ae64e3134cf3cb089f55. Note that
this result was correct as of block 5,874,861 but may possibly change
afterwards:

.. sourcecode:: python

   import root_hash
   import sha3
   import rlp
   import int_to_bytes

   KEY_LEN = 32
   ZERO    = b"\x00"

   dict_   = {}
   storage = [(0, 0x51f24771a5a2720456076e7c81d59753dac20e1f),
              (1, 0x4563918244f40000),
              (3, 0x55c64da8),
              (4, 0x6f05b59d3b20000),
              (5, 0x4fb5acbe16ffdda225cb14c64aa84c7e253b08ae)]
   for e in storage:
           key        = int_to_bytes.int_to_bytes(e[0])
           key        = (KEY_LEN - len(key)) * ZERO + key
           key        = sha3.keccak_256(key).digest()
           value      = rlp.encode(int_to_bytes.int_to_bytes(e[1]))
           dict_[key] = value

   print(root_hash.root_hash(dict_))

Root hashes are vital for the operation of the ETC world computer. The ETC
system utilizes state, transaction list, receipt list and storage root
hashes. These ETC root hashes can be found with a detailed recipe involving RLP
encodings, Keccak 256 hashes and Merkle Patricia tries.
