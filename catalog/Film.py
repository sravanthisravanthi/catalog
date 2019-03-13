
from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Film_setup import Base, FilmCategoryName, FilmName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///films.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Films Collection"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
fis_cat = session.query(FilmCategoryName).all()


# login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    fis_cat = session.query(FilmCategoryName).all()
    fies = session.query(FilmName).all()
    return render_template('login.html',
                           STATE=state, fis_cat=fis_cat, fies=fies)


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
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

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
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
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

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(User1)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

#####
# Home


@app.route('/')
@app.route('/home')
def home():
    fis_cat = session.query(FilmCategoryName).all()
    return render_template('myhome.html', fis_cat=fis_cat)

#####
# Film Category for admins


@app.route('/FilmStore')
def FilmStore():
    try:
        if login_session['username']:
            name = login_session['username']
            fis_cat = session.query(FilmCategoryName).all()
            fis = session.query(FilmCategoryName).all()
            fies = session.query(FilmName).all()
            return render_template('myhome.html', fis_cat=fis_cat,
                                   fis=fis, fies=fies, uname=name)
    except:
        return redirect(url_for('showLogin'))

######
# Showing films based on film category


@app.route('/FilmStore/<int:filid>/AllFilms')
def showFilms(filid):
    fis_cat = session.query(FilmCategoryName).all()
    fis = session.query(FilmCategoryName).filter_by(id=filid).one()
    fies = session.query(FilmName).filter_by(filmcategorynameid=filid).all()
    try:
        if login_session['username']:
            return render_template('showFilms.html', fis_cat=fis_cat,
                                   fis=fis, fies=fies,
                                   uname=login_session['username'])
    except:
        return render_template('showFilms.html',
                               fis_cat=fis_cat, fis=fis, fies=fies)

#####
# Add New Film


@app.route('/FilmStore/addFilmName', methods=['POST', 'GET'])
def addFilmName():
    if request.method == 'POST':
        category = FilmCategoryName(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(category)
        session.commit()
        return redirect(url_for('FilmStore'))
    else:
        return render_template('addFilmName.html', fis_cat=fis_cat)

########
# Edit Film Category


@app.route('/FilmStore/<int:filid>/edit', methods=['POST', 'GET'])
def editFilmCategory(filid):
    editFilm = session.query(FilmCategoryName).filter_by(id=filid).one()
    creator = getUserInfo(editFilm.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Film Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('FilmStore'))
    if request.method == "POST":
        if request.form['name']:
            editFilm.name = request.form['name']
        session.add(editFilm)
        session.commit()
        flash("Film Category Edited Successfully")
        return redirect(url_for('FilmStore'))
    else:
        # fis_cat is global variable we can them in entire application
        return render_template('editFilmCategory.html',
                               fi=editFilm, fis_cat=fis_cat)

######
# Delete Film Category


@app.route('/FilmStore/<int:filid>/delete', methods=['POST', 'GET'])
def deleteFilmCategory(filid):
    fi = session.query(FilmCategoryName).filter_by(id=filid).one()
    creator = getUserInfo(fi.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Film Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('FilmStore'))
    if request.method == "POST":
        session.delete(fi)
        session.commit()
        flash("Film Category Deleted Successfully")
        return redirect(url_for('FilmStore'))
    else:
        return render_template(
            'deleteFilmCategory.html', fi=fi, fis_cat=fis_cat)

######
# Add New Film Name Details


@app.route('/FilmStore/addCompany/addFilmDetails/<string:finame>/add',
           methods=['GET', 'POST'])
def addFilmDetails(finame):
    fis = session.query(FilmCategoryName).filter_by(name=finame).one()
    # See if the logged in user is not the owner of film
    creator = getUserInfo(fis.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new Film edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showFilms', filid=fis.id))
    if request.method == 'POST':
        moviename = request.form['moviename']
        year = request.form['year']
        rating = request.form['rating']
        action = request.form['action']
        budget = request.form['budget']
        filmdetails = FilmName(
            moviename=moviename, year=year,
            rating=rating, action=action,
            budget=budget,
            date=datetime.datetime.now(),
            filmcategorynameid=fis.id,
            user_id=login_session['user_id'])
        session.add(filmdetails)
        session.commit()
        return redirect(url_for('showFilms', filid=fis.id))
    else:
        return render_template('addFilmDetails.html',
                               finame=fis.name, fis_cat=fis_cat)

######
# Edit Film details


@app.route('/FilmStore/<int:filid>/<string:fiename>/edit',
           methods=['GET', 'POST'])
def editFilm(filid, fiename):
    fi = session.query(FilmCategoryName).filter_by(id=filid).one()
    filmdetails = session.query(FilmName).filter_by(moviename=fiename).one()
    # See if the logged in user is not the owner of film
    creator = getUserInfo(fi.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this Film edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showFilms', filid=fil.id))
    # POST methods
    if request.method == 'POST':
        filmdetails.moviename = request.form['moviename']
        filmdetails.year = request.form['year']
        filmdetails.rating = request.form['rating']
        filmdetails.action = request.form['action']
        filmdetails.budget = request.form['budget']
        filmdetails.date = datetime.datetime.now()
        session.add(filmdetails)
        session.commit()
        flash("Film Edited Successfully")
        return redirect(url_for('showFilms', filid=filid))
    else:
        return render_template(
            'editFilm.html', filid=filid,
            filmdetails=filmdetails, fis_cat=fis_cat)

#####
# Delte Film Edit


@app.route('/FilmStore/<int:filid>/<string:fiename>/delete',
           methods=['GET', 'POST'])
def deleteFilm(filid, fiename):
    fi = session.query(FilmCategoryName).filter_by(id=filid).one()
    filmdetails = session.query(FilmName).filter_by(moviename=fiename).one()
    # See if the logged in user is not the owner of film
    creator = getUserInfo(fi.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this film edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showFilms', filid=fil.id))
    if request.method == "POST":
        session.delete(filmdetails)
        session.commit()
        flash("Deleted film Successfully")
        return redirect(url_for('showFilms', filid=filid))
    else:
        return render_template(
            'deleteFilm.html', filid=filid,
            filmdetails=filmdetails, fis_cat=fis_cat)

####
# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={
                           'content-type':
                           'application/x-www-form-urlencoded'})[0]
    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
            'Successfully disconnected user'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#####
# Json


@app.route('/FilmStore/JSON')
def allFilmsJSON():
    filmcategories = session.query(FilmCategoryName).all()
    category_dict = [c.serialize for c in filmcategories]
    for c in range(len(category_dict)):
        films = [i.serialize for i in session.query(
         FilmName).filter_by(filmcategorynameid=category_dict[c]["id"]).all()]
        if films:
            category_dict[c]["film"] = films
    return jsonify(FilmCategoryName=category_dict)

####


@app.route('/filmStore/filmCategories/JSON')
def categoriesJSON():
    films = session.query(FilmCategoryName).all()
    return jsonify(filmCategories=[c.serialize for c in films])

####


@app.route('/filmStore/films/JSON')
def itemsJSON():
    items = session.query(FilmName).all()
    return jsonify(films=[i.serialize for i in items])

#####


@app.route('/filmStore/<path:film_name>/films/JSON')
def categoryItemsJSON(film_name):
    film = session.query(FilmCategoryName).filter_by(name=film_name).one()
    films = session.query(FilmName).filter_by(filmcategoryname=film).all()
    return jsonify(filmEdtion=[i.serialize for i in films])

#####


@app.route('/filmStore/<path:film_name>/<path:edition_name>/JSON')
def ItemJSON(film_name, edition_name):
    film = session.query(FilmCategoryName).filter_by(name=film_name).one()
    filmEdition = session.query(FilmName).filter_by(
           moviename=edition_name, filmcategoryname=film).one()
    return jsonify(filmEdition=[filmEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=4444)
