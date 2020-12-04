# Auction Site - Final Project

Final project for MPCS 51205 Aut 2020 from Team 4 - White Fifty Fifty 

### Frontend

Tech stack: HTML, CSS, JavaScript, Django, Redis 

Note: Django will generate an sqlite database by default, but we are not using it to store any information.

### Backend
Based on python packages: pika, Flask, Pymongo, psycopg2, flasgger

## Steps to run up the system
### Generate containers by order
#### Please ensure you are not running any containers now and create the container by order.

```
// RabbitMQ
docker run -d --hostname my-rabbit --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management

// Flask APIs
docker run -d --name apis -p 5000:5000 ymo1997/service_with_mongodb

// 8 Microservices
docker run -d --name user_service ymo1997/service_with_mongodb
docker run -d --name admin_service ymo1997/service_with_mongodb
docker run -d --name item_service ymo1997/service_with_postgresql
docker run -d --name auction_service ymo1997/service_with_postgresql
docker run -d --name shopping_cart_service ymo1997/service_with_postgresql
docker run -d --name notification_service ymo1997/service_with_postgresql
docker run -d --name search_service ymo1997/service_with_postgresql
docker run -d --name login_service ymo1997/service_with_postgresql

// Web-server
docker run -d --name web_server -p 8000:8000 ymo1997/web_server

```
### Start services
New a terminal for container `apis`
```
docker exec -it apis bash
cd Final-Project
git pull
python3 service/api.py
```

New a terminal for container `user_service`
```
docker exec -it user_service bash
cd Final-Project
git pull
python3 db/populate_user_db.py 
python3 service/user.py 
``` 

New a terminal for container `admin_service`
```
docker exec -it admin_service bash
cd Final-Project
git pull
python3 db/populate_admin_db.py 
python3 service/admin.py 
``` 

New a terminal for container `item_service`
```
docker exec -it item_service bash
cd Final-Project
git pull
python3 db/populate_item_db.py 
python3 service/item.py 
``` 

New a terminal for container `auction_service`
```
docker exec -it auction_service bash
cd Final-Project
git pull
python3 db/populate_auction_db.py 
python3 service/auction.py 
``` 

New a terminal for container `shopping_cart_service`
```
docker exec -it shopping_cart_service bash
cd Final-Project
git pull
python3 db/populate_shopping_cart_db.py 
python3 service/shopping_cart.py 
``` 

New a terminal for container `notification_service`
```
docker exec -it notification_service bash
cd Final-Project
git pull
python3 db/populate_notification_db.py 
python3 service/notification.py 
``` 

New a terminal for container `search_service`
```
docker exec -it search_service bash
cd Final-Project
git pull
python3 db/populate_search_db.py 
python3 service/search.py 
``` 

New a terminal for container `login_service`
```
docker exec -it login_service bash
cd Final-Project
git pull
python3 service/login.py 
``` 

### Run pytest
Check out http://localhost:5000/apidocs/#/ for APIs Description

Locally, go under `/test` run pytest.

### Website Demo

New a terminal for container `web_server`
```
docker exec -it web_server bash
sudo service redis-server start
cd Final-Project
git pull
python3 webserver/manage.py makemigrations
python3 webserver/manage.py migrate
python3 webserver/manage.py runserver 0.0.0.0:8000
``` 

Locally, open browser for http://localhost:8000 to check out our website
