.. image:: https://readthedocs.org/projects/windtalker/badge/?version=latest
    :target: http://windtalker.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://travis-ci.org/MacHu-GWU/windtalker-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/windtalker-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/windtalker-project/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/windtalker-project

.. image:: https://img.shields.io/pypi/v/windtalker.svg
    :target: https://pypi.python.org/pypi/windtalker

.. image:: https://img.shields.io/pypi/l/windtalker.svg
    :target: https://pypi.python.org/pypi/windtalker

.. image:: https://img.shields.io/pypi/pyversions/windtalker.svg
    :target: https://pypi.python.org/pypi/windtalker

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/windtalker-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: http://windtalker.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: http://windtalker.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: http://windtalker.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/windtalker-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/windtalker-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/windtalker-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/windtalker#files


Welcome to ``windtalker`` Documentation
==============================================================================

In World War II, US Marine specially recruited a lots of bilingual Navajo speakers to serve in their standard communications units in the Pacific Theater. These Navajo transmitted tactical messages over military telephone or radio communications nets using formal or informally developed codes built upon their native languages. These people, we call them --- **Wind Talker**

``windtalker`` is a utility tools built on top of `cryptography <https://pypi.python.org/pypi/cryptography>`_ and `rsa <https://pypi.python.org/pypi/rsa>`_. With this, **you can encrypt/decrypt binary data, text, files or even a entire directory in single line of code**! It support both symmetry and asymmetry encryption algorithm. For usage, you should start from `HERE <https://windtalker.readthedocs.io/index.html#table-of-content>`_

Example (SymmtricCipher):

.. code-block:: python

    >>> from windtalker import SymmetricCipher
    >>> c = SymmetricCipher(password="password") # Fernet encrypter
    >>> c.encrypt_text("Hello")
    Z0FBQUFBQlo0VHpVVjdWR0xCb0VEc0dMVUxib25jZEwzTWZ1UC1raFVmWndwNERrTmZVR1hNdzE3ZS05RWkwWXBrTi1adUhRWTNWYkxUT1Vkekh3MlVVcHZXLWxaMWMyOEE9PQ==

    >>> c.encrypt_file(r"C:\test.py") # c.decrypt_file(xxx) for decryption
    C:\test-encrypted.py

    >>> c.encrypt_dir(r"C:\User\Admin\Document") # c.decrypt_dir(xxx) for decryption
    C:\User\Admin\Document-encrypted.py

**HARDCODE YOUR PASSWORD IN YOUR CODE IS DANGEROUS!**:

You can create a ``.windtalker`` text file in your ${HOME} directory. and put your secret password in it. ``windtalker.SymmetricCipher`` can automatically read password from it.

${HOME} directory:

- Windows: C:\Users\<username>
- MacOS: /Users/<username>
- Linux: /home/<username>

For more features and how to use RSA to encrypt your file or directory, please read `THIS <https://windtalker.readthedocs.io/index.html#table-of-content>`_


.. _install:

Install
------------------------------------------------------------------------------

``windtalker`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install windtalker

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade windtalker
