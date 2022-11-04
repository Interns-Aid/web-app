### InternsAid
#### Internsaid = Intern's + AID (Help)

Interns Aid is for interns to prepare for a technical internship. An internship is the first step towards a career in the technical field. Most students leave the internship early because it is difficult to pass the technical tests required by the companies. It is stressful when you have no idea what to work on.

It is built to collect internship questions asked by companies. The questions can be homework or coding assignment type on the web platform. Anyone can add questions that have been asked.

Most companies also require a portfolio as a prerequisite. On this platform there will be volunteer mentors who will guide you on projects.

[![CI](https://github.com/Interns-Aid/web-app/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Interns-Aid/web-app/actions/workflows/ci.yml) [![Deployment](https://github.com/Interns-Aid/web-app/actions/workflows/deploy.yml/badge.svg)](https://github.com/Interns-Aid/web-app/actions/workflows/deploy.yml) ![Codecov](https://img.shields.io/codecov/c/github/Interns-Aid/web-app) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Interns-Aid/web-app/blob/4cca3c0e9a1fa921710f0aa0c9536191b96cbacd/LICENSE.md)



### Prerequisite
Project uses [black](https://github.com/psf/black) to format code and [flake8](https://github.com/PyCQA/flake8) for lint. [pre-commit](https://pre-commit.com/) has been used to run lint and format code before any commit.
 ```shell 
 pip install black flake8 pre-commit 
 pre-commit install
```

### Run Application
1. Prepare `.env` file <br/>
Make a copy of `.env_example`, rename into .env and change values as per your environment
2. Run Flask APP
````shell
export FLASK_APP=wsgi.py
flask run
````

### Run Test Cases
```shell
# Install Tox
pip install tox

# run tests 
tox
```
### API Documentation
```shell
http://localhost:5000/swagger-ui/
```

### Contribution
The goal is to build a platform that provides all the necessary resources for the preparation of a technical internship. This platform consists of different applications: Frontend, Backend, UI /UX, Admin. If you are interested in any part of the application, you can write me [rajesh.k.khadka] on gmail. If you are looking for an internship, I highly recommend you to work on it as it will boost your resume.