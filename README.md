# (WIP!) mInventory
Refactor for FastAPI
A simple application to manage an inventory

## Run local development environment
### Database
* have sqlite3 installed on your system\
`$ sudo apt install sqlite3`

* create a local db and ingest storage schema (drops table if it exists)\
`$ sqlite3 minventory.db < ./schemas/storage.sql`\
TODO: create script to automate db stuff

### Server
* make sure python3.X-venv is installed\
`$ sudo apt install python3.8-venv`

* within the repo directory run\
`$ python -m venv .faenv`

* source the virtual environment\
`$ . .faenv/bin/activate`

* install requirements\
`$ pip install -r requirements.txt`

* start local http server\
TODO!

* leave the virtual environment when needed\
`$ deactivate`
