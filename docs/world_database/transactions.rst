.. _ch_trans:

Transactions
================================================================================

Transactions are requests sent to the ETC network from user accounts.
Transactions can send funds, create new smart contracts, or, execute existing
smart contracts.  Transaction resource requirements are measured in *gas*
units.  Gas is purchased with classic ether.  All transactions contain the
following six elements:

to (receiving address)
   Transactions contain receiving account addresses.  This component is an empty
   string for smart contract creation transactions for which new accounts,
   with new addresses, will be created.

init or data (constructor or calling arguments)
   For smart contract creation transactions, this contains the
   associated constructors.  For smart contract execution transactions, this
   contains the data operated on.

value (transfer amount)
   amount of classic ether, in units of wei, to be transferred to the receiving
   account

gas price
   offer of classic ether willing to pay per gas unit

gas limit (maximum gas purchase)
   maximum number of gas units willing to purchase

nonce
   originating user account nonces

v, r, s (digital signature)
   three numbers comprising the digital signature of the transaction with
   respect to the private key of the originating account

If applying transactions requires more gas to complete than the maximum gas
amount allowed, then all the effects are reversed except that the user is still
charged for the gas utilized.
