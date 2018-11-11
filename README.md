# README

This repository is intented to hold the entire code written in order to fulfill the OpenClassRooms Project 4 requirements.

It will be based upon a pipenv environment which means that to build a new instance of the script on your PC you'll need :
- Python 3.7+
- pipenv (simply install with `pip install pipenv`)

To deploy the required environment, use `pipenv install`. This will setup your directory with the components used in the piece of software (by reading configuration files such as the Pipfile you may see in this repo).

To launch the python script, use `pipenv run python [script.py]` (scripts yet to come).

## Basic MySQL Config for P5

Please note that basic configuration used to run this P5 script with MySQL is the following :

```sql
CREATE DATABASE OCP5;
CREATE USER 'OCP5'@'localhost' IDENTIFIED BY 'OCP5';
GRANT ALL PRIVILEGES on OCP5.* TO 'OCP5'@'localhost' IDENTIFIED BY 'OCP5';
```

May you want to change this configuration, further documentation will be soon provided (currently no options are available).
