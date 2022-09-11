# Model Monitoring

This section aims to monitor ML models using Evidently, Grafana, Prometheus and Prefect. The scripts perform basic model monitoring that calculates and reports metrics and saves evidently report in the form of HTML file.

## Steps to execute the script

1. Open 3 SSH terminal windows, terminal 1, terminal 2, terminal 3. In all the terminals, activate virtual environment which has the libraries mentioned in Pipfile. You should be inside model_monitoring directory in all the 3 terminals.

Activate the virtual environment by running the following command in SSH terminal :

      pipenv shell

2. In Terminal 1, start the Evidently, Prometheus and Grafana services by executing the following command :

       docker-compose up

**NOTE :** The services should keep running, and you should go to terminal 2 to execute the scripts.

3. After the dataset is downloaded, we need to send the data from the downloaded dataset to the prediction service. Execute the following command in Terminal 2 : 

        python send_data.py

This script will send single row from dataset to prediction service (every second) along with creating the file **target.csv** with actual results (so it can be loaded after). To keep it simple, instead of sending all the data from the dataset, I am sending only 100 rows of data. You don't need to stop the script yourself, it will exit automatically after it has sent 100 rows of data.

4. (Optional) While sending the data (or after the data is sent), you can view the data drift at **http://localhost:3000/** This is shown in the video 
MLOps Zoomcamp 5.4 - Realtime monitoring walktrough (Prometheus, Evidently, Grafana) at time **11:44**. The username and password for Grafana is **admin**

You can also view the Prometheus database at **http://localhost:9091/** . This is also shown in video - MLOps Zoomcamp 5.4 - Realtime monitoring walktrough (Prometheus, Evidently, Grafana) at time **14:11**

5. After the data is sent, execute the following command in Terminal 2 : 

        prefect orion start

This will start Prefect. It can be viewed at **http://localhost:4200/** Go to terminal 3, to execute prefect_example.py.

6. In Terminal 3, execute prefect_example.py script by running the following command :

        python prefect_example.py

This script will :

* Load target.csv to MongoDB
* Download dataset from MongoDB
* Run Evidently Model Profile and Evidently Report on this data
* Save Profile data back to MongoDB
* Save Report to evidently_report_example.html

You can view the flows, flow runs and radar plot at **http://localhost:4200/**

To view the evidently report (html file), you need to download it to your local system first, and then open it with any browser of your choice.

Screenshots of Evidently report (html file), Grafana dashboard, Prometheus dashboard, Prefect flow and target.csv are saved in "output" folder for your reference.
