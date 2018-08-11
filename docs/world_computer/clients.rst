.. _ch_clients:

Clients
================================================================================

To interact with the ETC world computer requires communicating with a computer
on the ETC network.  It is relatively easy to set up a computer to become part
of the network.  This requires the installation of an implementation of the ETC
communication protocols.  Possible choices include
`Geth <https://github.com/ethereumproject/go-ethereum>`_,
`Parity <https://github.com/paritytech/parity>`_
and `Mantis <https://github.com/input-output-hk/mantis>`_.
To use ETC, it is not necessary to set up a new computer on the
network. Applications can simply request information from other network
computers.  Such applications are referred to as *light clients*.  Whether using
a light client or setting up a full network computer, users can communicate with
the ETC network using Web 3.

.. _sec_web3:

--------------------------------------------------------------------------------
Web 3
--------------------------------------------------------------------------------

Web3 refers to a standard set of ETC application programming interfaces using
the Javascript Object Notation Remote Procedue Call (JSON RPC) protocol.  Web3
provides a convenient way to interact with ETC nodes and the ETC system.  The
name Web3 refers to the most ambitious goal for Ethereum Classic (ETC) which is
to replace the World Wide Web (Web). Blockchain based replacements for the Web
are often referred to as Web 3.0.

The Web was developed by Tim Berners-Lee and first made publicly available in
1991. It is a user friendly general purpose system based on the Internet.
Initially the Web mainly contained simple static content such as primitive
personal home pages. As the Web evolved, greater dynamism and interactivity was
possible such as with social media. This improved Web is often referred to as
Web 2.0. The term was popularized by Tim O’Reilly.

Neither the Internet nor the Web were initially designed to be trustless
systems. Components have been steadily introduced to improve security such as
Transport Layer Security (TLS), certificate authorities, and, Domain Name System
Security Extensions (DNSSEC). Unfortunately, many such improvements are only
partially adopted.

Gavin Wood popularized the term Web 3.0 for blockchain based trustless
alternatives to the Web. Confusingly, Web 3.0 also sometimes refers to the
Semantic Web.

Web 3.0 is a peer to peer replacement for the Web. A peer to peer architecture
is required to build trustless systems.  Web 3.0 users are pseudonymous. They
are only identified by their accounts, unlike the Web, where addresses can be
associated with identities.  ETC requires access to additional short and long
term storage systems to replace the Web. The InterPlanetary File System (IPFS)
is an example of a compelling peer to peer storage system that can integrate
with ETC.

The Web currently coexists with blockchain systems. Websites access these
systems to provide additional functionality. As ETC and related systems mature,
browsers will increasingly just point to these Web alternatives thus ushering in
the era of Web 3.0.
