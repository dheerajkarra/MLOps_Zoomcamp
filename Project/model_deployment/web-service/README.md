# Model Deployment

This section aims to deploy model as web-service using Flask and Docker. The model deployment code is containerized.

**NOTE :** I have used SSH terminal for this section. I have provided the Pipfile if you are facing issues with the environment. You can create a virtual environment using Pipfile by running the command : pipenv install

More information on how to create a virtual environment using Pipfile can be found [here](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment)

## Steps to run the script in SSH terminal using Flask

1. Open two terminal windows, Terminal 1 and Terminal 2. In both the terminals, activate virtual environment which has the libraries mentioned in Pipfile. You should be inside web-service directory in both the terminals.

Activate the virtual environment by running the following command in SSH terminal :

      pipenv shell

2. In terminal 1, to start the server, execute the following command :

       python predict.py

**NOTE :** The server should keep running, and you should go to terminal 2 to execute the test script.

1. In terminal 2, execute the following command :

       python test.py

This will send selected features to the server and server will send predicted energy usage based on the features. 

## Steps to run the script in terminal using Docker

1. Stop the web services running in terminal 1. For Windows, it can be stopped using CTRL + C

2. Here, we are using docker to run the model. The code is containerized. In terminal 1, execute the following commands :

       docker build -t energy-deploy:v1 ./

This command will build a Docker image "energy-deploy" from the Dockerfile.

**NOTE :** Do not forget to include the "." at the end of Command-1

3. After the image is built, start the gunicorn server by running the following command in terminal 1 : 

       docker run -it --rm -p 9696:9696 energy-deploy:v1

**NOTE :** The services should keep running, and you should go to terminal 2 to execute the test script.

4. To get response from the server, execute the following command in terminal 2 : 

       python test.py

This will send selected features to the server and server will send predicted energy usage based on the features. 

Screenshots of logs in terminal are saved in "output" folder for reference.
