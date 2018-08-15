.. _ch_blocks:

Blocks
================================================================================

The ETC blockchain is composed of an array of blocks.  Blocks contain three
categories of information: *computation*, *consensus* and *context*.  Blocks
contain transaction related information (computation), mining related
information (consensus), and, information to properly locate blocks
on the blockchain (context).  All components except for two lists form the block
headers.

.. _sec_computation:

--------------------------------------------------------------------------------
Computation
--------------------------------------------------------------------------------

Transactions initiate all activity on the world computer.  This category
contains information related to this computation.  Specifically, these
block components consist of the following:

transaction list
   lists of transactions

transactions root (transaction list root hash)
   :ref:`root hashes <app_root_hashes>` of transaction lists

gas used (transaction list total gas requirement)
   gas requirements for *all* the transactions in the transaction list

state root (transaction list final state root hash)
   :ref:`root hashes <app_root_hashes>` of the states *after* each transaction
   is applied

receipts root (transaction log list root hash)
   :ref:`root hashes <app_root_hashes>` of transaction log lists

logs Bloom (transaction log list Bloom filter)
   :ref:`Bloom filters <app_bloom_filters>` of transaction log lists

It may seem problematic that blocks only contain root hashes of states and
transaction logs.  Nevertheless, the full specification of any state or
transaction log can always be obtained by reapplying all the transactions on the
blockchain with respect to the initial state.

.. _sec_consensus:

--------------------------------------------------------------------------------
Consensus
--------------------------------------------------------------------------------

Mining is the process of creating and validating new blocks. This is referred to
as mining because the participants (miners) are rewarded with newly created
ETC. The mining procedure is referred to as the consensus algorithm as it helps
users of ETC agree on an ordered set of transactions. This involves a race to
find certain numbers necessary to create new blocks.  These numbers are referred
to as *proof of work* information because they are "proof" that a certain amount
of computational work was done.  The block candidates that lose this race are
referred to as the *uncle* blocks since they are related to the parents or last
blocks added.  These block components consist of the following:

extra data (miner extra data)
   32 unused bytes added by miners

beneficiary (miner address)
   addresses with respect to block mining rewards

mix hash (miner validation help)
   values that help miners validate blocks faster

gas limit (miner gas maximum)
   maximum possible gas requirements to apply all transactions in blocks

nonce (proof of work information)
   the number required to add blocks to the blockchain

difficulty (proof of work difficulty)
   difficulty of finding proof of work information for the block

ommer header list (uncle header list)
   lists of the headers of the associated uncles

ommers hash (uncle header list root hash)
   Keccak 256 hashes of uncle header lists

The miner validation help components are necessary because slow block validation
risks certain denial of service attacks.  Miners are able to make slight
adjustments to the miner gas maxima of the next blocks they create if desired.
Uncles improve security by making attacks require performing more work.  The
consensus algorithm automatically increases the proof of work difficulty for the
next blocks when new blocks are being added too quickly. Likewise, the proof of
work difficulty decreases when new blocks are being added too slowly.

.. _sec_context:

--------------------------------------------------------------------------------
Context
--------------------------------------------------------------------------------

Blocks must always located correctly in the blockchain.  Here are the blockchain
components pertaining to context.

number (block number)
   the numbers of blocks that must precede blocks on the blockchain

parent hash (parent header hash)
   Keccak 256 hash of parent block headers

timestamp (date & time)
   dates and times that blocks were added to the blockchain

The parent block of a block is the preceding block on the blockchain.  Dates and
times are denoted by the number of seconds since 1970–01–01 00:00:00 UTC.

.. _sec_implicit_info:

--------------------------------------------------------------------------------
Accounts
--------------------------------------------------------------------------------

There is no explicit account information in the blockchain.  The only account
information is the state root hash.  To obtain account information, all the
transactions in all the blocks of the blockchain must be implemented on the
world computer with respect to the initial state.
