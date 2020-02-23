# Cheng's DigIO Test

This project is for my DigIO test

## For people who is familiar with Python

### Prepare environment

This solution was written with python3 with all the dependencies listed in
[requirement.txt](https://github.com/s3341458/digIO-test-python/blob/master/requirements.txt),
please use any dependency manager(eg. [pipenv](https://pipenv-fork.readthedocs.io/en/latest/))
you like

### Run parser on a log file:

    python3 solution.py [log_file_path]
    eg. python3 solution.py programming-task-example-data.log

### Run testcases:

    pytest


## For people who is more familiar with Docker

### Prepare environment

 - [Docker](https://docs.docker.com/)
 - [Docker Compose](https://docs.docker.com/compose/install/)

See these links to install on your system, then in the project root directory run:

    docker-compose build


### Run parser on a log file:

    docker-compose run --rm solution [log_file_path]
    eg. docker-compose run --rm solution programming-task-example-data.log

### Run testcases:

    docker-compose run --rm test

## Need to Mention:
+ The solution is based on my understanding about [task-example-log](https://github.com/s3341458/digIO-test-python/blob/master/programming-task-example-data.log), a bigger sample log will help me develop a more robust solution
+ In real world scenario, able to access the server config file will have a great benefits for this kind of task


