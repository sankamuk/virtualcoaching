# virtualcoaching

![Ansible](https://img.shields.io/badge/IAC-Ansible-brightgreen.svg)
![Python](https://img.shields.io/badge/Backend-PythonFlask-brightgreen.svg)
![React](https://img.shields.io/badge/Frontend-ReactJS-brightgreen.svg)

This is an application (ExamNow) designed to help registered user to give examination anywhere, anytime and check his/her preparation. 

## Technology Used:
- Python (Flask) 
- React JS

## Directory Layout

`api`
This is the Flask based backend to expose the API supporting the core functionalities.

`ui`
This is the React JS based frontend for the application using with user interacts with the backend.

`ansible`
This is the Ansible setup to deploy the application to any CentOS(tested on v7) host.

## Deployment Process

*Below steps to follow.*

  - Update hosts file ansible/dev/hosts and add your hostname in place of `client`. Also note the host should have a user ansible and its should have sudo right. Also the host should be password less login enabled with user ansible from your current host from where you will run this Ansible recipe.

  - Execute following command.
    ``` ansible-playbook -i dev/hosts dev/deploy.yml ```
