from flask import Flask, request, session, render_template, jsonify, redirect, url_for
from constants import CONSUMER_ID, CONSUMER_SECRET, APP_SECRET
from flask.ext.mysql import MySQL
from pprint import pprint
import requests
import json
"""
This file contains all the functions and routes for our demo app.
"""
app = Flask(__name__)
# comment out when you're done testing
app.debug = True
app.secret_key = APP_SECRET #a secret string that will sign your session cookies

mysql = MySQL()
mysql.init_app(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'ErnieBrain'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

qSet = [
"INSERT INTO groups (ownerId, user1, user2, user3, user4, user5, user6, user7, user8, user9, user10) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')",
"INSERT INTO groups (ownerId, user1, user2, user3, user4, user5, user6, user7, user8, user9) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')",
"INSERT INTO groups (ownerId, user1, user2, user3, user4, user5, user6, user7, user8) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')",
"INSERT INTO groups (ownerId, user1, user2, user3, user4, user5, user6, user7) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s')",
"INSERT INTO groups (ownerId, user1, user2, user3, user4, user5, user6) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s')",
"INSERT INTO groups (ownerId, user1, user2, user3, user4, user5) VALUES (%d, '%s', '%s', '%s', '%s', '%s')",
"INSERT INTO groups (ownerId, user1, user2, user3, user4) VALUES (%d, '%s', '%s', '%s', '%s')",
"INSERT INTO groups (ownerId, user1, user2, user3) VALUES (%d, '%s', '%s', '%s')",
"INSERT INTO groups (ownerId, user1, user2) VALUES (%d, '%s', '%s')"
]

"""
This is the function that will be called when users
visit the home page.

app.route is a function decorator. It takes a URI as an argument, and
whenever a user requests that url, the function it decorates will get called.
In this case, if your app was at www.myapp.com, then someone visiting
www.myapp.com or www.myapp.com/index.html would cause the flask app to call
the index() function. For more information about the app.route decorator
check out http://flask.pocoo.org/docs/quickstart/#routing.
"""
@app.route('/')
@app.route('/index.html')
def index():
    if session.get('venmo_token'):
        data = {'name': session['venmo_username'],
                'id': session['venmo_id'],
                'consumer_id': CONSUMER_ID,
            'access_token': session['venmo_token'],
            'signed_in': True}
        conn = mysql.connect()
        cursor = conn.cursor()

        #db_data = cursor.fetchone()
        #if db_data is None:
        try:
            query = "INSERT INTO user_tbl (username) VALUES ('%s')" % data['name']
            cursor.execute(query)
            conn.commit()
        except:
            pass

        # get lists
        currUser = session['venmo_username']
        query = "SELECT id FROM user_tbl WHERE username = '%s'" % currUser
        cursor.execute(query)
        conn.commit()

        currId = int(cursor.fetchone()[0])

        listQuery = "SELECT * FROM groups WHERE ownerId = %d" % currId
        cursor.execute(listQuery)
        conn.commit()

        lists = cursor.fetchall()
        returnLists = map(list, lists)
        listDicts = []
        count = 1
        for entry in returnLists:
            localDict = {}
            smallCount = 0
            for smallEntry in entry:
                if smallCount == 0:
                    smallCount = smallCount + 1
                elif smallCount == 1:
                    smallCount = smallCount + 1
                else:
                    smallKey = str(smallCount - 1)
                    localDict[smallKey] = smallEntry
                    smallCount = smallCount + 1
            listDicts.append(localDict)
            count = count + 1
        return render_template('/signedIn.html', data=data, returnLists=listDicts)
    else:
        data = {'signed_in': False,
        'consumer_id': CONSUMER_ID}
        return render_template('/index.html', data=data)

@app.route('/make_group', methods=["POST"])
def make_group():
    conn = mysql.connect()
    cursor = conn.cursor()
    
    group = request.form['group_raw']
    group_split = group.split(',')
    #access_token = request.args.get('access_token')
    #print access_token
    forKeyQ = "SELECT id FROM user_tbl WHERE username = '%s'" % session['venmo_username']
    cursor.execute(forKeyQ)
    conn.commit()

    forKey = cursor.fetchone()[0]

    for user in group_split:
        url = 'https://api.venmo.com/v1/users/' + user + '?access_token=' + session['venmo_token']
        response = requests.get(url)
        if 'error' in response.json():
            if response.json()['error']['code'] == 283:
                return 'Bad user, check %s' % user
        elif user == session['venmo_username']:
            return 'Cannot list yourself!'
    group_split.insert(0, forKey)
    number = 8 - (len(group_split) - 3)
    query = qSet[number] % tuple(group_split)
    cursor.execute(query)
    conn.commit()
    return 'Successfully created new list'

@app.route('/get_groups', methods=["GET"])
def get_groups():
    currUser = session['venmo_username']
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT id FROM user_tbl WHERE username = '%s'" % currUser
    cursor.execute(query)
    conn.commit()

    currId = int(cursor.fetchone()[0])

    listQuery = "SELECT * FROM groups WHERE ownerId = %d" % currId
    cursor.execute(listQuery)
    conn.commit()

    lists = cursor.fetchall()
    returnLists = map(list, lists)
    print returnLists
    return render_template('signedIn.html')

@app.route('/make_group_payment', methods=["POST"])
def make_group_payment():
    groupUsernames = request.form['groupUsernames']
    note = request.form['groupNote']
    amount = request.form['groupAmt']

    payload = {
        "access_token":session['venmo_token'],
        "note":note,
        "amount":amount,
    }
    amountNum = float(amount)

    usernameList = groupUsernames.split(',')
    toReturn = ''
    count = 0
    for user in usernameList:
        url = 'https://api.venmo.com/v1/users/' + user + '?access_token=' + session['venmo_token']
        response = requests.get(url).json()
        pprint(response)
        payload['user_id'] = response['data']['id']
        pprint(payload)
        url = "https://api.venmo.com/v1/payments"
        response = requests.post(url, payload)
        data = response.json()
        if 'error' in data:
            return jsonify(data)
        pprint(data)
        if count < (len(usernameList) - 1):  
            if amountNum < 0.00:
                temp = "PAID %s to %s with the message: '%s'\n" % ("{0:.2f}".format(abs(amountNum)), user, note)
            else:
                temp = "CHARGED %s to %s with the message: '%s'\n" % ("{0:.2f}".format(abs(amountNum)), user, note)
        else:
            if amountNum < 0.00:
                temp = "PAID %s to %s with the message: '%s'" % ("{0:.2f}".format(abs(amountNum)), user, note)
            else:
                temp = "CHARGED %s to %s with the message: '%s'" % ("{0:.2f}".format(abs(amountNum)), user, note)
        toReturn = toReturn + temp
        count = count + 1

    return toReturn

"""
Example app endpoints to make HTTP requests to a third party API.
In this example, we make POST and GET requests to the Venmo API to
make a sandbox payment and get your 20 most recent payments on Venmo, respectively.
"""
@app.route('/make_payment', methods=["POST"])
def make_payment():
    """
    the 'request' object will contain all information about
    the POST request, including the HTTP status code, the method,
    the url arguments and the POST data.
    take a look at http://flask.pocoo.org/docs/quickstart/#the-request-object
    for more info.

    request.form will have all the information that the incoming post request.
    In this example, our app makes a POST request to /make_payment, and we grab
    those parameters to make a call to the Venmo payments endpoint.
    """
    access_token = request.form['access_token']
    note = request.form['note']
    email = request.form['email']
    amount = request.form['amount']

    """
    the payload contains all the information we are going to send in our
    post request when we make a payment with the Venmo API.
    """
    payload = {
        "access_token":access_token,
        "note":note,
        "amount":amount,
        "email":email
    }

    url = "https://api.venmo.com/payments"
    response = requests.post(url, payload)
    data = response.json()
    return jsonify(data)

@app.route('/get_payments', methods=["GET"])
def get_payments():
    access_token = request.args.get('access_token')
    url = "https://sandbox-api.venmo.com/payments?access_token=" + access_token
    response = requests.get(url)
    data = response.json()
    return jsonify(data)

@app.route('/get_friends', methods=["GET"])
def get_friends():
    access_token = request.args.get('access_token')
    friends = {}
    url = "https://sandbox-api.venmo.com/v1/users/" + session['venmo_id'] + "/friends?access_token=" + access_token
    response = requests.get(url)
    data = response.json()
    for friend in data['data']:
        friends[friend['display_name']] = friend['id']
    return jsonify(friends)


"""
Example app endpoint that will handle OAuth server-side authentication.
This is the endpoint that Venmo will redirect once a user has successfully logged
in to your Venmo app. For more information on Venmo OAuth and the whole flow, check out
beta-developer.venmo.com/oauth.
"""
@app.route('/oauth-authorized')
def oauth_authorized():
    """
    You can use request.args to get URL arguments from a url. Another name for URL arguments
    is a query string.
    What is a URL argument? It's some data that is appended to the end of a url after a '?'
    that can give extra context or information.

    """
    AUTHORIZATION_CODE = request.args.get('code')
    data = {
        "client_id":CONSUMER_ID,
        "client_secret":CONSUMER_SECRET,
        "code":AUTHORIZATION_CODE
        }
    url = "https://api.venmo.com/v1/oauth/access_token"
    response = requests.post(url, data)
    response_dict = response.json()
    access_token = response_dict.get('access_token')
    user = response_dict.get('user')

    session['venmo_token'] = access_token
    session['venmo_username'] = user['username']
    session['venmo_id'] = user['id']

    return redirect(url_for('index'))

"""
Going to this url will delete the current session
and redirect back to the home page.
"""
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
