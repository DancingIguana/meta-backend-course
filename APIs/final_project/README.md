# Little Lemon API
## About
This is the final project of the API course in django from Meta's Backend Software Engineer certification.

## How to use
### User roles
Here, we have 4 types of users:
- **Admin**: Can get, create, delete and update the following things:
    1. Categories
    2. Menu items
    3. Users
    4. User groups
    5. Orders (update fields of delivery_crew and status)
- **Manager**: Can get, create, and update the following:
    1. Menu items
    2. User groups (get, assign or remove people from "Manager" or "Delivery crew" groups)
    3. Orders (update fields of delivery_crew and status)
- **Delivery crew**: Can only do the following:
    1. Menu items
    2. Orders (only can get, and update the status field of the orders where they have been assigned)
- **Customer**: a user that's authenticated but doesn't belong to any group. Can do the following:
    1. Get the menu items
    2. Add items to a cart by specifying menu item id, and quantity.
    3. Post an order that empties the user's cart automatically. Automatically it assigns the date and total price, the delivery crew and status are set to None and default respectively when posted.


### User registration and token generation endpoints
These endpoints are created with djoser. They're the following
| Endpoint               | Role                                      | Method | Description                                                                 |
|------------------------|-------------------------------------------|--------|-----------------------------------------------------------------------------|
| `/api/users`           | No role required                          | `POST` | Create a new user with name, email and password                             |
| `/api/users/users/me/` | Anyone with a valid user token            | `GET`  | Displays only the current user                                              |
| `/api/token/login`     | Anyone with a valid username and password | `POST` | Generates access tokens that can be used in other API calls in this project |


### Category
There are three categories: *Appetizers*, *Desserts* and *Main*. Al authenticated users can see them, but only the admin can perform changes.

| Endpoint                       | Role                                    | Method      | Description                |
|--------------------------------|-----------------------------------------|-------------|----------------------------|
| `/api/category`                | Customer, Delivery crew, Manager, Admin | `GET`       | Lists all the categories.  |
| `/api/category/`               | Admin                                   | `POST`      | Creates a new category.    |
| `/api/category/{categoryId}`   | Customer, Delivery crew, Manager, Admin | `GET`       | Lists a single category.   |
| `/api//{categoryId}`           | Admin                                   | `PUT,PATCH` | Updates a single category  |
| `/api/category/{categoryId}`   | Admin                                   | `DELETE`    | Deletes a single category. |

### Menu-items endpoints
These endpoints are related to the available menu items in the database.

| Endpoint                       | Role                                    | Method      | Description                |
|--------------------------------|-----------------------------------------|-------------|----------------------------|
| `/api/menu-items`              | Customer, Delivery crew, Manager, Admin | `GET`       | Lists all menu items.      |
| `/api/menu-items/`             | Manager, Admin                          | `POST`      | Creates a new menu item.   |
| `/api/menu-items/{menuItemId}` | Customer, Delivery crew, Manager, Admin | `GET`       | Lists a single menu item.  |
| `/api/menu-items/{menuItemId}` | Manager, Admin                          | `PUT,PATCH` | Updates a single menu item |
| `/api/menu-items/{menuItemId}` | Manager, Admin                          | `DELETE`    | Deletes a single menu item |

Also, it's possible to apply ordering and filtering in the first of these endpoints. You can order by `price`, search by an item's `title` or filter by `category`.

**Examples**
* `api/menu-items/?search=Bruschetta`: lists the menu items with the word Bruschetta in its `title` .
* `api/menu-items/?category=Main`: lists all the menu items in the Main `category`.
* `api/menu-items/?ordering=-price`: lists all the menu items sorted in descending order by `price`.

### User group management endpoints
These endpoints are for the managers and admin to see, and update the user groups from the organization.

| Endpoint                                   | Role           | Method   | Description                                                              |
|--------------------------------------------|----------------|----------|--------------------------------------------------------------------------|
| `/api/groups/manager/users`                | Manager, Admin | `GET`    | Lists all the managers.                                                  |
| `/api/groups/manager/users`                | Manager, Admin | `POST`   | Assigns an user to the manager group. Either by using 'id' or 'username' |
| `/api/groups/manager/users/{userId}`       | Manager, Admin | `DELETE` | Removes this user from the manager group.                                |
| `/api/groups/delivery-crew/users`          | Manager, Admin | `GET`    | Lists all the delivery crew.                                             |
| `/api/groups/delivery-crew/users/{userId}` | Manager, Admin | `DELETE` | Removes this user from the delivery crew.                                |

### Cart management endpoints
These endpoints are exclusive for the cart. Each customer has their own cart.
| Endpoint                            | Role     | Method       | Description                                                                                     |
|-------------------------------------|----------|--------------|-------------------------------------------------------------------------------------------------|
| `/api/cart/menu-items`              | Customer | `GET`        | Returns the current items in the user's cart for the current user token.                        |
| `/api/cart/menu-items`              | Customer | `POST`       | Adds the menu item to the user's cart. Sets the authenticated user as the user id for the item. |
| `/api/cart/menu-items`              | Customer | `DELETE`     | Deletes all the menu items created by the current user from the user's cart.                    |
| `/api/cart/menu-items/{cartItemId}` | Customer | `PUT, PATCH` | Edits the menu item or quantity of an item in the user's cart.                                  |
| `/api/cart/menu-items/{cartItemId}` | Admin    | `DELETE`     | Deletes this menu item from the user's cart.                                                    |

### Order Management endpoints
These endpoints are for keeping track of the orders performed whenever the customers post them.

| Endpoint                | Role           | Method       | Description                                                                                                                                                                                       |
|-------------------------|----------------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/api/orders`           | Customer       | `GET`        | Returns all the orders with the order items created by the user.                                                                                                                                  |
| `/api/orders`           | Customer       | `POST`       | Creates a new order item for the current user. Gets current cart items from the cart endpionts and adds those items to the order items table. Then deletes all items from the cart for this user. |
| `/api/orders/{orderId}` | Customer       | `GET`        | Returns all the menu items for this order ID.                                                                                                                                                     |
| `/api/orders`           | Manager, Admin | `GET`        | Returns all orders with order items by all users                                                                                                                                                  |
| `/api/orders/{orderId}` | Manager, Admin | `PUT, PATCH` | Updates the `delivery_crew` or `status` field in the order                                                                                                                                        |
| `/api/orders/`          | Delivery crew  | `GET`        | Returns all orders assigned to this delivery crew.                                                                                                                                                |
| `/api/orders/{orderId}` | Delivery crew  | `PUT, PATCH` | Updates only the `status` field in the order.                                                                                                                                                     |

Like in `Menu Items`, it's possible to apply ordering and filtering to the orders. 
**Examples**
* `api/orders/?ordering=total`: Order in ascending order by total price of the order
* `api/orders/?user_id=10`: List all the orders done by user with id 10
* `api/orders/?user_username=customer1`: List all the orders done by user `customer1`.
* `api/order/?delivery_crew_id=5`: List all the orders assigned to delivery crew user with id 5.
* `api/orders/?delivery_crew_username=delivery1`: List all the orders assigned to delivery crew with user `delivery1`-
* `api/orders/?status=1`: List all the orders with a status of 1 (completed).


## Throttling
This API has throttling implemented. For authenticated users there are 10 calls per minute and for non-authenticated users 5 per minute.


## Users and passwords

### Admin
| Username | mail               | password | token                                   |
|----------|--------------------|----------|-----------------------------------------|
| admin    | admin@little.lemon | admin    |7d5cbc6c8363022cfd3f3e9c884a9f363fb03cbb |



### Managers
| Username | mail                  | password | token
|----------|-----------------------|----------|----------------------------------------|
| manager1 | manager1@little.lemon | 0secret1 |9414fc0290b81828b6bcf2cf9a93584d4eacb89b|
| manager2 | manager2@little.lemon | 0secret1 |fba6098b4c425305813e65d55331dceeeed152b3|
| delivery1| delivery1@little.lemon| 0secret1 |23d8612f595026314a54804506112219191b630c|
| delivery2| delivery2@little.lemon| 0secret1 |8c26c072ec18e2f533753862b3f0ae85b57b31ec|



## Customers 

| Username | mail                  | password        | token
|----------|-----------------------|-----------------|----------------------------------------|
| customer1| customer1@email.com   | secretpassword1 |dd9821310732f26923b515a82521b1f280e77b47|
| customer2| customer2@email.com   | secretpassword1 |f3bc76179a5a058bc7705fa1bd2169f8b1ab908e|
