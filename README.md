# Compliance Continuous Monitoring

## Premise
The agent must do:
- List of running processes.
- Users with an open session in the system.
- Name of the operating system.
- Version of the operating system. 

The API must consist of:
- An application with an endpoint that allows the agent to send
the information collected
- Stored the information collected on normalized DB

Must have:
- Server must be running on an AWS EC2 instance
- Containerize the application
- Documentation 
- Detail of what other functionality you think we could implement in this system in the future
- Build infrastructure using CloudFormation

## Problem
Generate a program (agent) that can be executed on one of our servers, and from different commands of the operating system, can send the following data to an application (API).

## Solution

![Infra diagram](/images/infra-done.png)
### Tools

| Tools | Version |
|---   | ---  |
| Language | Python3.8 |
| Web framework | FastAPI 0.65.2 |
| DataBase | MySQL 8.0.3 |
| PaaS | Docker |
| docker-compose | docker-compose  |

## Agent

Responsible for capturing, from a host, metrics like:

- SO name
- SO version
- Processes running
- Online Users
- CPU usage
- Host IP

And send to API.
### How to run locally? *(Make sure that you have installed python3)*
1. ```pip3 install -r api/requirements.txt```
2. ```python3 agent/agent.py so-name```
3. ```export URL_API=http://{API_ENDPOINT} ```

*Make sure that you have set TOKEN environment in agent.py file*
### How to use? 

``` sh
python3 agent.py so-name    -   Send SO name
python3 agent.py ps         -   Send processes
python3 agent.py users      -   Send online users
python3 agent.py so-version -   Send SO version
python3 agent.py cpu        -   Send CPU usage
```

## API

Responsible for capturing metrics sent my Agent via POST request and save to MySQL database.

The database diagram is:
![DB diagram](/images/api-database.png)

### How to run locally? *(Make sure that you have installed python3)*
1. ```pip3 install -r api/requirements.txt```
2. ```uvicorn main:app```
### How to run with container? *(Make sure that you have installed Docker and docker-compose)*
1. ```docker-compose up -d```

### How to use?
- GET Requests:
    - http://${API_ENDPOINT}/cpus
    - http://${API_ENDPOINT}/hosts
    - http://${API_ENDPOINT}/processes?ip={IP_HOST}
    - http://${API_ENDPOINT}/users?ip={IP_HOST}

## AWS 
``` sh
sam build -t cfn-template/main.yml
sam deploy
```

## Difficulties

1. Run commands on EC2 instances via CloudFormation
2. Define VPC on an EC2 instance via CloudFormation
3. Create API key via CloudFormation

## Future improvements

1. Change MySQL container to AWS RDS MySQL
4. Use AWS Budgets to monitor costs 
5. Use AWS WAF to manage API requests
6. Create API Key via CloudFormation
