# MLOps Zoomcamp Project - Appliances Energy Usage Prediction

This is my project for MLOps Zoomcamp from DataTalks.Club

## Objective

The goal of this project is to understand the usage of different MLOps processes
in the Machine Learning pipeline built. Understanding of different services that help in 
building the production ready ML codes is explored using this project.

## Project Structure

To reproduce the project without running into issues, I recommend to prepare the virtual environment. 

There are separate directories for each criteria mentioned in README of [MLOps Zoomcamp Course Project](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/07-project)

The directories are : 

1. model_development
2. experiment_tracking_and_model_registry
3. workflow_orchestration
4. model_deployment
5. model_monitoring
6. best_practices

Each directory has a README file in it which has the instructions on how to run the code. 

## Tools and Technologies Used 

* Experiment Tracking and Model Registry : MLflow
* Workflow Orchestration : Prefect
* Containerization : Docker and Docker Compose
* Model Deployment : Deployment as web service using Flask, Docker and MLflow
* Model Monitoring : Evidently AI, Grafana and Prometheus
* Best Practices : Unit tests, Integration test, Linting, Code Formatting, Makefile and Pre-commit hooks

## Future Scope

1. Integration with Cloud
2. Inclusion of features like Alerting mechanism during model monitoring, IaC using Terraform 

**NOTE :** For peer reviewing process, please download the repository as zip file instead of cloning it using Git bash. You will run into issues while reviewing best_practices section of the project if you clone the repository.
