.. _extend-windtalker:

Create a new cipher using your own algorithm
===============================================================================
You can design your own encryption algorithm (**Even though I don't recommend to**) for fun. With ``windtalker``, you only need to write minimal code, and then it works for any type of encryption in text, files and also directory. This is how:

.. code-block:: python

    class YourCipher(BaseCipher):
        def __init__(self, *args, *kwargs):
            """Your setup method, like prepare a secret key.
            """

        def encrypt(self, binary, *args, **kwargs):
            """This method will encrypt a binary data to encrypted.
            """

        def decrypt(self, binary, *args, **kwargs):
            """This method will decrypt a binary data to original.
            """

After that:

- :meth:`~windtalker.cipher.BaseCipher.encrypt_text`
- :meth:`~windtalker.cipher.BaseCipher.decrypt_text`
- :meth:`~windtalker.cipher.BaseCipher.encrypt_file`
- :meth:`~windtalker.cipher.BaseCipher.decrypt_file`
- :meth:`~windtalker.cipher.BaseCipher.encrypt_dir`
- :meth:`~windtalker.cipher.BaseCipher.decrypt_dir`

will automatically work.
