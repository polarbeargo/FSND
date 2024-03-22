# Full Stack Web Developer Nanodegree Capstone

This is the capstone project for the Udacity Full Stack Web Developer Nanodegree. The project is a simple casting agency that allows users to view, create, update, and delete actors and movies. The project is hosted on Heroku and can be accessed [here](https://fsnd-capstone-udacity.herokuapp.com/).

## Environment Setup

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
- The following are the key dependencies used in the project:
    - [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

    - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.
    - [PostgreSQL](https://www.postgresql.org/) is the database used in the project.

    - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.
    - [Auth0](https://auth0.com/) is the authentication and authorization platform used in the project.

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

```
flask run --reload
```
- The `--reload` flag will detect file changes and restart the server automatically.


### Running the tests

- From the heroku_sample folder run

```bash
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python3 test_app.py
```

# API Reference

### Roles:
- Casting Assistant
    - Can view actors and movies
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies

### Permissions:
- `get:actors`
- `post:actors`
- `patch:actors`
- `delete:actors`
- `get:movies`
- `post:movies`
- `patch:movies`
- `delete:movies`

### Set JWT Tokens
- To get the JWT tokens, you can use the following link to create users and sign them in:
```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: We have implemented Auth0 for authentication. The tokens are provided in the [setup.sh](projects/capstone/heroku_sample/setup.sh) file.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return the following error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /movies

- Fetches a dictionary of movies in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `movies`, that contains an object of `id: category_string` key: value pairs.
- Sample: `curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://127.0.0.1:5000/movies`
```json

``` 
#### GET /actors
- Fetches a dictionary of actors in which the keys are the ids and the value is the corresponding string of the actors
- Request Arguments: None
- Returns: An object with a single key, `actors`, that contains an object of `id: category_string` key: value pairs and a list of questions.
- Sample: `curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://127.0.0.1:5000/actors`
```json

```

#### POST /movies
- General:
    - Creates a new movie using the submitted movie. Returns the id of the created movie, success value to update the frontend.
- Sample: ``
```
{
  "created": 25, 
  "success": true
}
```
#### POST /actors
- General:
    - Creates a new actor using the submitted actor. Returns the id of the created actor, success value to update the frontend.
- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name":"Hmm", "age":"18", gender: "M"}'`
```
{
  "created": 25, 
  "success": true
}
```
#### DELETE /movies/{movie_id}
- General:
    - Deletes the movie of the given ID if it exists. Returns the id of the deleted question, success value to update the frontend.
- Sample: `curl -X DELETE http://127.0.0.1:5000/movies/11`
```
{
  "deleted": 11, 
  "success": true
}
```

#### DELETE /actors/{actor_id}
- General:
    - Deletes the actor of the given ID if it exists. Returns the id of the deleted question, success value to update the frontend.
- Sample: `curl -X DELETE http://127.0.0.1:5000/acctors/1`
```
{
  "deleted": 1, 
  "success": true
}
```
