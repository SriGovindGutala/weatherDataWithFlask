# Code Challenge Template

Flask API for Weather data ingestion and viewing


Steps to install:

1. create virtual env "weatherapp" using your favourite virtual env tool. I personally recommend "pyenv"

2. active env

3. pip install -r requirements.txt

4. python flask.py

Now the app should be running at 127.0.0.1:8000

To try and check out API signatures there is a postman collection as well as Swagger at
127.0.0.1:8000/apidocs/index.html


To run test suite, run command
pytest


Database that is being used for now is SQLite

Ingestion data to start with by calling
127.0.0.1:8000/api/weather/ingest

This will fill the database with all the data from the .txt files


Improvments that I can think of:

1. Use envs to make app more "12 factor enabled"

2. Use more production grade loggin system

3. Auto fix linting, right now pylint gives only errors does not fix it

4. More testing scenarios, covering all edge cases

5. Use a production grade Database

6. Use sentry as a error detecting monitoring system



AWS Deployment:

Older methods:

1. Use jenkins to create github webhooks and get latest code and scp it to EC2 instance

2. Manually copy over FTP to EC2

New methods:

Most cloud providers now a days have a robust CI/CD mechanism including one click integration with Github webhooks.

AWS CodeBuild, CodeDeploy, CodePipeline can be used in tandem to easily push latest code to EC2.

A startup script like start.sh can be written to ensure smooth start of a new installation.

This can include supervisor to make it fail safe

And Nginx and gunicorn can be added as dependencies to make it a production grade API system.
