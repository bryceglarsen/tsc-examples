# Using Tableau Server Client
This repository provides some examples for TSC by Tableau.  
Official documentation can be found [here](https://tableau.github.io/server-client-python/docs/) and [GitHub](https://github.com/tableau/server-client-python)  
Below are some initial set-up steps I'd recommend.

## Tableau Developer Program
Check out the new Developer Portal [here](https://tableau.com/developer)  
These examples are based on the use of a [free Sandbox](https://www.tableau.com/developer/get-site) through the program

## Fork Sample Repo
I’d recommend [forking the repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo) for ease of following along  
and then clone to your computer. Once that’s done, navigate to the root of the repository.

## Use pyenv to set python version locally
Intro to pyenv [here](https://realpython.com/intro-to-pyenv/)
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
For more information about why visit [this link](https://medium.com/python-pandemonium/better-python-dependency-and-package-management-b5d8ea29dff1)
```bash
pip install -r requirements.txt
```

## Create .env file
An .env file is a great way to host your credentials and avoid entering over and over.
Here we'll be using Personal Access Tokens for authentication. [Create Tokens](https://help.tableau.com/current/server/en-us/security_personal_access_tokens.htm#create-tokens)

```bash
tokenName='TokenName'
tokenSecret='TokenSecret'
url='https://10ax.online.tableau.com'
site='SiteName'
```

## Create New Projects
Make new projects to use
```bash
python 0_setup/CreateProjects.py
```
