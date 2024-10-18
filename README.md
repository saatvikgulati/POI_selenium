# There are 2 scripts in this repo

## Both scripts use selenium to go to the website and fetch the addresses

For the first one it goes to a url and fetches all the UK, London Store locations

For the second one it goes to the pepperfry website and traverses across all the store location cities and fetches there addresses

### In both cases the results are stored in a csv file using pandas data frame under data folder

> There are question and answer txt file and a few sql queries answering questions

To run the task files first initialize virtualenv `python -m venv .venv` or `python3 -m venv .venv`
### For Windows
`.venv\Scripts\activate.bat`
`pip install -r requirements.txt`
`python POI_task_1.py` or `python3 POI_task_1.py`
`python POI_task_2.py` or `python3 POI_task_2.py`

### For Linux
`source .venv/bin/activate`
`pip install -r requirements.txt`
`python POI_task_1.py` or `python3 POI_task_1.py`
`python POI_task_2.py` or `python3 POI_task_2.py`