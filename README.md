CyberErnie - a webapp dedicated to enabling saved group payments via the Venmo API.
===============================================================================
Documentation
-----------
A Flask app that allows saved group payments via the Venmo API. After a user logs in, he/she is able to create chargable groups that are persistent across sessions.

Venmo API documentation available [here](http://venmo.com/api).

Flask documentation available [here](http://flask.pocoo.org/).

Bootstrap documentation available [here](http://getbootstrapcom/).

Jinja2 documentation available [here](http://jinja.pocoo.org/docs/).

jQuery documentation available [here](http://jquery.com/).

Setup
-----------
Clone this repo to a local directory on your computer. Navigate to the directory.

Install flask and requests

    pip install -r requirements.txt

Run a setup script to create a couple of useful constants for your app, include a key to encrypt your sessions
and placeholders for Venmo app credentials.
`python setup.py`

How to run
-----------
Go into the app main directory and
run `python main.py`
That's all (make sure you have that constants file, constants.py, and you have installed those libraries mentioned above)!


That's it!
----------
Now get charging!

TODO!
----------
Create a more robust relational DB to eliminate list size cap

~~JSON list implementation (eliminating list size cap)~~

Overhaul front-end design for payments screen
