.. _ch_accounts:

Accounts
================================================================================

Accounts are associated with users and
:ref:`smart contracts <ch_smart_contracts>`.   All accounts contain the
following five components:

address
   These are sets of numbers used to identify accounts.

balance
   All funds are associated with accounts.  This is a balance of classic ether,
   also know as ether or ETC.

code (smart contract)
   All smart contracts are associated with accounts.  This component is
   an empty string for user accounts.

storage
   All smart contracts have associated memory.  This component is an
   empty string for user accounts.

nonce
   Nonces are counters.  For user accounts, these equal the number of associated
   :ref:`transactions <ch_trans>`.  For smart contract accounts, these
   equal the number of associated smart contracts created.

All components of all accounts together comprise the *state* of the world
computer.

.. _sec_addresses:

Addresses
--------------------------------------------------------------------------------

All accounts are identified by addresses which are derived from secret random
numbers unique to each account.  These secret random numbers are referred to as
*private keys*.  Private keys must be kept private because they are used to
digitally sign transactions from accounts.  These transactions can transfer
funds, create smart contracts, and, execute smart contracts.  Strictly speaking,
private key numbers must be between 1 and

.. sourcecode:: shell

   115792089237316195423570985008687907852837564279074904382605163141518161494336

inclusive.  This requirement is necessary for their use in ETC digital
signatures. Some may be concerned that two users might unintentionally select
the same private key. The odds of that happening are vanishingly small. In fact,
the number of possible private keys is approximately equal to the number of
atoms in the entire universe!

All private keys are associated 64 byte numbers derived from them which are
referred to as *public keys*.  The calculation of public keys involves an odd
type of arithmetic with respect to pairs of numbers.  Here is a Python script
that calculates public keys from private keys:

.. sourcecode:: python

   #!/usr/bin/env python3

   """
   Calculates ETC public keys from ETC private keys.

   Usage: etc_pub_key <private key>
   """

   import random
   import sys

   A           = 0
   N           = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
   P           = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
   GX          = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
   GY          = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
   HEXADECIMAL = 16
   NUM_FORMAT  = "{{:0{}x}}".format(len(hex(P)[2:]))

   def inverse(number):
           """
           Inverts a number.
           """

           inverse = 1
           power   = number
           for e in bin(P - 2)[2:][::-1]:
                   if int(e):
                           inverse = (inverse * power) % P
                   power = (power ** 2) % P

           return inverse

   def add(pair_1, pair_2):
           """
           Adds two pairs.
           """

           if   pair_1 == "identity":
                   sum_ = pair_2
           elif pair_2 == "identity":
                   sum_ = pair_1
           else:
                   if pair_1 == pair_2:
                           numer   = 3 * pair_1[0] ** 2 + A
                           lambda_ = (numer * inverse(2 * pair_1[1])) % P
                   else:
                           numer   = pair_2[1] - pair_1[1]
                           denom   = pair_2[0] - pair_1[0]
                           lambda_ = (numer * inverse(denom)) % P
                   x    = (lambda_ ** 2 - pair_1[0] - pair_2[0])  % P
                   y    = (lambda_ * (pair_1[0] - x) - pair_1[1]) % P
                   sum_ = (x, y)

           return sum_

   def multiply(number, pair):
           """
           Multiplies a pair by a number.
           """

           product = "identity"
           power   = pair[:]
           for e in bin(number)[2:][::-1]:
                   if int(e):
                           product = add(power, product)
                   power = add(power, power)

           return product

   def convert(pair):
           """
           Converts pairs to numbers by concatenating the elements.
           """

           return int("".join([NUM_FORMAT.format(e) for e in pair]), HEXADECIMAL)

           print(convert(multiply(int(sys.argv[1]), (GX, GY))))

The reason for this convoluted process is so that private keys cannot be derived
from public keys.  This allows public keys to be safely shared with anyone.  If
you want to learn more, investigate elliptic curve cryptography. The reason for
this name is that historically it followed from calculations of the arc lengths
of ellipses.  Together, public and private keys are often referred to as
*wallets*.

Addresses are formed from the first 20 bytes of the Keccak 256 hashes of public
keys.  These are more often used to identify accounts rather than public
keys. Interestingly, public keys cannot be determined solely from addresses.
Here is a Python script that calculates addresses from public keys. It requires
the PySHA3 package. Addresses are typically expressed in hexadecimal notation
and that convention is followed in this script:

.. sourcecode:: python

   #!/usr/bin/env python3

   """
   Calculates ETC addresses from ETC public keys.

   Usage: etc_address <public key>
   """

   import sha3
   import binascii
   import sys

   N_ADDRESS_BYTES = 20
   N_PUB_KEY_BYTES = 64

   public_key = (int(sys.argv[1])).to_bytes(N_PUB_KEY_BYTES, byteorder = "big")
   print(sha3.keccak_256(public_key).hexdigest()[-2 * N_ADDRESS_BYTES:])

Here is a slightly edited session, on a Linux computer, that calculates a public
key and address with regards to a random private key. It uses the aforementioned
scripts saved in files called etc_pub_key and etc_address respectively:

.. sourcecode:: shell

   % PRIVATE_KEY="92788259381212812445638172234843282167646237087212249687358593145563035518424"

   % PUBLIC_KEY=`etc_pub_key $PRIVATE_KEY`

   % ADDRESS=`etc_address $PUBLIC_KEY`

   % echo $PRIVATE_KEY
   92788259381212812445638172234843282167646237087212249687358593145563035518424

   % echo $PUBLIC_KEY
   9808854183897174607002157792089896992612613490844656534725423301978228163634425857099752732031947328803605451685330420628756154476771607661633738743568351

   % echo $ADDRESS
   89b44e4d3c81ede05d0f5de8d1a68f754d73d997

.. _sec_ether_gas:

Ether & Gas
--------------------------------------------------------------------------------

To create and utilize smart contracts, user submit transactions.  Transactions
must pay for these services in classic ether.  Classic ether can be obtained by
purchasing it or by mining.  The smallest denomination of classic ether used in
the ETC system is 1 wei.  One billion billion (10¹⁸) weis equal a single classic
ether.  Due to the mining reward formula, the total supply of classic ether will
never exceed 210.6 million tokens.

The cost of creating and executing all smart contracts is measured in a made up
unit referred to as gas units.  Users submit transactions that pay for gas units
in terms of classic ether.  Notice that while the price of classic ether
fluctuates, the price of various services in terms of gas units does not.  In
transactions, user specify how much classic ether they are willing to pay per
gas unit.  For security reasons, the amount of gas that can be purchased and
used by blocks is limited.
