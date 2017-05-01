#!/usr/bin/env python
import os
from datetime import date
from forms import LoginForm, RegisterForm, WishForm
from app import app, forms, db, login_manager # models
from models import UserProfile, WishedItem
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify, send_from_directory, session, make_response
from sqlalchemy.sql import exists
from jwt import encode, decode
from werkzeug.wsgi import SharedDataMiddleware
from json import dumps
@app.route('/')
def home():
	return render_template('indexT.html')





@app.route('/api/test', methods = ['GET', 'POST'])
def testAPI(username, homePage):
	return username
	
@app.route('/register')
def registerUserForm():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegisterForm()
	return render_template('signup.html', form = form)

@app.route('/login')
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/create-wish')
@login_required
def createWish():
	form = WishForm()
	return render_template('create-wish.html', form = form)
	
@app.route('/wish', methods = ['GET'])
def userWishes(myWish):
	return render_template('wish.html', myWish = myWish)
	

@login_manager.user_loader
def load_user(id):
	return UserProfile.query.get(int(id))

@app.route('/api/user/register', methods = ['POST'])
def registerUser():
	form = RegisterForm()
	user = None
	if request.method == 'POST':
		if form.validate_on_submit():
			file = request.files['image']
			if not db.session.query(exists().where(UserProfile.username == form.lastname.data)).scalar():
				if form.password.data == form.confirmpass.data:
					user = UserProfile(first_name = form.firstname.data, last_name = form.lastname.data, username = form.username.data, password = form.password.data, profile_photo = 'default.png')
					if file and validate_file(file.filename):
						filename = secure_filename(file.filename)
						filename = 'user_profile_{0}.{1}'.format(user.username, filename.split('.')[-1])
						filefolder = app.config['UPLOAD_FOLDER']
						file.save(os.path.join(filefolder, filename))
						user.profile_photo = filename
					db.session.add(user)
					db.session.commit()
					flash('Registration Successful. You may login')
					return redirect(url_for('login'))
				else:
					flash("Passwords does not match")
					return redirect(url_for('registerUserForm'))
			flash("Username is already in use. Please enter a new one")
			return redirect(url_for('registerUserForm'))
		else:
			flash("All fields required")
			return redirect(url_for('registerUserForm'))
	else:
		return redirect(url_for('registerUserForm'))

@app.route('/api/user/login', methods = ['POST'])
def userlogin():
	print request.get_json()
	data = request.get_json()
	# return dumps({"message" : data['password']})
	users = UserProfile.query.all()
	for user in users:
		if user.username == data['email'] and check_password_hash(user.password, data['password']):
			obj = {'userid' : user.id, 'email' : user.username, 'firstname' : user.first_name, 'lastname' : user.last_name, 'image' : user.profile_photo}
			auth = encode(obj, str(user.id), algorithm = 'HS256')
			user.secretKey = auth
			login_user(user)
			next = request.args.get('next')
			print next
			return dumps({'token': auth, 'user' : obj, 'message' : "SUCCESS"})
		elif user.username == data['email'] and not check_password_hash(user.password, data['password']):
			return dumps({'message' : 'PASSWORD'})
	return dumps({'message' : 'USER'})
	
	# form = LoginForm()
	# if request.method == 'POST':
	# 	if form.validate_on_submit():
	# 		users = UserProfile.query.all()
	# 		for user in users:
	# 			if user.username == form.username.data and check_password_hash(user.password, form.password.data):
	# 				login_user(user)
	# 				next = request.args.get('next')
	# 				return redirect(url_for('home'))
	# 		flash('Invalid username or Password')
	# 		return redirect(url_for('login')) 
 #       else:
	# 		flash('Username and password required')
	# 		return redirect(url_for('login')) 
	# return redirect(url_for('login')) 


@app.route('/api/users/<userid>/wishlist', methods = ['POST', 'GET'])
@login_required
def userWishList(userid):
	form = WishForm()
	if request.method == 'GET':
		wishes = WishedItem.query.all()
		myWish = []
		for wish in wishes:
			if int(wish.userid) == int(userid):
				myWish.append(wish)
		return render_template('wish.html', myWish = myWish)
	elif request.method == 'POST':
		if form.validate_on_submit():
			wish = WishedItem(userid = current_user.id, title = form.wishtitle.data, description = form.description.data, weburl = form.weburl.data, thumbnail = None)
			db.session.add(wish)
			db.session.commit()
			flash('Wish wish added successfully')
		else:
			flash('All fields required')
	return redirect(url_for('createWish'))
	
@app.route('/api/thumbnails')
@login_required
def getThumbnails(url = None):
	if url == None:
		return 'None'
	return 'True'

@app.route('/api/users/<userid>/wishlist/<itemid>', methods=['DELETE', 'POST', 'GET'])
@login_required
def deleteWish(userid, itemid):
	wishes = WishedItem.query.all()
	for wish in wishes:
		if int(wish.userid) == int(userid) and int(wish.id) == int(itemid):
			db.session.delete(wish)
			db.session.commit()
			flash('Item deleted')
	return redirect(url_for('userWishList', userid = current_user.id))

@app.route('/<userid>/mywishlist/')
@login_required
def showWishList(userid):
	return "This will display all the user wishes"

def validate_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """ 
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response	
	

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
    
    
    
# ****************************************************