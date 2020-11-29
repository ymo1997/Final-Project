### Auction Site

## Install

Creating and activating virtual environment

    virtualenv venv
    cd venv/Scripts
    activate
(source the `venv/bin/activate` file if you are using mac)
Setup & install Redis server on Windows
* [Linux](https://redis.io/topics/quickstart)
* [Mac](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298)
* [Windows](https://www.onlinetutorialspoint.com/spring-boot/setup-install-redis-server-on-windows-10.html)

Start the Redis server 
  
Navigate back to the main folder. Installing requirements and making migrations

    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver


## NOTE

Django will generate an sqlite database by default, but we are not using it to store any information.