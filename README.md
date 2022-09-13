# mysql-db-backup

required
--------
install prettytable
```sh
    python -m pip install -U prettytable
```

You can install it with pip:
.. code:: python
    python3 -m pip install PyMySQL

for telegram
.. code:: python
    python -m pip install requests

Example
-------
copy data 1 table
.. code:: python
    python3 main.py -t tablename

copy data many tables
    .. code:: python
    python3 main.py -t tablename1,tablename2,tablename3,tablename4,tablename5