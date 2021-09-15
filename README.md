# Using Tableau Server Client
This repository provides some examples for TSC by Tableau.
Below are some initial set-up steps I'd recommend.

## Tableau Developer Program
Check out the new Developer Portal here: https://tableau.com/developer  
These examples are based on the use of a free Sandbox through the program: https://www.tableau.com/developer/get-site

## Use pyenv to set python version locally
Intro to pyenv: https://realpython.com/intro-to-pyenv/
```bash
brew install pyenv
pyenv local 3.9.1
# use this to check version:
pyenv versions
```

## Make virtual environment and activate
```bash
python -m venv venv
souce venv/bin/activate
```

## Install dependencies
For more information about why: https://medium.com/python-pandemonium/better-python-dependency-and-package-management-b5d8ea29dff1
```bash
pip install -r requirements.txt
```

## Create .env file
```bash
tokenName='TokenName'
tokenSecret='TokenSecret'
url='https://10ax.online.tableau.com'
site='SiteName'
