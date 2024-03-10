## Full Stack Web Developer Nanodegree Capstone

This is the capstone project for the Udacity Full Stack Web Developer Nanodegree. The project is a simple casting agency that allows users to view, create, update, and delete actors and movies. The project is hosted on Heroku and can be accessed [here](https://fsnd-capstone-udacity.herokuapp.com/).

### Environment Setup

- From the heroku_sample folder run

```bash
# Mac users
python3 -m venv venv
source venv/bin/activate
# Windows users
> py -3 -m venv venv
> venv\Scripts\activate
```

- **Install dependencies**<br> - In the heroku_sample folder run

```bash 
pip3 install -r requirements.txt
```
- Set up the environment variables
```
chmod +x setup.sh
source setup.sh
```
### Set up the Database

- Create a new database in PostgreSQL

```
createdb capstone
```
- To migrate your local database to another database in the Heroku cloud, you will have to run these commands:
    
```bash
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```
- To debug the database, use the following commands:
```bash
psql postgres 
\c capstone # Connect to the database
\dt # List of relations
```

### Start the Server

- From the heroku_sample folder ensure you are working at created virtual environment run the server, execute:

``````
python3 app.py
``````

### Running the tests

- From the heroku_sample folder run

```bash
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python3 test_app.py
```
