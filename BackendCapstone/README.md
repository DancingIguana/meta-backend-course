# Back-End Developer Capstone
This is the repository for the final project of the Meta's Back-End Specialization in Coursera.

## About
This project is a restaurant web application and API that uses Django as its back-end. Its main features are:
- A restaurant main webpage
- API Endpoints that allow:
  * Registering and logging in to the app based on Token registration.
  * Getting and updating the restaurant's menu depending on your authentication.
  * Posting and updating table reservations depending on your authentication.

**Note**: The database is configured for MySQL and it's only possible to use a database of your own when testing this project.

## How to use
Install the dependencies

```
pip install requirements.txt
```

Configure your database with your data under `littlelemon/settings.py/`:
```py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "LittleLemon",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

Run the necessary migrations:

Go to the `/littlelemon/` directory in the terminal and run the migrations for the database:
```
python3 manage.py  makemigrations
python3 manage.py migrate
```


Create a superuser for testing:
```
django-admin createsuperuser
```

Run the server
```
python3 manage.py runserver
```
Visit your localhost in the browser:

- Main app: [http://127.0.0.1:8000/restaurant](http://127.0.0.1:8000/restaurant) 
- Django admin (with superuser data): [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) 

## API Endpoints
Here are the following API endpoints:

### Restaurant Menu
| Endpoint                                   | Role           | Method   | Description                                                              |
|--------------------------------------------|----------------|----------|--------------------------------------------------------------------------|
| `/restaurant/menu` | Anyone | `GET`    | Lists all the menu items.    |
| `restaurant/menu/{menuItemId}` | Anyone | `GET`   | Displays the data of a particular menu item. |
| `restaurant/menu` | Authenticated user | `POST` | Posts a menu item.  |
| `/restaurant/menu/{menuItemId}` | Authenticated user | `PUT`, `PATCH`, `DELETE` | Update or delete a specific menu item. |

### Table booking
| Endpoint                                   | Role           | Method   | Description                                                              |
|--------------------------------------------|----------------|----------|--------------------------------------------------------------------------|
| `/restaurant/booking/tables` | Authenticated user | `GET`    | Lists all the bookings.    |
| `restaurant/booking/tables/{tableId}` | Authenticated user | `GET`   | Displays the data of a particular booking. |
| `restaurant/booking/tables/` | Authenticated user | `POST` | Posts a booking.  |
| `/restaurant/booking/tables/{tableId}` | Authenticated user | `PUT`, `PATCH`, `DELETE` | Update or delete a specific booking. |

### User authentication
| Endpoint                                   | Role           | Method   | Description                                                              |
|--------------------------------------------|----------------|----------|--------------------------------------------------------------------------|
| `/restaurant/api-token-auth` | Anyone | `POST`    | Given an 'username' and 'password' of an existing user, generate the corresponding Authentication Token.    |
| `/auth/users/` | Authenticated user | `GET`   | Lists all the registered users in the application. |
| `/auth/users/{username}` | Authenticated user | `GET` | Displays the data of a particular user.  |
| `/auth/users/` | Authenticated user | `POST` | Create a new user. |
| `/auth/users/{username}` | Authenticated user | `PUT`, `PATCH`, `DELETE` | Update or delete a registered user. |


## Screenshots

Main site:
![home_page](https://github.com/DancingIguana/meta-backend-course/blob/main/BackendCapstone/imgs/main_site.png)

Menu API:

![home_page](https://github.com/DancingIguana/meta-backend-course/blob/main/BackendCapstone/imgs/menu.png)

Single Menu Item API:

![menu_item](https://github.com/DancingIguana/meta-backend-course/blob/main/BackendCapstone/imgs/menu_item.png)

User API:

![users](https://github.com/DancingIguana/meta-backend-course/blob/main/BackendCapstone/imgs/users.png)

Single User API:

![single_user](https://github.com/DancingIguana/meta-backend-course/blob/main/BackendCapstone/imgs/edit_user.png)

Authentication token generation

![token_generation](https://github.com/DancingIguana/meta-backend-course/blob/main/BackendCapstone/imgs/token_generation.png)