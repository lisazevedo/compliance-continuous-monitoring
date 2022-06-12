# Compliance Continuous Monitoring

## Premise

## Problem

## Solution
![DB diagram](/images/template.png)

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
2. ```python3 agent.py so-name```
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

## Difficulty

## Future improvements

1. Change MySQL container to AWS RDS
2. Change ImageId, in CloudFormation template, from static to dinamic variable
3. Change CloudFormation to Terraform
4. Use AWS Budgets to monitor costs 
5. Use AWS WAF to manage API requests