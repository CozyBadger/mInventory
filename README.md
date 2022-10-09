# (WIP!) mInventory
Refactor for FastAPI

A simple application to manage an inventory

## Run local development environment
### Server
* make sure python3.X-venv is installed\
`$ sudo apt install python3.8-venv`

* within the repo directory run\
`$ python -m venv .venv`

* source the virtual environment\
`$ . .venv/bin/activate`

* install requirements\
`$ pip install -r requirements.txt`

* start local http server\
`$ uvicorn main:app --reload`

* leave the virtual environment when needed\
`$ deactivate`
