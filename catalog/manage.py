from novels_db import Base, BookStoreCategory, Books, OurUsers
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template
from flask import url_for, request, redirect, flash, jsonify
from flask_util_js import FlaskUtilJs

from flask import session as login_session
import random
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import string
import json
from flask import make_response
import requests

app = Flask(__name__)
fujs = FlaskUtilJs(app)

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())[
    'web']['client_id']
APPLICATION_NAME = "Restaurant"


engine = create_engine("sqlite:///books.db",
                       connect_args={'check_same_thread': False},
                       echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.context_processor
def inject_fujs():
    return dict(fujs=fujs)

# ---------------------------Login Example----------------------------------
# Create anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in range(32))
    login_session['state'] = state
    categorys = session.query(BookStoreCategory).all()
    books = session.query(Books).all()
    # return "The current session state is %s" % login_session['state']
    return render_template(
        'login.html',
        STATE=state,
        categorys=categorys,
        books=books,
        categoryName="ALL",
        present_user=login_session)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return str("Hello" + response)

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        print("***************************", user_id)
    login_session['user_id'] = user_id
    flash("LoggedIn Successfully...!", 'success')
    output = '''
<div class='col-sm-offset-4'>
<div class='col-sm-5'>
<div class="panel panel-info animated bounce infinite">
<div class="panel-body">
<center>
<img src="''' + login_session['picture'] + '''" style="width: 100px; height: 100px;border-radius: 50%;">
</center>
<h3 class="text-center text-info">''' + login_session['username'] + '''</h3>
</div>
</div>
</div>
</div>
	'''

    # output += '<h1>Welcome, '
    # output += login_session['username']
    # output += '!</h1>'
    # output += '<img src="'
    # output += login_session['picture']
    # flash("you are now logged in as %s" % login_session['username'])
    # print("done!")
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


def createUser(login_session):
    newUser = OurUsers(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(OurUsers).filter_by(
        email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(OurUsers).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(OurUsers).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None

# @app.route('/gdisconnect')


@app.route('/logout')
def gdisconnect():
    access_token = login_session['access_token']
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s\
    ' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['user_id']
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Your Logged Out Successfully...!", "info")
        return redirect('/')
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response

# ------ Ending  Login & Logout  -----------


# ------ Home , About, CRUD Operation Pages and Functionalitys :)----------
@app.route('/', methods=["GET"])
@app.route('/home', methods=["GET"])
def home():
    categorys = session.query(BookStoreCategory).all()
    books = session.query(Books).all()
    return render_template(
        "home.html",
        categorys=categorys,
        books=books,
        categoryName="ALL",
        present_user=login_session)


@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html")


@app.route('/<categoryName>', methods=['GET'])
def category(categoryName):
    if not categoryName == "ALL":
        AllCategorys = session.query(BookStoreCategory).all()
        category = session.query(BookStoreCategory).filter_by(
            category=str(categoryName)).first()
        categoryUpdate = session.query(BookStoreCategory).all()

        cN = print(categoryName)
        books = session.query(Books).filter_by(category_id=category.id).all()
        if len(books) == 0:
            data = "No Data"
        else:
            data = "Found Data"
        return render_template(
            "home.html",
            categoryName=category,
            myCategory=cN,
            books=books,
            AllCategorys=AllCategorys,
            data=data,
            categoryUpdate=categoryUpdate,
            present_user=login_session)
    elif categoryName == "ALL":
        categorys = session.query(BookStoreCategory).all()
        books = session.query(Books).all()
        return render_template(
            "home.html",
            categoryName="ALL",
            categorys=categorys,
            books=books,
            present_user=login_session)


@app.route("/newBookShelf", methods=["POST"])
def addBookShelf():
    bookShelf = request.form['category'].title().strip()
    if (int(request.form['present_id']) == int(login_session['user_id'])):
        if request.method == "POST":
            verifyField = session.query(BookStoreCategory).filter_by(
                category=bookShelf).count()
            # print(verifyField,bookShelf)
            if (verifyField == 0) and (bookShelf.upper() != "ALL"):
                # print(verifyField,bookShelf)
                # print("---------------------------------------",bookShelf)
                # present_id = int(login_session['user_id'])
                bookShelf = BookStoreCategory(
                    category=bookShelf, ourUser_id=int(
                        request.form['present_id']))
                session.add(bookShelf)
                session.commit()
                return redirect('/')
            else:
                return jsonify({'error': "Data Not Saved"})
        else:
            return jsonify({'error': "Data Not Saved"})
    else:
        return jsonify({'error': "User Not Exist"})
    return jsonify({'error': "Data Not Saved"})


@app.route("/updateBookShelf", methods=["POST"])
def updateShelf():
    if (int(request.form['present_id']) == int(login_session['user_id'])):
        if request.method == "POST":
            editBookShelf = session.query(BookStoreCategory).filter_by(
                id=request.form['shelfId']).one()
            editBookShelf.category = request.form['shelfName']

            editBookType = session.query(Books).filter_by(
                bookType=request.form['beforeShelf']).all()
            for i in range(0, len(editBookType)):
                editBookType[i].bookType = request.form['shelfName']
            session.commit()
            return redirect('/')
        else:
            return jsonify({'error': "Data Not Saved"})
    else:
        return jsonify({'error': "No User Exist"})

    return jsonify({'error': "Data Not Saved"})


@app.route("/deleteBookShelf", methods=["POST"])
def deleteShelf():
    if (int(request.form['present_id']) == int(login_session['user_id'])):
        if request.method == "POST":
            deleteBookShelf = session.query(
                BookStoreCategory).filter_by(id=request.form['shelfId'])
            # print("**************************",deleteBookShelf.category)
            deleteBookShelf.delete()

            deleteBookType = session.query(Books).filter_by(
                bookType=request.form['shelfName'])
            # for i in range(0,len(deleteBookType)):
            deleteBookType.delete()
            # print("*************************",deleteBookType[i])
            session.commit()
            return redirect('/')
        else:
            return jsonify({'error': "Data Not Saved"})
    else:
        return jsonify({'error': "No User Exist"})
    return jsonify({'error': "Data Not Saved"})


@app.route("/allJSON", methods=["GET"])
def AllJSON():
    bookShelf = session.query(BookStoreCategory).all()
    books = session.query(Books).all()

    bookShelfSerial = [shelf.serialize for shelf in bookShelf]
    for myShelf in range(len(bookShelfSerial)):
        SingleBooks = [sBook.serialize for sBook in session.query(
            Books).filter_by(category_id=bookShelfSerial[myShelf]["id"])]
        if SingleBooks:
            bookShelfSerial[myShelf][bookShelfSerial[myShelf]
                                     ['category']] = SingleBooks
    # booksSerial=[book.serialize for book in books ]

    # AllBookShelfs_Books=[
    # shelf['category']
    # [book.serialize].serialize
    # for shelf,book in (bookShelf, books)]

    # return jsonify(
    # AllBookShelfs_Books=
    # [ shelf.serialize for shelf in bookShelf],
    # Books=[book.serialize for book in books ])
    # return jsonify(
    # AllBookShelfs_Books=[ shelf.serialize
    # for shelf in bookShelf],
    # Books=[book.serialize for book in books ])
    # return jsonify
    # (AllBookShelfs_Books=[bookShelfSerial,booksSerial])
    return jsonify(AllBookShelfs_Books=bookShelfSerial)


@app.route("/showAllBookShelf/JSON", methods=["GET"])
def showAllBookShelf():
    booksStores = session.query(BookStoreCategory).all()
    return jsonify(
        AllBookShelfs=[
            booksCategory.serialize for booksCategory in booksStores])


@app.route("/showSingleBookShelf/<bookShelf>/JSON", methods=["GET"])
def showSingleBookShelf(bookShelf):
    if bookShelf == "ALL":
        bookShelf = "ALL"
        jsonBooksShelf = session.query(BookStoreCategory).all()
        jsonShelfOut = {
            "AllBooksShelf": [
                shelf.serialize for shelf in jsonBooksShelf]}
    else:
        jsonBooksShelf = session.query(
            BookStoreCategory).filter_by(category=bookShelf)
        jsonShelfOut = {
            bookShelf +
            " BooksShelf": [
                shelf.serialize for shelf in jsonBooksShelf]}
    return jsonify(jsonShelfOut)


@app.route('/newBook', methods=['POST'])
def addNewBook():
    title = request.form["title"]
    author = request.form["author"]
    bookType = request.form['bookType']
    # if  (int(request.form['present_id']) ==  int(login_session['user_id'])):
    if request.method == "POST":
        if title and author and bookType:
            books = Books(title=request.form["title"],
                          author=request.form["author"],
                          bookType=request.form["bookType"],
                          description=request.form["description"],
                          publishedDate=request.form["publishedDate"],
                          publisher=request.form["publisher"],
                          imageLinks=request.form["imageLinks"],
                          infoLink=request.form["infoLink"],
                          category_id=request.form["category_id"],
                          ourUser_id=login_session['user_id'])
            # ourUser_id= int(request.form['present_id'])
            session.add(books)
            session.commit()
            # flash("New Book Created @:"+request.form['bookType'])
            return redirect('/')
        else:
            return jsonify({'error': "Data Not Saved"})
    else:
        return jsonify({'error': "Data Not Saved"})
    return jsonify({'error': "Data Not Saved"})


@app.route('/booksUpdates', methods=["POST"])
def booksUpdate():
    print(
        "-----------------------",
        request.form['id'],
        request.form['title'],
        request.form['category_id'])
    if request.method == "POST":
        editBook = session.query(Books).filter_by(id=request.form['id']).one()
        editBook.title = request.form['title']
        editBook.author = request.form['author']
        editBook.bookType = request.form['bookType']
        editBook.description = request.form['description']
        editBook.publishedDate = request.form['publishedDate']
        editBook.publisher = request.form['publisher']
        editBook.imageLinks = request.form['imageLinks']
        editBook.infoLink = request.form['infoLink']
        editBook.category_id = request.form['category_id']

        session.add(editBook)
        session.commit()
        return redirect('/')
    else:
        return jsonify({'error': "Data Not Saved"})
    return jsonify({'error': "Data Not Saved"})


@app.route('/removeBooks', methods=['POST'])
def booksDelete():
    if request.method == "POST":
        delBooks = session.query(Books).filter_by(id=request.form['id'])
        # print('---------------------------------------',delBook.id)
        delBooks.delete()
        session.commit()
        return redirect('/')
    else:
        return jsonify({'error', "Data Not Deleted"})
    return jsonify({'error', "Data Not Deleted"})


@app.route("/showAllBooks/<bookName>/JSON", methods=["GET"])
def showAllBooksJSON(bookName):
    if bookName == "ALL":
        bookName = "ALL"
        jsonBooks = session.query(Books).all()
        jsonOut = {"AllBooks": [book.serialize for book in jsonBooks]}
    else:
        jsonBooks = session.query(Books).filter_by(bookType=bookName)
        jsonOut = {bookName + " Books": [book.serialize for book in jsonBooks]}
    return jsonify(jsonOut)

# @app.route('/login', methods=["GET","POST"])
# def login():
# 	if request.method == "POST":
# 		return "LogIn Data"
# 	return render_template("login.html")


if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'e7a9804ba98684deefd88d6a6c8cd0db'
    app.debug = True
    app.run(host="0.0.0.0", port=5001)


# Udacity Google New Sigin Functionality
# https://knowledge.udacity.com/questions/33052
