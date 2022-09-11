# Model Deployment

This section aims to deploy the model locally using artifacts from MLFlow service.

## Steps to execute the script

1. Open 3 terminal windows. Terminal 1, Terminal 2, and Terminal 3. In all the terminals, activate virtual environment which has the libraries mentioned in Pipfile. You should be inside web-service-mlflow directory in all the 3 terminals. 

Activate the virtual environment by running the following command in SSH terminal :

      pipenv shell

2. In Terminal 1, type the following command :

       mlflow ui --backend-store-uri=sqlite:///mlflow.db 


**NOTE :** The server in terminal 1 should keep running, and you should go to terminal 2 to execute other scripts.

3. After executing the command in step 2, run the script **random-forest-mlflow.py**. It will train and log model in MLflow.

4. In this step, you need to export the RUN_ID of the model which was logged locally.

5. Open Terminal 2, and export the RUN_ID you got from step 4. Export the RUN_ID by running the following command : 

       export RUN_ID="run-id"
   

6. Now in Terminal 2, after exporting the RUN_ID, execute the following command : 

       python predict.py

This command will start the server, which waits for incoming data.

**NOTE :** The server in terminal 2 should keep running, and you should go to terminal 3 to execute other scripts.

7. Open Terminal 3, and execute the following command : 

       python test.py

This command will send selected features to the server and print the model version which has been trained and logged in MLflow. It will also print the predicted energy usage based on the features given.

**NOTE :** If you encounter **connection in use** error while running MLflow, the run the following command in terminal :

    pkill gunicorn

You can view the logged model in MLflow (http://127.0.0.1:5000).

Screenshots of MLflow and logs of SSH terminal are saved in "output" folder for reference.
