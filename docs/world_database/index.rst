.. _part_wd:

World Database (Blockchain)
================================================================================

The world database stores requests sent to the world computer.  These requests
are referred to as *transactions*.  The transactions are collected into sets
referred to as *blocks*.  The blocks form a tree and a single path through that
tree defines the *blockchain*.  The blockchain stores other information in
addition to transactions such as transaction *logs*.  Lastly, process of
creating, verifying and adding new blocks to the blockchain is referred to as
*mining*.

The blockchain distributed database architecture was first introduced to the
world in the Bitcoin system.

.. toctree::
   transactions
   blocks
   logs
   mining
