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

# Cart 

## Cart Object

| Attribute | Type | Description |
|-----------|------|-------------|
|**cart_id** |integer |ID of the shopping cart|
|**product_list**|integer |List of products within the shopping cart|
|**user_id** |integer |Owner's id of the shopping cart|
|**complete** |boolean |False = current cart, True = history cart|

## Cart Transaction History Database

| Parameter | Type | Description |
|-----------|------|-------------|
|**cart_id** |integer |ID of the shopping cart|
|**user_id** |integer |Owner's id of the shopping cart|
|**product_id** |integer |ID of the product put into shopping cart|
|**quantity** |integer |Number of products selected|
|**complete** |boolean |False = current cart, True = history cart|

# API

## Endpoints

|Method|Endpoint/Request|Description|
|------|----------------|-----------|
|**POST**|   /api/v1/add| Add product item/s|
|**POST**|   /api/v1/remove| Remove product item/s|
|**POST**|   /api/v1/checkout|Checkout current shopping cart|
|**GET**|    /api/v1/users/:user_id/current_transaction/|Display active carts|
|**GET**|    /api/v1/users/:user_id/history_transaction/|Display carts that were checked out of given user|

## Requests and responses

Example of requests and responses are given for each endpoints:

### POST add or remove product item/s
Create new transaction on the basis of `product_id` and `quantity` parameter

**Add Example:** 
Endpoint: /api/v1/add
```
POST /api/v1/transactions
Content-type: application/json 
Accept: application/json
```
**Reponse to request:**
```
{
	"cart_id::555
	"user_id": 55
	"product id": "1",
	"quantity": "1",
	"complete": "False"
}
```

**Remove Example:** 
Endpoint: /api/v1/remove
```
POST /api/v1/transactions
Content-type: application/json 
Accept: application/json
```
**Reponse to request:**
```
{
	"cart_id": 555
	"user_id": 55
	"product id": "1",
	"quantity": "0",
	"complete": True"
}
```

### POST checkout shopping cart
Update `False` status of `complete` parameter of current cart to be `True` = PAID
Endpoint: /api/v1/checkout

**Example:** 

```
GET /api/v1/checkout
Content-type: application/json 
Accept: application/json
```
**Reponse to request:**
```
{
	"Current cart has been checked out."
}
```

### GET current shopping carts
Endpoint:  /api/v1/users/:user_id/current_transaction/

**Example:** Current user `id` = 2 

```
GET /api/v1/users/2/current_transaction/
Content-type: application/json 
Accept: application/json
```
**Reponse to request:**
```
{
  "current": [
    {
      "cart_id": "555",
	"user_id": "2",
	"product id": "1",
	"quantity": "1",
	"complete": False"
    }, 
    {
     "cart_id": "555",
	"user_id": "2",
	"product id": "1",
	"quantity": "3",
	"complete": False"
    }
  ]
}
```

### GET history shopping carts
Endpoint: /api/v1/users/:user_id/history_transaction/

**Example:**  Current user `id` = 2 

```
GET /api/v1/users/2/history_transaction
Content-type: application/json 
Accept: application/json
```
**Reponse to request:**
```
{
  "history": [
    {
     "cart_id": "555",
	"user_id": "2",
	"product id": "1",
	"quantity": "1",
	"complete": "True"
    }, 
    {
    "cart_id": "555",
	"user_id": "2",
	"product id": "1",
	"quantity": "3",
	"complete": "True""
    }
  ]
}
```
