# Final Project

Final project for MPCS 51205 Aut 2020 from Team White Fifty Fifty 

## Descrption
Based on python packages: Nameko, Flask, Pymongo, psycopg2, flasgger

## Run Project
1. Clone this git
2. Open a console and install python packages
```
pip install Nameko
pip install Flask
pip install Pymongo
pip install psycopg2
pip install flasgger
```

3. Start Dockerized Services for Databases
```
//  RabbitMQ
docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
// MongoDB
docker run --hostname mongodb --name mongodb -p 27017:27017 -e MONGODB_PASS="password" -d mongo:3.4-xenial
// PostgreSQL
docker run -it -d --rm --name postgresql -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres
```

4. Populate Databases 
```
cd db
python create_dbs.py
```

5. Checkout Mongo Databases to ensure the data has been populated
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

5. Open and Check out API by using Swagger (might be dockerized later)
```
cd ../app
python api.py
```
Open http://localhost:5000/apidocs/#/ in the browser, you can see the explanations and JSON models for each API. Also you can input your own JSON to test.

6. Turn on microservices (can be dockerized after things done)
```
cd ../service
nameko run admin user auction notification
```

## Run Test for back-end
In the back-end, we have implemented the user and admin's business logic. To test, please 
```
cd ../test
pytest
```

## Run Test for front-end
Please checkout \frontend for more information
