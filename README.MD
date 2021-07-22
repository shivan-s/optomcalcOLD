# OptomCalc
*Calculations for Optometry*
---
By Shivan Sivakumaran

## Introduction

The is a website that contains common calculations performed by Optometrists and Optical Dispensers.

[The site is live](https://optomcalc.shivan.xyz)

## How this works

### Production Set up

Ansible playbooks are used to set up the application on a 'production' server. [The code for this can be found here](https://github.com/shivans93/ansible).

This includes the `nginx` and `certbot` set up, which are on the server. The `postgresql` database, `django` and `gunicorn` app sit inside their own `docker` containers.

`Gunicorn` is used as a the wsgi service.

`Docker-compose` is used to orchestrate the entire project:
```
$ sudo docker-compose up --build
```

### Local running

This is weird and I'm sure there are plenty workarounds. Since I do not have `nginx` running on my local machine, if I run the `docker-compose` command as if it were in production, the site will work. However, I will not have any static files. This is because `nginx` serves those static files. I use `docker-compose` to spin up at `postgresql` database and then run:
```
$ pipenv run python manage.py runserver
```
to create a local django instance, which is connected to the dockerised `postresql` database. I can a function application with static files that I can then make edits to my code.

### Code structures

Below is how the application is structured

```
├── db-data # Database
├── optomcalc
│   ├── calculator # application or 'calculator' code
│   │   ├── templates
│   │   │   └── calculator
│   │   └── tests
│   ├── optomcalc # admin app
│   └── static # static files for nginx
│       └── calculator
│           ├── css
│           └── js

```
## Feedback

Please [contact me](mailto:shivan@shivansivakumaran.com) if you have any questions.
