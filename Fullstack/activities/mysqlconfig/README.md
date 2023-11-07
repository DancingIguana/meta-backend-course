# MySQL Config Quick Setup

1. Install `mysqlclient` and `pymysql`:
```
pip install mysqlclient
pip install pymysql
```

2. Connect to the MySQL server from the terminal
```
mysql -u root -p
```
Or specify the host (default is localhost)
```
mysql -u root -h 127.0.0.1 -p
```
Or if MySQL is running in a different number from 3306, specify the port number
```
mysql -u root -P 3307 -p
```

3. Create a databse in mysql:
```
create database littlelemon;
```

4. Exit MySQL:
```
exit
```

5. Configure the django project:

In the project's `__init__.py` add the following:
```py3
import pymysql

pymysql.install_as_MySQLdb()
```
In `settings.py`
`

In the project's settings update `DATABASES` with the following:
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "littlelemon",
        "HOST": "localhost", # Or the specified host address for mysql (127.0.0.1 for example)
        "USER": "db_username", 
        "PASSWORD": "db_password", #
        "PORT": "3306",  # Or the specified port
    }
}
```

6. Perform the migrations

```
python3 manage.py makemigrations
python3 manage.py migrate
```

7. Check changes in database:
Login to mysql with the corresponding user and password and run:
```
use littlelemon;
show tables;
```
You should see all the django tables in there.