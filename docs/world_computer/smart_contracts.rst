.. _ch_smart_contracts:

Smart Contracts
================================================================================

Smart contracts are autonomous software applications that manage agreements.
Agreements may be trivial or extremely complex.  An alternative equivalent term
is software *agents*.  Consider vending machines.  They specify and enforce
agreements to release various items for various payments.  They do not require
humans to operate.  Vending machine are therefore examples of smart contracts.
They notion of smart contracts was conceived by Nick Szabo and predates
blockchain technology:

   "A smart contract is a computerized transaction protocol that executes the
   terms of a contract. The general objectives of smart contract design are to
   satisfy common contractual conditions (such as payment terms, liens,
   confidentiality, and even enforcement), minimize exceptions both malicious
   and accidental, and minimize the need for trusted intermediaries. Related
   economic goals include lowering fraud loss, arbitration and enforcement
   costs, and other transaction costs."

           -- Nick Szabo, 1994

ETC makes an excellent smart contract platform.  ETC programs autonomously
manage countless agreements in a secure, reliable and trustless manner.  For
this reason ETC programs are referred to as smart contracts.

ETC smart contracts can read and write to their own storage as well as invoking
other smart contracts.  In this way, smart contracts can work to together to
provide increasingly sophisticated services.

Some, like Nick Szabo, envision smart contracts streamlining voluntary
contractual agreements and disrupting the legal profession.  Clearly software is
less prone to misunderstanding and ambiguity than spoken languages!  Others see
a future where complex smart contracts replace entire corporations.  Such
programs are referred to as *distributed autonomous enterprises (DAEs)*.  For
example, imagine a smart contract implementing a ride sharing service.  The
smart contract could bring riders and drivers together in an efficient flexible
manner.  Note that ETC smart contracts can not only make existing agreements
more efficient, but, they can also make possible contracts which previously were
not possible due to overhead costs.  For example, in addition to assisting
multinational corporations, ETC can help teenagers running a small business and
people providing microservices to third world countries.

Because the ETC world computer is implemented by a network of
computers, ETC smart contracts are also referred to as decentralized
applications, or *dapps* for short.

.. _sec_sc_langs:

--------------------------------------------------------------------------------
Smart Contract Languages
--------------------------------------------------------------------------------

Typically smart contracts are written in high level languages.  The
corresponding source code is compiled to the equivalent ETC virtual machine
instructions.  The most popular high level smart contract language is Solidity
although there are other possible choices such as Vyper.  Solidity is a
Javascript like language designed to be easily adopted by new developers.  Here
is a Solidity source code for a simple program that maintains a counter
variable.  The counter can be incremented by anyone but only the user account
that created the smart contract can reset the counter value:

.. sourcecode:: javascript

   pragma solidity ^0.4.18;

   /*
   This smart contract maintains a counter which anyone can increment but only
   the author can set to an arbitrary value.
   */

   contract Counter {
           uint    counter;
           address author;

           function Counter() public {
                   counter = 0;
                   author  = msg.sender;
           }

           function increment() public {
                   counter += 1;
           }

           function set(uint new_value) public {
                   if (msg.sender == author) {
                           counter = new_value;
                   }
           }

           function get_counter() public constant returns (uint) {
                   return counter;
           }
   }

Here is Solidity source code for a more complex program that implements a new
token:

.. sourcecode:: javascript

   pragma solidity ^0.4.18;

   /*
   Implements ChrisCoin which adheres to the Ethereum Token Standard.
   */

   contract ChrisCoin {
           string                                       name_;
           string                                       symbol_;
           uint                                         decimals_;
           uint                                         total_supply;
           mapping(address => uint)                     balance;
           mapping(address => mapping(address => uint)) approved;

           event Approve(address indexed  managed_add,
                         address indexed  manager_add,
                         uint             approv_amt);
           event Transfer(address indexed send_add,
                          address indexed receiv_add,
                          uint            trans_amt);

           function ChrisCoin() public {
                   /*
                   Sets the named constants and the initial balance(s).
                   */

                   name_               = "ChrisCoin";
                   symbol_             = "CHRC";
                   decimals_           = 18;
                   total_supply        = 21000000 * 10 ** decimals_;
                   balance[msg.sender] = total_supply;
           }

           function name() public constant returns (string) {
                   /*
                   Returns the cryptocurrency name.
                   */

                   return name_;
           }

           function symbol() public constant returns (string) {
                   /*
                   Returns the exchange ticker symbol.
                   */

                   return symbol_;
           }

           function decimals() public constant returns (uint) {
                   /*
                   Returns the maximum number of subdivision decimal places.
                   */

                   return decimals_;
           }

           function balanceOf(address account_add) public constant returns (uint) {
                   /*
                   Returns account balances.
                   */

                   return balance[account_add];
           }

           function allowance(address managed_add,
                              address manager_add)
                              public constant returns (uint) {
                   /*
                   Returns approved amounts.
                   */

                   return approved[managed_add][manager_add];
           }

           function approve(address manager_add,
                            uint approv_amt)
                            public constant returns (bool) {
                   /*
                   Returns approved amounts.
                   */

                   approved[msg.sender][manager_add] = approv_amt;
                   Approve(msg.sender, manager_add, approv_amt);

                   return true;
           }

           function valid(address send_add,
                          address receiv_add,
                          uint trans_amt)
                          public constant returns (bool) {
                   /*
                   Determines the validity of transfers.
                   */

                   bool valid_trans_amt  = trans_amt <= total_supply;
                   bool suff_send_bal    = balance[send_add] >= trans_amt;
                   uint receiv_bal       = balance[receiv_add] + trans_amt;
                   bool valid_receiv_bal = receiv_bal <= total_supply;

                   return valid_trans_amt && suff_send_bal && valid_receiv_bal;
           }

           function update_balance(address send_add,
                                   address receiv_add,
                                   uint    trans_amt)
                                   private {
                   /*
                   Updates balance with regards to tranfers.
                   */

                   balance[send_add]   -= trans_amt;
                   balance[receiv_add] += trans_amt;
           }

           function update_approved(address send_add, uint trans_amt) private {
                   /*
                   Updates approved with regards to tranfers.
                   */

                   approved[send_add][msg.sender] -= trans_amt;
           }

           function transfer(address receiv_add,
                             uint trans_amt)
                             public constant returns (bool) {
                   /*
                   Transfers funds between accounts.
                   */

                   bool result = false;
                   if (valid(msg.sender, receiv_add, trans_amt)) {
                           update_balance(msg.sender, receiv_add, trans_amt);
                           Transfer(msg.sender, receiv_add, trans_amt);
                           result = true;
                   }

                   return result;
           }

           function transferFrom(address send_add,
                                 address receiv_add,
                                 uint trans_amt)
                                 public constant returns (bool) {
                   /*
                   Transfers funds between accounts.
                   */

                   bool result     = false;
                   bool approv_amt = trans_amt <= approved[send_add][msg.sender];
                   if (valid(send_add, receiv_add, trans_amt) && approv_amt) {
                           update_balance(send_add, receiv_add, trans_amt);
                           update_approved(send_add, trans_amt);
                           Transfer(send_add, receiv_add, trans_amt);
                           result = true;
                   }

                   return result;
           }
   }

.. _sec_multisig:

--------------------------------------------------------------------------------
Multisig Smart Contracts
--------------------------------------------------------------------------------

Multisig smart contracts will likely be the dominant smart contract type in the
future. The security and other benefits are that compelling. I will describe
these smart contract types and scenarios where they are useful.

Malware, keyboard loggers and “man in the middle attacks” are just some of the
ways passwords can be stolen. Therefore, many use multifactor authentication to
increase security. For example, accessing a website from a laptop may require a
password and approval from a smartphone.

Ethereum Classic (ETC) and other smart contract systems can also benefit from
multifactor authentication. ETC users are associated with accounts. ETC account
authentication involves digital signatures. Therefore, ETC smart contracts
requiring multifactor authentication are referred to as multisig smart
contracts.

One of the most common types of multisig smart contracts requires digital
signatures from any two of three accounts. Here are some applications where this
is useful:

Single Individuals
   Imagine always requiring a digital signature from a laptop based account and
   a smartphone based account. To protect against the loss of either device,
   store the information for the third account in a secured paper wallet.

Online Shopping (Trusted Escrow)
   When purchasing products and services online, imagine buyers placing funds in
   multisig smart contracts. Have buyers and sellers each control an associated
   account. Allow an arbiter to control the third associated account. Notice
   buyers and sellers can together release funds without the arbiter. In the
   event of disagreements notice the arbiters can, together with buyers or
   sellers, release funds to the desired choices. This is referred to as trusted
   escrow because the arbiter does not control of any funds.

Small Businesses
   Imagine a small business controlling one associated account, and, a separate
   inspection service company controlling the second associated account. All
   transactions must be approved by the inspection service. To protect against
   issues with either account, store the information for the third associated
   account in a secured paper wallet.

Here are two more multisig smart contract types and applications:

Majority Rule
   Imagine all members of a group controlling separate associated
   accounts. Always require digital signatures from any majority of the
   accounts. This would implement a majority rule arrangement.

Unanimity Rule
   Imagine all members of a group controlling separate associated
   accounts. Always require digital signatures from all of the accounts. This
   would implement a unanimity rule arrangement.

There are currently no ETC multisig smart contract standards. However, open
source templates are available such as from the OpenZeppelin project.

There are several common scenarios where multisig smart contracts are useful and
significantly increase security. Therefore, it is likely they will take over ETC
and the world.
