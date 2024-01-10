# Django Rest Framework Permissions and Postgresql

## Author:
Jacob Bassett

## Date:
1-9-2024

## Description:
This is a simple rest api built with django, django-rest-framework, and postgresql. The purpose of this project if for Jacob to practice with django, DRF, permissions, PostgreSQL, and Docker.

## Usage and Tests:
Clone this repository down to your local machine and create a container with the following commands.

```bash
# have docker app open and run the follow
(.venv) ➜  drf-api-permissions-postgres git:(dev) ✗ docker compose up -d

# to open a shell, make migrations, and create user
(.venv) ➜  drf-api-permissions-postgres git:(dev) ✗ docker compose exec web bash
root@beecb2b6d567:/code# python manage.py migrate
root@beecb2b6d567:/code# python manage.py createsuperuser
Username (leave blank to use 'root'): user
Email address: user@email.com
Password:
Password (again):
Bypass password validation and create user anyway? [y/N]: y
# open http://127.0.0.1:8000/api/v1/snacks/create/ to login

# to run unit tests
root@beecb2b6d567:/code# python manage.py test
----------------------------------------------------------------------
Ran 20 tests in 5.910s

FAILED (errors=1)
Destroying test database for alias 'default'...
root@beecb2b6d567:/code# python manage.py test
Found 19 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...................
----------------------------------------------------------------------
Ran 19 tests in 5.590s
```

Once you have the Docker container up and running locally you can visit the following endpoints and perform the following actions.


| Endpoint                                                  | Permissions     | Actions          |
|-----------------------------------------------------------|-----------------|------------------|
| http://127.0.0.1:8000/api/v1/snacks/view/                 | AllowAny        | get              |
| http://127.0.0.1:8000/api/v1/snacks/create/               | IsAuthenticated | get, post        |
| http://127.0.0.1:8000/api/v1/snacks/update/<id>           | IsAuthenticated | get, put, delete |
| http://127.0.0.1:8000/api/v1/snackcollections/view/       | AllowAny        | get              |
| http://127.0.0.1:8000/api/v1/snackcollections/create/     | IsAuthenticated | get, post        |
| http://127.0.0.1:8000/api/v1/snackcollections/update/<id> | IsAuthenticated | get, put, delete |