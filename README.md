# Auction Site - Final Project

Final project for MPCS 51205 Aut 2020 from Team White Fifty Fifty 

## Frontend

Tech stack: HTML, CSS, JavaScript, Django, Redis 

### Install
Open `webserver` directory.

Creating and activating virtual environment (Optional)
```
virtualenv venv
source venv/bin/activate
```

Install and start Redis server on Mac
```
brew install redis
redis-server /usr/local/etc/redis.conf
```
* [Linux](https://redis.io/topics/quickstart)
* [Windows](https://www.onlinetutorialspoint.com/spring-boot/setup-install-redis-server-on-windows-10.html)

Navigate back to the `webserver` folder. Install requirements and make migrations
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### NOTE

Django will generate an sqlite database by default, but we are not using it to store any information.

## Backend

### Descrption
Based on python packages: Nameko, Flask, Pymongo, psycopg2, flasgger

### Run Services

1. Start Dockerized Services for Databases
```
//  RabbitMQ
docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
// MongoDB
docker run --hostname mongodb --name mongodb -p 27017:27017 -e MONGODB_PASS="password" -d mongo:3.4-xenial
// PostgreSQL
docker run -it -d --rm --name postgresql -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres
```

2. Populate Databases 
```
cd db
python create_dbs.py
```

3. Checkout Databases to ensure the data has been populated (Check if you want)
```
docker exec -it mongodb /bin/bash
mongo
use admin_db
db.admin.find()
// You should see the initial data in admin collection in the output
use user_db
db.user.find()
// You should see the initial data in user collection in the output
```

```
docker exec -it postgresql /bin/bash
psql -U dbuser -d item_db -h localhost
\d
select * from item;
```

4. Open and Check out API by using Swagger (might be dockerized later)
```
cd ../app
python api.py
```
Open http://localhost:5000/apidocs/#/ in the browser, you can see the explanations and JSON models for each API. Also you can input your own JSON to test.

5. Turn on microservices (can be dockerized on a container after things done)
```
cd ../service
nameko run user admin item auction shopping_cart login search notification
```

### Run Website
Open your browser and connect to http://localhost:8000


### Run Test for back-end
In the back-end, we have implemented the user and admin's business logic. To test, please 
```
cd ../test
pytest
```



## Version Updated

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
In the local, go under `/test` run pytest.

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
