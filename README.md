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

The PUT route localhost:5000/spend_points . A request can be made with a object body using a key of "points" and a value to the amount of points to be spent. The route will order all transaction made from oldest to newest and create a list of all points in the Balances database(local storage). It creates the list of transactions so that it may compare each transaction to the database subtracting points from the balances in the order they were made. The balance points list is used to check that there are points left to spend. The route will then do a series of conditionals to check that there are sufficient points to spend, that there have been transactions, and that all points in balances are not zero. After which it will go through each transaction first checking that the points spent is less than the total points available to spend. Then creating a variable called pointsToSpend with the value either being the points left to spend or the transaction amount depending on whether or not it would exceed the transaction amount. After the route is called with a correct amount the balances will be returned with the new points remaining.
