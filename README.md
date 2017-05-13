# AWS-lambdas-python

A project to create and upload lambda functions. 
At the moment, the deployment manager is in progress. 

### project's path


```
├── sttc/
│   ├── aws
│   │   ├── config
│   │   │   ├── ConfigProvider.py       : provider of the configuration in it's resources
│   │   │   ├── Regions.py              : manager of different regions of AWS
│   │   ├── service
│   │   │   ├── *Manager.py            : managers of AWS' services like Lambda, IAM 
│   │   ├── resource
│   │   │   ├── defaultConf.json        : contains every general values like arn of policies, 
│   │   │                                   general roles for lambda creation
│   │   │   ├── privateConf.json        : not on GitHub: contains private data
│   │   │   ├── privateConfExample.json : list of every field of privateConf.json with mock data
│   ├── deploy
│   │   ├── Deploy.py                   : Run this to deploy the project
│   │   │   ├── resources
│   │   │   │   ├── deployConfig.json   : contains what's needed to configure the deployer, 
│   │   │                                   like lambda's validation config
│   │   ├── service  
│   │   │   ├── *.py                   : services needed by the deployer  
│   ├── iam                             : actually unused right now ;-)
│   ├── lambda                           
│   │   ├── <DirectoryName>             : each directory contains one and only one lambda
│   │   │   ├── deployConfig.json       : contains every data needed by the deployer
```
