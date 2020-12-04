# Auction Site - Final Project

Final project for MPCS 51205 Aut 2020 from Team 4 - White Fifty Fifty 

### Frontend

Tech stack: HTML, CSS, JavaScript, Django, Redis 

Note: Django will generate an sqlite database by default, but we are not using it to store any information.

### Backend
Based on python packages: pika, Flask, Pymongo, psycopg2, flasgger

## Steps to run up systems
### Generate containers by order
Please ensure you are not running any containers now.

```
// RabbitMQ
docker run -d --hostname my-rabbit --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management

// Flask APIs
docker run -d --name apis -p 5000:5000 -v /Users/yinghuamo/Documents/GitHub/Final-Project:/Final-Project ymo1997/service_with_mongodb

// 8 Microservices
docker run -d --name user_service -v /Users/yinghuamo/Documents/GitHub/Final-Project:/Final-Project ymo1997/service_with_mongodb
docker run -d --name admin_service -v /Users/yinghuamo/Documents/GitHub/Final-Project:/Final-Project ymo1997/service_with_mongodb
docker run -d --name item_service -v /Users/yinghuamo/Documents/GitHub/Final-Project:/Final-Project ymo1997/service_with_postgresql
docker run -d --name auction_service -v /Users/yinghuamo/Documents/GitHub/Final-Project:/Final-Project ymo1997/service_with_postgresql
docker run -d --name shopping_cart_service -v /Users/yinghuamo/Documents/GitHub/Final-Project:/Final-Project ymo1997/service_with_postgresql
docker run -d --name notification_service -v /Users/yinghuamo/Documents/GitHub/Final-Project:/Final-Project ymo1997/service_with_postgresql
docker run -d --name search_service -v /Users/yinghuamo/Documents/GitHub/Final-Project:/Final-Project ymo1997/service_with_postgresql
docker run -d --name login_service -v /Users/yinghuamo/Documents/GitHub/Final-Project:/Final-Project ymo1997/service_with_postgresql

// Web-server
docker run -d --name web_server -p 8000:8000 -v /Users/yinghuamo/Documents/GitHub/Final-Project:/Final-Project ymo1997/web_server

```
### Start services
New a terminal for container `apis`
```
docker exec -it apis bash
python3 Final-Project/service/api.py
```

New a terminal for container `user_service`
```
docker exec -it user_service bash
python3 Final-Project/db/populate_user_db.py 
python3 Final-Project/service/user.py 
``` 

New a terminal for container `admin_service`
```
docker exec -it admin_service bash
python3 Final-Project/db/populate_admin_db.py 
python3 Final-Project/service/admin.py 
``` 

New a terminal for container `item_service`
```
docker exec -it item_service bash
python3 Final-Project/db/populate_item_db.py 
python3 Final-Project/service/item.py 
``` 

New a terminal for container `auction_service`
```
docker exec -it auction_service bash
python3 Final-Project/db/populate_auction_db.py 
python3 Final-Project/service/auction.py 
``` 

New a terminal for container `shopping_cart_service`
```
docker exec -it shopping_cart_service bash
python3 Final-Project/db/populate_shopping_cart_db.py 
python3 Final-Project/service/shopping_cart.py 
``` 

New a terminal for container `notification_service`
```
docker exec -it notification_service bash
python3 Final-Project/db/populate_notification_db.py 
python3 Final-Project/service/notification.py 
``` 

New a terminal for container `search_service`
```
docker exec -it search_service bash
python3 Final-Project/db/populate_search_db.py 
python3 Final-Project/service/search.py 
``` 

New a terminal for container `login_service`
```
docker exec -it login_service bash
python3 Final-Project/service/login.py 
``` 

### Run pytest
http://localhost:5000/apidocs/#/ for APIs Description

Locally, go under `/test` run pytest.

### Website Demo

New a terminal for container `web_server`
```
docker exec -it web_server bash
sudo service redis-server start
python3 Final-Project/webserver/manage.py makemigrations
python3 Final-Project/webserver/manage.py migrate
python3 Final-Project/webserver/manage.py runserver 0.0.0.0:8000
``` 

Locally, open browser for http://localhost:8000
