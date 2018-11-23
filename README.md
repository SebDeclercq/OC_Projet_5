# README

This repository is intented to hold the entire code written in order to fulfill the OpenClassRooms Project 5 requirements.

It will be based upon a pipenv environment which means that to build a new instance of the script on your PC you'll need :
- Python 3.7+
- pipenv (simply install with `pip install pipenv`)

To deploy the required environment, use `pipenv install`. This will setup your directory with the components used in the piece of software (by reading configuration files such as the Pipfile you may see in this repo).

For the first run, set up the MySQL database (see [Database Configuration](#database-configuration)) and use `pipenv run python main.py --setup_db`. If your configuration is different from default, please refer to the [Usage](#usage) section.

To use the python script with default configuration, run `pipenv run python main.py`.

Lots of options are available.

The `categories.yml` holds the list of the categories you wish to manage in your database. The program is configured to allow 5 categories max and 100 products max by category.

## Usage

Please find the help page hereafter, which is also available with the `-h --help` option for `main.py`.


    DESCRIPTION:
    This main script is intended to pilot all processing actions for the P5 of OpenClassRooms DA Python. It creates the database or updates it if the correponding options are provided. Its main goals are to interact with collected OpenFoodFacts data in order to select healthier products than your regular.

    USAGE:
       python main.py [OPTIONS]

    MODES:
       --setup_db       Sets up database (flag)
       --update_db      Updates database content (flag)
       -i --interactive DEFAULT: Active interactive mode (flag)

    OPTIONS:
       --categories File containing the wished categories in database
       -u --user    Username for MySQL database (useless for SQLite)
       -p --pass    Password for MySQL database (useless for SQLite)
       -d --dbname  Database to use (for SQLite: "sqlite:///[DBNAME]")

       -h --help    Displays this help guide

    REQUIREMENTS:
       python 3.7+
       requests
       sqlalchemy
       pyyaml
       mysql-connector-python


## Database Configuration

Default configuration uses MySQL as RDBMS. The default configuration used to run this script is the following :

```sql
CREATE DATABASE OCP5;
CREATE USER 'OCP5'@'localhost' IDENTIFIED BY 'OCP5';
GRANT ALL PRIVILEGES on OCP5.* TO 'OCP5'@'localhost' IDENTIFIED BY 'OCP5';
```

May you want to change this configuration, please use the adequate options (see in previous section of this README).
