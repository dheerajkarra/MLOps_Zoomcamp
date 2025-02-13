# Best Practices

Unit tests can be found in **tests** folder

Integration test can be found in **integration-test** folder

For linting and code formatting, the file **pyproject.toml** is used

Makefile is also present

For pre-commit hooks, **.pre-commit-config.yaml** is used

**NOTE :** I have used SSH terminal for this section. I have provided the Pipfile if you are facing issues with the environment. You can create a virtual environment using Pipfile by running the command : pipenv install

More information on how to create a virtual environment using Pipfile can be found [here](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment)

Activate the virtual environment by running the following command in SSH terminal :

      pipenv shell

**NOTE :** integration-test folder has **run.sh** file. You need to give permission before running it, or else you will get permission denied error.

You should be inside **code** directory. You can give permission to run.sh file by executing the following command in SSH terminal :

      chmod +x integration-test/run.sh

**IMPORTANT-NOTE :** Before running the commands, go to **run.sh** file present inside **integration-test** directory.

### Steps to run unit tests, integration test, linting, and code formatting

1. Open SSH terminal. Activate virtual environment which has the libraries mentioned in Pipfile. Make sure you are inside **code** directory in the terminal.

2. Execute the following command :

       make publish

This command will :

* Run unit tests. There might be warnings related to sklearn version. You can ignore that. To configure Python Tests, please refer the video MLOps Zoomcamp 6.1 - Testing Python code with pytest, at time **6:09**
* Perform quality checks - linting and code formatting. It will reformat batch.py file by using "black"
* Build docker container and image
* Run integration test. Integration test will output the predicted energy usage and print the contents of predictions
* Print contents of publish.sh file

### Steps to perform pre-commit hooks

1. Open SSH terminal. Activate virtual environment which has the libraries mentioned in Pipfile. Make sure you are inside **code** directory in the terminal.

2. Initialize empty Git repository by running the following command :

       git init

3. Install pre-commit by running the following command :

       pre-commit install

4. Check status of files by running the following command :

       git status

5. Add all the files by running the following command :

       git add .

**NOTE :** Make sure "." is added at the end of above command

6. Commit the files by running the following command :

       git commit -m 'initial commit'

Here, either all tests will pass or some tests will fail. If you have already executed the command *make publish*, then all tests should pass. If not, then some tests will fail, but those files will be reformatted by pre-commit. Repeat Steps 4, 5, and 6 to add the files modified by pre-commit.

Screenshots of logs of SSH terminal while executing the above commands have been saved to "output" folder for reference.
