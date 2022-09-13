# mysql-db-backup

backup DB mysql table and send report success to Telegram Bot

required
--------
install prettytable
```sh
python -m pip install -U prettytable
```

You can install it with pip:
```python
python3 -m pip install PyMySQL
```

for telegram
```python
python -m pip install requests
```

Example
-------
you can run for backup

copy data 1 table
```python
python3 main.py -t tablename
```
copy data many tables
```python
python3 main.py -t tablename1,tablename2,tablename3,tablename4,tablename5
```