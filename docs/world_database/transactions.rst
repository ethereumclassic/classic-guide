.. _ch_trans:

Transactions
================================================================================

Transactions are requests sent to the ETC network from user accounts.
Transactions can send funds, create new smart contracts, or, execute existing
smart contracts.  Transaction resource requirements are measured in *gas*
units.  Gas is purchased with classic ether.  All transactions contain the
following six elements:

addresses
   Transactions contain receiving account addresses.  This component is an empty
   string for smart contract creation transactions for which new accounts,
   with new addresses, will be created.

data
   For smart contract creation transactions, this contains the
   associated constructors.  For smart contract execution transactions, this
   contains the data operated on.

gifts
   amount in classic ether to be transferred to the receiving account

offers
   price in classic ether willing to pay per gas unit, and, the maximum gas
   units willing to purchase

nonces
   originating user account nonce

digital signatures
   digital signature of the transaction with respect to the private key of the
   originating user account

If applying transactions requires more gas to complete than the maximum gas
amount allowed, then all the effects are reversed except that the user is still
charged for the gas utilized.
