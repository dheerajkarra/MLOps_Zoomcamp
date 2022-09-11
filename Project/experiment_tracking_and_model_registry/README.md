# Experiment Tracking and Model Registry

This section aims to perform experiment tracking and register best models using MLflow. 

File Structure : 

1. preprocess.py -> This script loads the raw data from input folder, processes it and saves the pre-processed data in output folder.

2. train.py -> The script will load the pre-processed data from output folder, train the model on the training set and calculate the RMSE on the validation set. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud).

3. hpo.py -> This script tries to reduce the validation error by tuning the hyperparameters of the random forest regressor using hyperopt. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud).

4. register_model.py -> This script will promote the best model (with lowest test_rmse) to the model registry. It will check the results from the previous step and select the top 5 runs. After that, it will calculate the RMSE of those models on the test set and save the results to a new experiment called "red-wine-random-forest-best-models". The model with lowest test RMSE from the 5 runs is registered.

**Artifacts are saved locally. My script saves these artifacts in local folder.**

The scripts use SQLite as backend for storing the artifacts.

The scripts will log artifacts in MLflow, locally
(http://127.0.0.1:5000)

**NOTE :** I have used Anaconda Prompt for this section instead of SSH terminal because I was having issues with sklearn version in SSH terminal. If you face any errors while running the script, please consider creating a new environment using the requirements.txt file.

### Steps to create and activate anaconda environment

1. conda create -n mlops python=3.9

2. conda activate mlops

3. pip install -r requirements.txt

### Steps to run the scripts

1. Open 2 SSH terminal/Anaconda Prompt - Terminal 1 and Terminal 2. In both the terminals, activate virtual/conda environment which has the libraries mentioned in **requirements.txt** file. You should be inside experiment_tracking_and_model_registry directory in both the terminals.

2. In terminal 1, start the MLflow server using the following command :

       mlflow ui --backend-store-uri=sqlite:///mlflow.db 

**NOTE :** The server should keep running, and you should go to terminal 2 to execute the scripts.

3. Go to terminal 2, and execute the script preprocess.py. This script loads the raw data from input folder, preprocesses it and saves the pre-processed data in output folder. Run the script using the following command : 

       python preprocess.py

4. Make sure the server from step-1 is up and running. After the execution of step-2 is finished, execute the script train.py in terminal 2. Run the script using the following command : 

       python train.py
       
The script will load the datasets produced by the previous step, train the model on the training set and calculates the RMSE on the validation set. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud). 

5. After the execution of step-3 is finished, execute the script hpo.py in terminal 2. Run the script using the following command :

       python hpo.py
       
This script tries to reduce the validation error by tuning the hyperparameters of the random forest regressor using hyperopt. The script logs the parameters and artifacts in MLflow(locally). 

6. After the execution of step-4 is finished, execute the script register_model.py in terminal 2. Run the script using the following command :

       python register_model.py
   
This script will promote the best model (with lowest test_rmse) to the model registry. It will check the results from the previous step and select the top 5 runs. After that, it will calculate the RMSE of those models on the test set and save the results to a new experiment called "energy-random-forest-best-models_2". 

For model registry, out of the 5 runs in "energy-random-forest-best-models_2" experiment, the run with lowest test_rmse is registered. You can view the registered model at **http://127.0.0.1:5000/#/models** 

The script logs the parameters and artifacts in MLflow(locally) 

**NOTE :** If you encounter **connection in use** error while running MLflow, the run the following command in terminal :

    pkill gunicorn

Experiments and models(and artifacts) can be viewed locally at http://127.0.0.1:5000 Registered model can also be viewed at http://127.0.0.1:5000/#/models

Images of experiments and registered model from MLflow are saved to "output_images" folder for reference.
