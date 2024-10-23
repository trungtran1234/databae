# Databae - Powered By SingleStore
Databae is your personal AI assistant when it comes to being able to explore and analyze your SingleStore database with human language. Tell Databae what you want to query your SingleStore database in human language, and Databae will automatically query the database, analyze the dataset, and visualize the results for you to understand.

## Diagram
<img src="https://github.com/user-attachments/assets/cb7e0d4d-fae8-4bea-bcdf-f2a91b8f8bb5" width="500" title="Ray Romano saying What do you think?" alt="Ray Romano saying What do you think?"/>

## Instructions 
### Frontend 
* Install [npm](https://nodejs.org/en)
* Change directory into the folder ```frontend``` and run ```npm install``` to install all the dependencies
* Run the command ```npm run dev```

### Backend
* Install [Python](https://www.python.org/) (minimum version 3.10)
* Install [Poetry & Pipx](https://python-poetry.org/).
* Run ```poetry shell``` and ```poetry install```
* Make a .env file consisting to store the Groq API key
```GROQ_API_KEY=GRAB YOUR API KEY FROM GROQ```
* For backend, open up two terminals. Change into the directory folder ```backend``` and run ```uvicorn server:app --reload``` on terminal 1 and run ```python agents.py``` on terminal 2. Depending on your operating system, it
could be python or python3. 

## Use Cases
* Connect to any SingleStore database to visualize data
* Generate a pie chart based off data in the database
* Generate a table based off data in the database
* Generate a plaintext response based off data in the database

## Audience
Anyone, whether SQL wizards or not, can use it. Type in plain English, and we generate the queries and visualize the data for you.
* Are you in the medical industry? Do you want to visualize the amount of usage of medication A within each age group? Tell Databae!
* Are you in the education industry? Do you want to know the grades of every student? Tell Databae!
* Are you in the music industry? Do you want to make a pie chart that visualizes how many tracks each artist has created? Tell Databae!


