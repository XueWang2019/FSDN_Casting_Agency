# FSDN_Casting_Agency
## Result:
1. Final url:
https://casting-agency-liu.herokuapp.com/
2. Instructions to set up authentication:
The token for the three user: assistant, director and producer are saved in test.py file. They will expire at 12/03, around 20:00 (GMT+1)
3. How to generate token: use below url as without front end:
https://castingagenceudacity.eu.auth0.com/authorize?audience=http://localhost:5000&response_type=token&client_id=Wi6AkMalbQsq6b3s4xACd0bsHOIJWJHG&redirect_uri=http://localhost:5000

## Motivation
Through previous 4 projects, I have learned below concepts:
* Coding in Python 3
* Relational Database Architecture
* Modeling Data Objects with SQLAlchemy
* Internet Protocols and Communication
* Developing a Flask API
* Authentication and Access
* Authentication with Auth0
* Authentication in Flask
* Role-Based Access Control (RBAC)
* Testing Flask Applications
* Deploying Applications
Capston project starts almost from zero, which is a very good practis to use all of the concepts. For the point I am comfortable with, this an opportunity to confirm that the ability with that skill. For those that you are less confident in, this is an opportunity to reinforce those skills and walk away very confident in them.
With our toolbox in hand, let's see what we're getting into with this Capstone!

## Project dependencies, local development and hosting instructions,
### Key Dependencies
* Python 3.8
* Flask 
* SQLAlchemy 
* Flask-CORS 
* Heroku

## Detailed instructions for scripts to install any project dependencies, and to run the development server.
1. Use Auth0 to for authenrization and authentication and Role-Base Access Control
2. Test all of the endpoints locally: the 16 test cases are passed locally. During this process, database path uses local postgresql database
3. Create a heroku application: then get the git url and application domain
4. Configuration:
4.1 requirements.txt: I don't use pip freeze > requirements.txt because there is problem with cloud-init, so I manually write a requirements.txt which can solve this problem
4.2 run our local migrations using our manage.py file, to mirror how Heroku will run behind the scenes for us when we deploy our application:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
During this process, keep the database and password are from locally
5. Deploy
Use the reference from Heroku to push to git

6. Add postgresql add on for our database After step 5, I add postgresql add on for our database, use below command: 
```
heroku addons:create heroku-postgresql:hobby-dev --app casting-agency-liu
```
Use below command, you can check your configuration variables in Heroku. You will see DATABASE_URL and the URL of the database you just created.
```
heroku config --app name_of_your_application
```

7. Modify the database link Now replace the DATABASE_URL with the one generated at setp6 in your py file

8. Now push changes in git use git pull
```
git pull heroku master
```


## Documentation of API behavior and RBAC controls
Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

Models:  
* Movies with attributes title and release date  
* Actors with attributes name, age and gender  

Endpoints:
* GET /actors and /movies   
* DELETE /actors/ and /movies/      
* POST /actors and /movies and      
* PATCH /actors/ and /movies/    
 
Roles:  
* Casting Assistant:  
  *  Can view actors and movies  
* Casting Director:  
  * All permissions a Casting Assistant has and…  
  * Add or delete an actor from the database  
  * Modify actors or movies  
 Executive Producer  
   * All permissions a Casting Director has and…  
   * Add or delete a movie from the database  
     
Tests:  
  * One test for success behavior of each endpoint  
  * One test for error behavior of each endpoint  
  * At least two tests of RBAC for each role  

### API Endpoint  
```
GET '/'
*  Home Route
*  Return message:
 {
  "message": "Hello,hello, World!"
}

GET '/movies':  
* Get movie's name
*  Return:  
 {
                    "success": True,
                    "movie name": movie
                }
 GET '/actors':
 * Get actors' name
 * Return:{
                    "success": True,
                    "actor": actor
                }
                
 POST '/movies':
 * Add movies
 * Return {
                    "success": True,
                    "title": title,
                    "release_date": release_date
                }
                
 POST '/actors'
 * Add actors
 * Return:  {
                    "success": True,
                    "name": name,
                    "age": age,
                    "gender": gender
                }
                
 PATCH '/movies/<int:id>'  
 *  Edit movies
 *  Return added movie's detail
 *  {"success": True, "movie": [movies.details()]}

PATCH '/actors/<int:id>'
*  Edit actors
*  Return: {"success": True, "actor": [actors.details()]}

DELETE '/movies/<int:id>'
* Delete movies
* Return {
                    "success": True,
                    "delete": id
                }
                
DELET '/actors/<int:id>' 
* Delete actors
* Return {
                    "success": True,
                    "delete": id
                }
  
  ```

### Medium story for deployment  

[medium story](https://towardsdatascience.com/deploy-a-micro-flask-application-into-heroku-with-postgresql-database-d95fd0c19408)
