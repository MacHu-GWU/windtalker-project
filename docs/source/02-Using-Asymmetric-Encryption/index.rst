.. _asymmetric:

Using asymmetric encryption
===============================================================================
All symmetric encryption algorithm has a inevitable problem. It's very hard to find a **ONE HANDRED PERCENT SAFE WAY to send your secret key to your receiver**. Asymmetric encryption doesn't have this problem. If you don't familiar with asymmetric encryption algorithm, you may need to figure out the basic idea of **why it's safe to use public key for encryption, and how to sign your message to avoid mid-man attack**; Read this: https://en.wikipedia.org/wiki/RSA_(cryptosystem)

Now, let's take a look at how it's done in this example. You want to send a encrypted message to your friend **Bob** using a unsafe channel.


Encrypt/Decrypt a Message
-------------------------------------------------------------------------------
**Generate a key pair**:

For demonstration purpose, you are the **A**, and your friend Bob is **B**. First, you both need to generate a private-public key pair, and share your own public key to each other. There's no problem if public key exposed to others::

	>>> from windtalker.asymmetric import AsymmetricCipher
	>>> A_pubkey, A_privkey = AsymmetricCipher.newkeys() # send A_pubkey to Bob
	>>> B_pubkey, B_privkey = AsymmetricCipher.newkeys() # get B_pubkey from Bob

**Encrypt and Decrypt**:

This code is a view from your side::

	>>> message = "Turn right at blue tree"
	>>> cipherA = AsymmetricCipher(A_pubkey, A_privkey, B_pubkey)
	>>> token = cipherA.encrypt_text(message)
	>>> sign = cipherA.sign

And then send ``token`` and ``sign`` to your friend **Bob**. From **Bob**'s point of view, it looks like::

	>>> cipherB = AsymmetricCipher(B_pubkey, B_privkey, A_pubkey)
	>>> original_message = cipherB.decrypt(token, signature=sign)


Work with files and directory
-------------------------------------------------------------------------------
Asymmetric encryption algorithm works slow. A widely used solution is to encrypt your files with :ref:`Symmetric Encryption <symmetric>`, and then use asymmetric encryption to encrypt your secret key of symmetric encryption.
