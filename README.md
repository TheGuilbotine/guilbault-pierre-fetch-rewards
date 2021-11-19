The following application is written in Python using Flask. In lieu of using models and forms to check data before going to the database we are using local storage and conditional statements. Refactoring will be necessary to check requests for good data. As of now the PUT route is not fully functional. But you will find that the GET and POST routes act as expected.

To install dependencies used for this application use:
```bash
pipenv install
```
Once dependencies are installed you may run the following command in the terminal.
```bash
flask run
```
Once the application is running HTTP requests can be made using [Postman](https://www.postman.com/downloads/),  a great desktop app for testing your backend routes.

An HTTP request can be sent using GET to localhost:5000/ . The GET request will return all balances currently in the users BALANCES database. This will be an empty object if no POSTs have been sent to the application.

The POST route is localhost:5000/transaction . A request can be sent in the body using a Python dictionary (object) with the key words "payer" and "points" with respective payer name and points acquired or spent as the values. The application will create a timestamp based on UTC time for the data as it passes it to the TRANSACTIONS database (local storage) a function will then check the BALANCES database (local storage) for any payers of that name, if that payer already exists for the user then the points will be added or subtracted from the current points amount for that payer. Otherwise a new data column will be added to the database.

The PUT route localhost:5000/spend_points is currently under construction. Trouble working with the data and and altering it accordingly has proven problematic. More time will need to be spent debugging.
However the PUT route will take the incoming data object keyword "points" with respective points value as a positive number. The route will copy the TRANSACTIONS data into a new list, ordering it based on timestamp. Once the data is ordered from oldest to newest the route will search through each row as long as there are points to spend. It will alter the amount of points spent based on each transaction and then query the BALANCES database to update each column accordingly. The end result should be un updated balance(s) based on the transactions made and when they were made and points to be sent reaching zero. No balance should be negative.
