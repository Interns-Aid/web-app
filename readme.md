### Interns Aid (Help)
InternsAid was developed to collect internship questions asked by companies. The questions can be of home  and coding assignment type on the web platform. Anyone can add questions that have been asked.

[![CI](https://github.com/Interns-Aid/web-app/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Interns-Aid/web-app/actions/workflows/ci.yml) [![Deployment](https://github.com/Interns-Aid/web-app/actions/workflows/deploy.yml/badge.svg)](https://github.com/Interns-Aid/web-app/actions/workflows/deploy.yml) ![Codecov](https://img.shields.io/codecov/c/github/Interns-Aid/web-app) 

### Prerequisite
Project uses [black](https://github.com/psf/black) to format code and [flake8](https://github.com/PyCQA/flake8) for lint. [pre-commit](https://pre-commit.com/) has been used to run lint and format code before any commit.
 ```shell 
 pip install black flake8 pre-commit 
 pre-commit install
```

### Run Test Locally
```shell
# Install Tox
pip install tox

# run tests 
tox
```
### Contribution
This project is still in the development phase. The aim is to build a platform that provides all the necessary resources for a good preparation for an internship. You can work on any part of the application (frontend, backend, admin).
