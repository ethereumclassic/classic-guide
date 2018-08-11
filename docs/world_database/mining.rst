.. _ch_mining:

Mining
================================================================================

Mining is the process of creating, validating, adding and distributing blocks.
Computers, and their administrators, that perform this service are referred to
as *miners*.  Anyone computer on the network can become a miner.  People are
incentivised to become miners because of the financial rewards.  Mining
amazingly allows the Ethereum Classis system to be managed and secured in a
trustless decentralized manner.

.. _sec_pow:

--------------------------------------------------------------------------------
Proof Of Work Information
--------------------------------------------------------------------------------

Valid blocks must contain certain numbers referred to as proof of work
information.  These numbers are also referred to as *nonces*.  Miners compete to
be the first to find this proof of work information and thereby add new blocks
to the blockchain.  Finding proof of work information is intentionally made
difficult.  This difficulty is a main reason for the security of the blockchain.

The difficult process of finding adequate nonces involves the following.  Nonces
must be found such that certain hashes of the blocks, with the nonces added,
have numerical values below specified maxima.  The only way to find such hashes
is to simply try as many nonce guesses as possible until adequate hashes are
found.  The maxima are automatically adjusted to keep the average block addition
time around 15 seconds.  Ethash is the hashing algorithm in this process.

.. _sec_ethash:

--------------------------------------------------------------------------------
Ethash
--------------------------------------------------------------------------------

The Ethash hashing algorithm requires the determination of a certain extremely
large directed acyclic graph that depends on block numbers.  Quickly calculating
several Ethash hashes requires storing the entire directed acyclic graph in
memory.  These large memory requirements thwart attempts to dominate the mining
process by building application specific integrated circuits (ASICs).


.. _sec_uncles:

--------------------------------------------------------------------------------
Uncle Blocks
--------------------------------------------------------------------------------

In the contest to add blocks to the blockchain, the losing blocks can be
leveraged to increase the security of the blockchain.  These losing blocks, to
be used this way, must have parent blocks that are at most six blocks from the
growing end of the blockchain.  Miners gain additional financial rewards when
they mention the hashes of the headers of these losing blocks in blocks that are
accepted.  This uncle block system is referred to as the GHOST protocol.

Here is why uncle blocks increase the security of the blockchain.  The mining
contest will inevitably create multiple chains of blocks.  The convention is
that the official chain is the one that is the most difficult to
reproduce.  Adding uncle blocks increases the difficulty of reproducing the
official chain.

Uncle blocks are especially useful when blocks are not propagating quickly
throughout the network.  This leads to many losing blocks as miners keep adding
blocks to outdated versions of the official chain.  As block creation times
thereby increase, the security of the network decreases.  This is fortunately
mitigated with uncle blocks.

.. _sec_mining_pools:

--------------------------------------------------------------------------------
Mining Pools
--------------------------------------------------------------------------------

Because of the nature of the mining contest, the average expected mining rewards
are proportional to the amount of computational resources dedicated to mining.
There can still be variability in payout frequencies due to the random nature of
the mining process.  In order to deal with this variability, miners often join
groups referred to as mining pools.

Some mining pools may lead to large amounts of mining resources in the control
of a few individuals.  Fortunately, there are trustless decentralized mining
pools that avoid this risk.

.. _sec_mining_rewards:

--------------------------------------------------------------------------------
Mining Rewards
--------------------------------------------------------------------------------

Mining rewards consists of three parts:

Base Rewards
    This part depends on the block numbers. It is paid with newly created
    funds. Every five million blocks (about 2.4 years) this part decreases by
    20%. Initially it was 5 ETC. It changed to 4 ETC after block number five
    million and will continue to change in the future.

    Define the block era E as a function of the block number N as follows (//
    denotes integer division):

.. sourcecode:: bash

   E = (N - 1) // 5000000

Then the base reward is as follows:

.. sourcecode:: bash

   5 ⋅ 0.8:superscript:`E`

Uncle Rewards
   This part depends on the number of uncle blocks included as well as the block
   numbers. It is also paid with newly created funds. Each block can include at
   most two uncle blocks. The reward for each uncle block is an additional
   3.125% of the base reward.

   For the block era E and number of uncles U, the total uncle reward is as
   follows:

.. sourcecode:: bash

   0.03125 ⋅ U ⋅ (5 ⋅ 0.8:superscript:`E`)

After block number five million, miners that create the uncle blocks began
getting this same reward per uncle block.

Gas Rewards
   This part depends on the transactions included. It is paid from the
   originating accounts. Miners execute the transactions and receive payments
   for the gas required. Each transactions specifies a price paid per unit gas.

   For gas requirements G₁, G₂, G₃, … and corresponding gas prices P₁, P₂, P₃,
   …, the total gas reward is as follows:

.. sourcecode:: bash

   G₁ ⋅ P₁ + G₂ ⋅ P₂ + G₃ ⋅ P₃ + …

Therefore, the total reward for creating a block is the following:

.. sourcecode:: bash

   (1 + 0.03125 ⋅ U ) ⋅ (5 ⋅ 0.8:superscript:`E`) + G₁ ⋅ P₁ + G₂ ⋅ P₂ + G₃ ⋅ P₃ + …

Here is a Python script that uses this mining reward formula to calculate
mining rewards:

.. sourcecode:: python

   #!/usr/bin/env python3

   BASE_INITIAL  = 5
   BASE_PERCENT  = 0.8
   UNCLE_PERCENT = 0.03125
   N_ERA_BLOCKS  = 5e6

   def mining_reward(block_number, num_uncles, gas_reqs, gas_prices):
           """
           Calculates mining rewards from block information.  The gas
           information must be provided in lists or tuples.  The gas
           prices must be in ETC.
           """

           era           = (block_number - 1) // N_ERA_BLOCKS
           base_reward   = (BASE_PERCENT ** era) * BASE_INITIAL
           uncle_reward  = UNCLE_PERCENT * base_reward
           uncle_rewards = num_uncles * uncle_reward
           gas_rewards   = 0
           for (gas_req, gas_price) in zip(gas_reqs, gas_prices):
                   gas_rewards += gas_req * gas_price

           return base_reward + uncle_rewards + gas_rewards

Here are some example calculations on real ETC blockchain data:

.. sourcecode:: python

   >>> mining_reward(5425392, 0, [], [])
   4.0
   >>> mining_reward(5423326, 1, [], [])
   4.125
   >>> mining_reward(5424471, 0, [36163, 36163] , [2e-8, 2e-8])
   4.00144652
   >>> mining_reward(5421363, 1, [21000, 21000, 21000, 21000, 21000], [5.5e-8, 2e-8, 2e-8, 1.6e-8, 1e-8])
   4.127541

The mining reward formula bounds the supply of ETC. Notice only the base and
uncle rewards increase the supply since the gas rewards just transfer existing
funds. Because the uncle rewards vary, the eventual total supply of ETC can only
be approximated.

The formula for the future increase in supply per era, assuming a constant
number of uncle blocks, is the following:

.. sourcecode:: bash

   5000000 ⋅ (1 + 2 ⋅ 0.03125 ⋅ U ) ⋅ (5 ⋅ 0.8:superscript:`E`)

The factor of 2 is necessary to include the uncle block creator rewards. The
total supply can be estimated from this formula by adding the contributions for
the remaining eras. Era 192, which will occur around the year 2474, is the last
era which increases the supply.

Assuming no more uncle blocks gives a lower bound of about 198.3 million
ETC. Assuming the maximum number of uncle blocks gives an upper bound of about
210.6 million ETC.
