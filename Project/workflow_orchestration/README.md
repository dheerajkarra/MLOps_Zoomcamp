# Workflow Orchestration

This section aims to fully deploy the workflow using Prefect. 

The following services of Prefect are used in this section : 

1. Deployments
2. Work Queues and Agents

***********************************************************************************************************************************************************************

**Prefect Agents and Work Queues**

Agents and work queues bridge the Prefect Orion orchestration environment with a user’s execution environment. When a deployment creates a flow run, it is submitted to a specific work queue for scheduling. Agents running in the execution environment poll their respective work queues for new runs to execute. Work queues are automatically created whenever they are referenced by either a deployment or an agent.

***********************************************************************************************************************************************************************

### Steps to run the script in SSH terminal

Open 3 SSH terminal windows, Terminal 1, Terminal 2, Terminal 3. In all the terminals, activate virtual environment which has the libraries mentioned in Pipfile. You should be inside workflow_orchestration directory in all the 3 terminals.

Activate the virtual environment by running the following command in SSH terminal :

      pipenv shell

1. In Terminal 1, execute the following command : 

        
        prefect orion start

This will start Prefect. Let the service be running in this terminal. Go to Terminal 2, to execute other commands.

2. In Terminal 2, run the following command : 

        prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

3. In Terminal 2, run the following command :

        prefect deployment create orchestration.py

4. To view the deployments, run the following command in Terminal 2 :

        prefect deployment ls

Once the deployment has been created, you'll see it in the Prefect UI (**http://127.0.0.1:4200**) and can inspect it using in the CLI by running the above command.

The next steps are related to scheduled deployments, agents, and work queues. If you wish to see scheduled deployments, then make changes in yaml file. 

5. Create a work queue. Run the following command in terminal 2 :

        prefect work-queue create {work-queue-name}

This will create a work queue and print its details (name, uuid, tags, concurrency limit) in the terminal. If you open the work queue in Prefect UI (**http://127.0.0.1:4200**), you will see upcoming runs. Those will be either "scheduled" or "late" depending on the interval you have set in yaml file. 

7. Now, to deploy the flow runs present in work queue, you need to start an agent. Agent processes are lightweight polling services that get scheduled work from a work queue and deploy the corresponding flow runs. In Terminal 2, run the following command : 

        prefect agent start 'uuid'
   

The above command will start an agent. Agent deploys flow runs present in work queue. 

If you have scheduled the deployments, then you can see the deployment of flow runs in terminal 2 at periodic interval as mentioned in schedule in main-deployment.yaml file.

After the agent has started, the work queue will be empty. The work queue will have "scheduled" or "late" flow runs until an agent is started.

Flows, deployments, blocks and work queues can be viewed at : http://127.0.0.1:4200

Screenshots of flows, deployment, agents and work queues are stored in "output" folder for reference.

 
**Commands used**

        prefect orion start
        prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
        prefect deployment create orchestration.py
        prefect deployment ls
        prefect work-queue create energy_usage
        prefect agent start 'uuid'
