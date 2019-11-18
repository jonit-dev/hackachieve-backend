<p align="center">
  <img width="300" height="300" src="https://www.hackachieve.com/landing_resources/images/hackachieve-logo-vertical.svg">
</p>

# Hackachieve Community Version: Open-source alternative to project management

[Support this initiative through Patreon](https://www.patreon.com/hackachieve)

Hackachieve is a productivity management system oriented towards short term and long term goals, where users can collaborate with each other to achieve their personal or business goals!

This is our Django powered back-end server that's supposed to run together with our [front-end](https://github.com/jonit-dev/hackachieve-frontend)

![](https://www.hackachieve.com/landing_resources/images/dashboard.webp)

![](https://www.hackachieve.com/landing_resources/images/team-work.png)

**Features**

- Authentication: e-mail/password, social login (facebook)
- Onboarding tutorial
- Goals categories
- Create long-term or short-term goals
- Invite members to your board, add members to goal
- Tasks
- Organize your projects
- Prioritize goals
- Goal status: on going, done
- Upload files to goals
- Add checklists inside your goals
- Deadlines
- Card description, link support
- Goals tags
- Filter by goal type

**Front-end technology stack**:

- ReactJS, Redux, Redux-thunk

**Back-end technology stack**:

- Django, Django rest framework

## Onboarding

- [Click here to join us!](https://forms.gle/2B9C9yqA5ghbgQgw8)

- [Slack link](https://join.slack.com/t/hackachieve/shared_invite/enQtODI1MTQ3MDc1OTcwLWI2NThkYzY1ZWJiMmU2MjlmNjhlNDFiMTFiMGEyMzhiMmVmYzZmNjg4MGZjNTQ5ZTUzY2FkNTVjNjlmZTFkY2Q)

- [Onboarding checklist](https://docs.google.com/document/d/1pDb5k5inDOZ1L3jFc897x1jhrHCByFX53V6clIvLrQI/edit?usp=sharing) - your first steps!

- [Trello board](https://trello.com/b/Z4LkfUxm/hackachieve-open-source) - This is the read-only version only. Please request to join the project to get a member access

- [Documentation](https://docs.google.com/spreadsheets/d/1XaLITuGNUd2Y8iBDdIui7wCFxUaCd165xmohOt0zjp4/edit?usp=sharing) - A list with all of our relevant project documents

- [How do we manage our project](https://drive.google.com/drive/folders/1cSQEKJkNba2ly5yc_iHvwc7c-sd2NUr2):

- [Review our system flow](https://drive.google.com/file/d/1SUSOs3Wy9wxO8bx50Tn1ZuVmohrwDEK-/view?usp=sharing)

- [Canvas](https://canvanizer.com/canvas/rAEaPKu4VDWDV)

- [Project Management](https://drive.google.com/file/d/1hsQn5W298bo5ar1p13SAJooecn7Ko3sH/view?usp=sharing) - How do we manage our project goals

- [Code quality standards](https://drive.google.com/file/d/1GXOZkpDfXBBymKP4H5yN7u2xHyPaRBTn/view?usp=sharing)

## General guidelines

- You can only do a task that’s assigned to you and on the “sprint” column
- Your weekly limit varies according to my sprint planning. In every week, I estimate how many hours I will assign you and I adjust it properly
  Please, remember to move your assigned cards between Trello’s columns, according to its status (Backlog, ongoing, done), so I can know your current progress. You should also use the card status dropdown whenever possible.
- If you finish your tasks earlier than your weekly limit, let me know. If you log unnecessary hours just to reach the limit, I’ll remove you from the team as soon as I notice it.
- Please, make sure your PR is production-ready before submitting it. (for devs only)
- Clean all react console warnings after you finish (for ReactJS devs only)
- Your weekly hours are related to your efficiency and company needs (how much can you deliver and the time spent on each task). I'll increase or decrease according to it, your hourly rate and the company needs.
- If you have any issues, refer to the documentation first (check "documentation" column on trello). If it's not there, let me know and I'll be glad to help.

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

_ps: There's a significant chance you don't need to makemigrations again, but lets run it just in case._

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

`hackachieve/hackachieve/apiUrls.py`

#### API DOCS

You can find our api docs here:

```
https://documenter.getpostman.com/view/2492528/RztppSdX
```

### Required files

- Create .env file on the project root

- Setup a basic env configuration:

```
ENV=dev
SEND_TRANSACTIONAL_EMAILS=off
```

- You must also create a /logs folder inside /hackachieve. Inside this logs folder, add a myapp.log file with writing permissions

### mySQL Error

If some mysql error occurs while trying to setup the server, please install

```
sudo apt-get install libmysqlclient-dev
```

then install mysql client:

```
pip3 install mysqlclient
```

## Licensing

- **_GPL v2 (GNU General Public License):_**
  - By using Hackachieve you agree to [GPL License link](https://opensource.org/licenses/GPL-2.0)
- **_Hackachieve enterprise license_**
  - For licensing inquiries, please contact [Hackachieve Foundation](mailto:joaopaulofurtado@live.com)
  - Required if:
    - You wish to use Hackachieve as part of a proprietary application
