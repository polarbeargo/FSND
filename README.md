# Full Stack Web Developer Nanodegree Capstone

This is the capstone project for the Udacity Full Stack Web Developer Nanodegree. The project is a simple casting agency that allows users to create, update, and delete actors and movies. The project is hosted on Render and can be accessed [here](https://cd0044-full-stack-web-developer.onrender.com/).

## Environment Setup

- In the project folder run

```bash
# Mac users
python3 -m venv venv
source venv/bin/activate
# Windows users
> py -3 -m venv venv
> venv\Scripts\activate
```

- **Install dependencies**<br> - Once we have our virtual environment setup and running, install dependencies by running:

```bash 
pip3 install -r requirements.txt
```
- The following are the key dependencies used in the project:
    - [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

    - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. We'll primarily work in `app.py`and can reference `models.py`.
    - [PostgreSQL](https://www.postgresql.org/) is the database used in the project.

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

```bash
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python3 test_app.py
```

# API Reference

### Roles:
- Film Assistant
    - Can delete, get and patch movies.
- Casting Director
    - All permissions a film Assistant has and can modify actors or movies.

### Permissions:
- `get:actors`
- `post:actors`
- `delete:actors`
- `get:movies`
- `post:movies`
- `patch:movies`
- `delete:movies`

### Set JWT Tokens
- To get the JWT tokens, we can use the following link to create users and sign them in:
```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}

Example:
https://dev-2rphxhqkvfsgcgle.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=p7kqMKdpURBhQHUYQyGDhtUfc2Z9Q4Jz
&redirect_uri=https://cd0044-full-stack-web-developer.onrender.com/
```

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`. 
- Authentication: We have implemented Auth0 for authentication. The tokens are provided in the [setup.sh](setup.sh) file.

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

- Fetches a dictionary of movies.
- Returns: An object with a single key, `movies`, that contains a list of movies and a success value.
- Sample: `curl -X GET -H "Content-Type: application/json" https://cd0044-full-stack-web-developer.onrender.com/movies -H "Authorization: $MOVIES_TOKEN"`
```json
{"movies":[
    {"id":1,"release_year":"2020-01-01","title":"Kong Skull Island"},
    {"id":2,"release_year":"2024-01-01","title":"Dune 2"},
    {"id":3,"release_year":"2024-03-29","title":"Kung Fu Panda"}],
    "success":true,
    "total_movies":3    
}

``` 
#### GET /actors
- Fetches a dictionary of actors.
- Returns: An object with a single key, `actors`, that contains a list of actors their name, age, gender and a success value
- Sample: `curl -X GET -H "Content-Type: application/json" https://cd0044-full-stack-web-developer.onrender.com/actors -H "Authorization: $ACTORS_TOKEN"               `
```json
{
  "actors":[
      {"age":"60","gender":"M","id":1,"name":"Michael Bay"},
      {"age":"20","gender":"F","id":2,"name":"Eve Witz"},
      {"age":"25","gender":"M","id":3,"name":"Harry Potter"}],
      "success":true
}

```

#### POST /movies
- General:
    - Creates a new movie using the submitted movie. Returns the id of the created movie and the success value.
- Sample: `curl -X POST -H "Content-Type: application/json" https://cd0044-full-stack-web-developer.onrender.com/movies -H "Authorization: $MOVIES_TOKEN" --data-raw '{ "title": "Kong Skull Island", "release_year": "2020-01-01"}'`
```
{
  "movie": 1, 
  "success": true
}
```
#### POST /actors/create
- General:
    - Creates a new actor using the submitted actor. Returns the id of the created actor and the success value.
- Sample: `curl -X POST -H "Content-Type: application/json" https://cd0044-full-stack-web-developer.onrender.com/actors/create -H "Authorization: $ACTORS_TOKEN" --data-raw '{"name": "Michael Bay", "age": "60", "gender": "M"}'`
```
{
  "created_actor_id":1,
  "success":true
}
```
#### DELETE /movies/{movie_id}
- General:
    - Deletes the movie of the given ID if it exists. Returns the id of the deleted movie and the success value.
- Sample: `curl -X DELETE -H "Content-Type: application/json" https://cd0044-full-stack-web-developer.onrender.com/movies/1 -H "Authorization: $MOVIES_TOKEN"`
```
{
  "deleted": 1, 
  "success": true
}
```

#### DELETE /actors/{actor_id}
- General:
    - Deletes the actor of the given ID if it exists. Returns the id of the deleted actor and the success value.
- Sample: `curl -X DELETE -H "Content-Type: application/json" https://cd0044-full-stack-web-developer.onrender.com/actors/1 -H "Authorization: $ACTORS_TOKEN"`
```
{
  "deleted": 1, 
  "success": true
}
```

#### PATCH /movies/{movie_id}
- General:
    - Updates the movie of the given ID if it exists. Returns the id of the updated movie and the success value.
- Sample: `curl -X PATCH https://cd0044-full-stack-web-developer.onrender.com/movies/2 -H "Authorization: $MOVIES_TOKEN" --data-raw '{ 'title': 'Dune', 'release_year': '2020-01-01'}'`
```
{
  "success": true,
  'movie': 2,
}
``` 
