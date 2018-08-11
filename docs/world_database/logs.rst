.. _ch_logs:

Logs
================================================================================

For every transaction, the following information is logged:

* final state root hash

* cumulative gas usage

For example, the final state root hash logged with regards to the third
transaction of block 5,889,421 is:

.. sourcecode:: javascript

   0x915dd6ca7dca0c1d68c3cc84e0d8551394f353042af35bd6b5cf21084d643a27

That is the state root hash after the first three transactions have been
applied. Since all transactions for that block require 21,000 gas, the
cumulative gas usage logged with regards to the third transaction is 63,000
gas.  Smart contracts can request the logging of additional information.

.. _sec_logging_requests:

--------------------------------------------------------------------------------
Logging Requests
--------------------------------------------------------------------------------

Smart contracts can request the logging of additional information. Specifically,
smart contracts can request the logging of named lists of values. For example,
suppose a smart contract based game wanted to record the following information
for a player:

* account address

* health points

* gold coins

This information could be placed in a list named *Player* as in the following
Solidity code declaration:

.. sourcecode:: javascript

   event Player(address user, uint256 health, uint256 gold);

Here is Solidity code to write specific player data to the blockchain:

.. sourcecode:: javascript

   emit Player(0xdf0b7310588741cad931de88bc6c4f687cdf0e16, 234, 198);

Note that variable values are stored but not variable names. Note also that user
interfaces can access this logged information but that smart contracts cannot.

Logging requests are identified on the blockchain by hashes formed from their
list names and list value types. For example, the aforementioned *Player*
logging request is found on the blockchain by searching for the Keccak 256 hash
of the string “Player(address,uint256,uint256)”.

:ref:`Bloom filters <app_bloom_filters>` are always included with all smart
contract logging requests. Bloom filters are hashes created from data to speed
up searches with minimal storage requirements.

.. _subsec_indexed_values:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Indexed Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another way to speed up logging request searches is to store logging request
values in a special way. Specifically, they can be stored as if they were
additional logging request identifiers. This avoids having to extract them from
the bytes encoding all the logging request values. Values stored in this manner
are referred to as indexed values. For example, the Ethereum Token Standard
specifies logging requests with indexed values as in this Solidity code:

.. sourcecode:: javascript

   event Transfer(address indexed sender, address indexed receiver, uint256 amount);

The log for transaction

.. sourcecode:: javascript

   0x104068d21afd428ce8eb5d9da155e11ba53414e40e088c884a678c6c203083d7

contains three logging request identifiers:

.. sourcecode:: javascript

   0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef

   0x000000000000000000000000efb32e82cf9d65a828d6d99e12f0beab01a467a6

   0x000000000000000000000000e71ac6142eaffc85ee3b9049facbcb13bc11402a

The first value is the Keccak 256 hash of the string
“Transfer(address,address,unit256)”. The other values are the sending and
receiving addresses with regards to the corresponding token transfer.
