# Hackachieve

 Goals-focused productivity app for personal life or small businesss, with gamification features

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To run hackachieve server, make sure you have installed.

```
MAMP or XAMP or LAMP stack
mysql should be running before you try to run your server.
```

### Installing

1 - clone repository and cd into your folder

2 - search for settings.py (its on /hackachieve/hackachieve/settings.py) and setup your database config. You'll have to change basically NAME, USER and PASSWORD variables

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hackachieve',
        'USER': 'django-admin',
        'PASSWORD': 'yourpasswordhere',
        'HOST': '127.0.0.1',
        'POST': '3306',
        'OPTIONS': {
            "init_command": 'SET foreign_key_checks = 0; \
                             SET sql_mode=STRICT_TRANS_TABLES;',

        },
    }
```

3 - activate django virtual enviroment (run on the project root folder, not on settings.py folder):
   
```
source venv/bin/activate
```
4 - now, it will appear a (venv) symbol. That means you're now on virtual environment.
 
5 - Lets install our project dependencies. To do it, we'll use a package manager called pip (that's like npm, but focused on django/python), so make sure its installed:
 
 ```
 https://www.makeuseof.com/tag/install-pip-for-python/
```

6 - Then run the following command to install our dependencies
```
pip install -r requirements.txt
```

7 - Dependencies should be set after it. Lets setup our database. Run this command on your project root folder.
```
python3 manage.py makemigrations
python3 manage.py migrate
```
*ps: There's a significant chance you don't need to makemigrations again, but lets run it just in case.*

8 - Run the server
```
python3 manage.py runserver
```

9 - everything now should be good to go. If not, contact me (Joao Paulo)

10 - If you want to run the server again, after installing it, make sure you ALWAYS run your venv first:

```
source venv/bin/activate
python3 manage.py runserver
```

### API

To use our API, I strongly recommend you to use **postman**, since it will make your life easier.

You can check all routes available by taking a look at:

```hackachieve/hackachieve/apiUrls.py```

#### API DOCS

You can find our api docs here:
```
https://documenter.getpostman.com/view/2492528/RztppSdX
```
