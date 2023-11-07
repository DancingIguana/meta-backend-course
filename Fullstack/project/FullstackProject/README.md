Important: `mysqlclient` by itself didn't work in my device, so it's important to install `pymysql`:
```
pip install pymysql
```

Also, the configuration is in MySQL, so check that the database name, user and password match with the ones in your system. This can be updated/checked in the `littlelemon/settings.py`