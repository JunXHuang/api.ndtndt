## An ebay like Proxy Bidding System [backend]  

View at : https://ndtndt.azurewebsites.net

#### ndtndt - NOT DUE TODAY, NOT DO TODAY  

###### Rest API backend for NDTNDT project. 

###### Frontend is at (https://github.com/NazimAmin/ndtndt)

  - Includes multiple system level service roles.
  - Options such as add/edit/delete, search, filter, bid, report etc. with an intuitive look.

Technology used:
 - Front-end - AngularJS
 - [Backend REST  - Python](https://github.com/NazimAmin/api.ndtndt)  
 - DB - SQL Server

## Build & development & Dependencies front-end

Clone `git clone https://github.com/NazimAmin/ndtndt` - 

Run `npm install` to install node_modules

Run `bower install` to install bower_components

Run `grunt ` for building and `grunt serve` for preview.

## Build & development & Dependencies backend

Clone `git clone https://github.com/JunXHuang/api.ndtndt` - 

Run `pip install -r requirement.txt`

Run `Python api.py`

Change database connection string to whichever connection you have in https://github.com/JunXHuang/api.ndtndt/blob/master/ndtndt/ndtndt/ndtndt/__init__.py

Run tablequery.sql, insertquery.sql, and trigger.sql to populate the database
https://github.com/JunXHuang/api.ndtndt/tree/master/ndtndt/db

## Contributors

<> with :hotsprings: by [@Nazim](http://github.com/nazimamin) [@Jun Huang](http://github.com/JunXHuang)





