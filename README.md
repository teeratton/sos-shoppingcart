SOS Shopping Cart API
=====================
This API for shopping cart provides a selection of endpoints for interacting with backend mechanics for an online shopping website's cart as a micro-service, with cart transaction history database. We utiltize continious integration (CI) and continuous deployment (CD) through Travis CI and Heroku. 

## List of requirements:

- Update a shopping cart (add/remove)
- Check out (Complete purchase of all products in current shopping cart)
- Display history and current shopping carts of each user

# Contents

- [Generals](#generals)
  - [Hello World](#hello)
  - [Authentication - Authorization](#auth)
- [Cart](#cart) 
  - [Cart Object](#obj)
  - [Cart Transaction History Database](#db)
- [API](#api)
  - [Endpoints](#endpts)
  - [Requests and responses](#req)
    - [POST add product items](#add)
    - [POST remove product items](#remove)
    - [POST checkout shopping cart](#checkout)
    - [GET current shopping carts](#current)
    - [GET history shopping carts](#history)
 
## Hello World 
Our SOS shopping cart is deployed through heroku at: 
```
https://sos-shoppingcart.herokuapp.com/
```
You can try send a `GET` request to the endpoint. You should see the following JSON message:
```
"Welcome to the shopping cart and cart transaction database API!"
```
If you look at the header, you should see that the content-type is json:
```
Content-Type: application/json
```

## Authentication - Authorization
Authorization functionality is provided by a separate, web front-end, micro-service. Therefore, a JWT token is provided by front-end microservice and included in the Authorization header in all HTTP requests. 

# Transaction 

## Transaction Object

| Attribute | Type | Description |
|-----------|------|-------------|
|**user_id** |integer |Owner's id of the shopping cart|
|**product_list**|integer |product's the shopping cart|
|**quantity** |boolean |quantity of the product|
|**complete** |boolean |False = current cart(not paid), True = history cart(paid)|

## Cart Transaction History Database

| Parameter | Type | Description |
|-----------|------|-------------|
|**transaction_id** |integer,pk |ID of the shopping cart|
|**user_id** |integer |Owner's id of the shopping cart|
|**product_id** |integer |ID of the product put into shopping cart|
|**quantity** |integer |Number of products selected|
|**complete** |boolean |False = current cart, True = history cart|

# API

## Endpoints

|Method|Endpoint/Request|Description|
|------|----------------|-----------|
|**POST**|   /api/v1/add_transaction| Add product to cart|
|**POST**|   /api/v1/change_quantity| Change quantity of product in the cart|
|**DELETE**| /api/v1/delete_transaction| Remove product from the cart|
|**POST**|   /api/v1/checkout|Checkout current shopping cart|
|**GET**|    /api/v1/users/:user_id/current_transaction/|Display active carts|
|**GET**|    /api/v1/users/:user_id/history_transaction/|Display carts that were checked out of given user|

## Requests and responses

Example of requests and responses are given for each endpoints:

### POST add transaction
Create new transaction on the basis of `product_id` and `quantity` parameter

## Add product to cart
```
POST /api/v1/add_transaction
Content-type: application/json 
Accept: application/json
```
**Request body:**
```
{
	"user_id": 55
	"product id": "1",
	"quantity": "1",
}
```

## POST Change quantity
Change quantity inside a shopping cart of a product item
```
POST /api/v1/change_quantity
Content-type: application/json 
Accept: application/json
```
**Request body:**: This will update the quantity of production_id 1 and user_id 55 to 1
```
{
	"user_id": 55,
	"product id": "1",
	"quantity": "1"
}
```

## DELETE transaction of a product from cart 
```
POST /api/v1/delete_transaction
Content-type: application/json 
Accept: application/json
```
**Request body:**: This will delete the product_id 1 from user_id55's cart
```
{
	"user_id": 55,
	"product id": "1"
}
```

## POST Checkout shopping cart
Update `False` status of `complete` parameter of current cart to be `True` = PAID
Endpoint: /api/v1/checkout
```
POST /api/v1/checkout
Content-type: application/json 
Accept: application/json
```
**Request body:** This will update all current transaction of given user_id to 'True' = PAID
```
{
	"user_id": 55
}
```

## GET current shoppingcart
Endpoint:  /api/v1/users/:user_id/current_transaction/

**Example:** Current user `id` = 3 

```
GET /api/v1/users/3/current_transaction/
Content-type: application/json 
Accept: application/json
```
**Response body:**
```
[
	{"user_id" : 3,
		"product_id": 5,
		"quantity": 10}, 
	{"user_id" : 3,
		"product_id: 10, 
		"quantity" : 3}
]
```

## GET history shopping carts
Endpoint: /api/v1/users/:user_id/history_transaction/

**Example:**  Current user `id` = 2 

```
GET /api/v1/users/2/history_transaction
Content-type: application/json 
Accept: application/json
```
**Response:**
```
[
	{"user_id" :2 , 
		"product_id": 10, 
		"quantity": 2}, 
	{"user_id" : 2, 
		"product_id: 20, 
		"quantity" : 10}
]
```
