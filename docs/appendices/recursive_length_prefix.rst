.. _app_rlp:

Recursive Length Prefix
================================================================================

Serialization is the process of encoding data structures into byte sequences. It
is also referred to as marshalling and pickling. Serialization is necessary when
storing and sending data structures.

RLP is a serialization format created by Ethereum developers for storage and
communications. It is used for all data structures such as accounts,
transactions and blocks. RLP is simpler than the alternatives such as Extensible
Markup Language (XML), JavaScript Object Notation (JSON), Binary JSON (BSON),
Protocol Buffers and Bencode.

RLP is also consistent. The same inputs are always converted to the same byte
sequences. This is not true of all serialization formats. For example, when
encoding sets of key value pairs, some schemes do not specify an ordering.

RLP operates on byte sequences and lists. Lists can contain byte sequences and
other lists. The interpretation of all inputs is handled by other protocols. For
byte sequences, small headers are added which depend on the length. For lists,
the elements are encoded separately and concatenated. As with byte sequences,
small headers are added which depend on the length. Lastly, all lengths are
encoded in big endian format.

Here are Python functions which implement RLP encoding and decoding:

.. sourcecode:: python

   #!/usr/bin/env python3

   import math

   N_BITS_PER_BYTE = 8

   def n_bytes(integer):
           """
           Finds the numbers of bytes needed to represent integers.
           """

           return math.ceil(integer.bit_length() / N_BITS_PER_BYTE)

   def get_len(input, extra):
           """
           Finds the lengths of the longest inputs using the given extra values.
           """

           n_bytes = input[0] - extra

           return 1 + n_bytes + int.from_bytes(input[2:2 + n_bytes], "big")

   def rlp_encode(input):
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
                           body += rlp_encode(e)
                   if len(body) < 56:
                           header = bytes([len(body) + 192])
                   else:
                           len_   = len(body)
                           len_   = len_.to_bytes(n_bytes(len_), "big")
                           header = bytes([len(len_) + 247]) + len_
                   result = header + body

           return result

   def rlp_decode(input):
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
                           result.append(rlp_decode(input[:len_]))
                           input = input[len_:]

           return result

Notice that the functions are recursive. Notice also that the functions work for
inputs requiring up to about 18 million terabytes. Here are examples of their
usage:

.. sourcecode:: python

   >>> rlp_encode(b"A")
   b'A'

   >>> rlp_encode(b"12345")
   b'\x8512345'

   >>> rlp_encode(20 * b"12345")
   b'\xb8d12345123451234512345123451234512345123451234512345123451234512345123451234512345123
     45123451234512345'

   >>> rlp_encode([b"12345"])
   b'\xc6\x8512345'

   >>> rlp_encode([b"abcde", 3 * [b"12345"], [b"fghij"], b"67890", 4 * [b"klmno"]])
   b'\xf8\x85abcde\xd2\x8512345\x8512345\x8512345\xc6\x85fghij\x8567890\xd8\x85klmno\x85klmno
     \x85klmno\x85klmno'

   >>> rlp_decode(b"\x8512345")
   b'12345'

   >>> rlp_decode(b"\xc6\x8512345")
   [b'12345']

   >>> rlp_decode(b"\xf8\x85abcde\xd2\x8512345\x8512345\x8512345\xc6\x85fghij\x8567890\xd8\x85klmno\x85klmno\x85klmno\x85klmno")
   [b'abcde', [b'12345', b'12345', b'12345'], [b'fghij'], b'67890', [b'klmno', b'klmno', b'klmno', b'klmno']]

RLP is an elegant and approachable serialization format used extensively by
ETC. It can be quickly mastered thereby illuminating this important aspect of
the system.
