# Django Shop With RestApi using DRF and JWT authentication

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/gomofficial/Django-Blog.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/Scripts/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```


Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd backend 
(env)$ python manage.py runserver --settings=Config.local

```
And navigate to `http://127.0.0.1:8000/`.


## Running Locally with Docker

1.build the image:

```sh
  $ docker-compose build .
```
2.Spin up the containers
```sh
  $ docker-compose up
```
then view the site at  http://localhost:8000/

## Walkthrough

Before you interact with the application, go to settings and set up
secret key.


## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test

```
## API Docs 
  navigate to `http://127.0.0.1:8000/swagger/` and `http://127.0.0.1:8000/redoc/`
  
## Features
 rest api using drf,
 jwt authentications,
 django templates,
 html and css
