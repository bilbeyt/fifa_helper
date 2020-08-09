# FIFA19 Helper

This application provides following functionalities:

* Search players with given word that is found in name, nationality or club
* Build a team with given budget

## Requirements

* Python 3.8+
* Remote MySQL server
* Docker

## Usage (Docker)

*CONTAINER_NAME* can be determined using **docker ps**.

1. Create .env file from .env-sample using your remote sql credentials.
2. Run following command to build Docker image.
    ```bash
    docker build -t fifa_helper:latest .
    ```
3. Run following command to start server.
    ```bash
    docker run --env-file=.env -p 8000:8000 fifa_helper
    ```
4. Run following command to initialize db and create first players. 
    ```bash
    docker exec -it $CONTAINER_NAME python player_creator.py
    ```

## Running Tests

*CONTAINER_NAME* can be determined using **docker ps**.

1. Use following command for coverage. 
    ```bash
    docker exec -it $CONTAINER_NAME coverage run -m pytest
    ```
2. Use following command to see report.
    ```bash
    docker exec -it $CONTAINER_NAME coverage report
    ```

## Deploying the Application

1. Get a Heroku account.
2. Login to your account using the command below.
    ```bash
    heroku login
    ```
3. Login to container service.
    ```bash
    heroku container:login
    ```
4. Create a new space for your application with following:
    ```bash
    heroku create
    ```
5. Build and push the docker image using command below.
    ```bash
    heroku container:push web
    ```
6. Release the application using command below.
    ```bash
    heroku container:release web
    ```
7. Set environment variables using following command:
    ```bash
    heroku config:set $(cat .env | sed '/^$/d; /#[[:print:]]*$/d')
    ```
8. Start the application using the command below.
    ```bash
    heroku ps:scale web=1
    ```

## Demo

You can test the application using this [url](https://salty-plateau-88036.herokuapp.com/).