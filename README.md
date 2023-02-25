# Take-Home Assignment

The goal of this take-home assignment is to evaluate your abilities to use API, data processing and transformation, SQL, and implement a new API service in Python.


## How to Run
1. To build and run the project with Docker Compose, open a terminal window in the root directory of project and run the following command:
```
docker-compose up --build
```
2. This will start the application and print the logs to the console. To stop the application, press Ctrl+C.

3. Run the following command to retrieve the financial data of Two given stocks (IBM, Apple Inc.)for the most recently two weeks:
```
python get_raw_data.py
```
   Users can replace with their AlphaVantage API key in `get_raw_data.py`
   
4.  Run the application in the background:
```
docker-compose up -d
```
5. Now users can can make requests to http://localhost:5000. 
   For example, to get financial data from the API:
```
http://localhost:5000/api/financial_data?symbol=AAPL&start_date=2023-02-01&end_date=2023-03-01
```
   
   Make a request to get statistics by running:
```
http://localhost:5000/api/statistics?symbol=AAPL&start_date=2023-02-01&end_date=2023-03-01
```


## Tech stack
### Flask
### Flask-SQLAlchemy
### SQLite