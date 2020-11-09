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

3. Start Dockerized Services
```
//  RabbitMQ
docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
// MongoDB 还没弄docker，先在本地弄
brew install mongodb-community@4.4
brew services start mongodb-community@4.4
// PostgreSQL
docker run -it -d --rm --name postgresql -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres
```

4. Build Databases
```
cd /db
python create_dbs.py
```

5. Check out API using Swagger
```
cd /app
python api.py
```
Open http://localhost:5000/apidocs/#/ in the browser, you can see the explanations and JSON models for each API. Also you can input your own JSON to test.

