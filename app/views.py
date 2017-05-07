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
from jwt import encode, decode, InvalidTokenError
from werkzeug.wsgi import SharedDataMiddleware
from json import dumps
import requests
from bs4 import BeautifulSoup
import urlparse
from requests.exceptions import MissingSchema
from requests.packages.urllib3.exceptions import InsecureRequestWarning, SNIMissingWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

@app.route('/')
def login():
	
	# return app.send_static_file('index.html')
	# return 'Hello'
	return render_template('index.html');
	
@app.route('/logout')
# @login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

	
@login_manager.user_loader
def load_user(id):
	return UserProfile.query.get(int(id))

@app.route('/api/users/register', methods = ['POST'])
def registerUser():
	data = request.get_json()
	if request.method == 'POST':
		if not db.session.query(exists().where(UserProfile.username == data['email'])).scalar():
			if data['password'] == data['conpassword']:
				user = UserProfile(first_name = data['firstname'], last_name = data['lastname'],  username = data['email'], password = data['password'] , profile_photo = 'user_profile_administrator.png')
				db.session.add(user)
				db.session.commit()
				return dumps({'message' : '200-OK', 'error' : 'null'})
			else:
				return dumps({'message' : '200-OK', 'error' : 'INCORRECT PASSWORDS'})
		return dumps({'message' : '200-OK', 'error' : 'USER EXIST'})
	return dumps({'message':'400-ERROR', 'error' : '0X51427'})

@app.route('/api/users/logout', methods = ['GET'])

def userLogout():
	logout_user()
	print 'user logged out'
	return dumps({'message' : '200-OK', 'key': 'null', 'user': {}})

@app.route('/api/users/data', methods = ['POST'])

def getUserData():
	data = request.get_json()
	try:
		decoded = decode(data['key'], str(app.secret_key), algorithms='HS256')
		username = decoded['email']
		password = decoded['password']
		
		user = UserProfile.query.filter_by(username = username).first()
		
		if user == None:
			return dumps({'message' : 'Session Lost', 'key' : 'null', 'user' : {} })
			
		elif user.passwordMatch(password):
			obj = {'userid' : user.id, 'email' : user.username, 'firstname' : user.first_name, 'lastname' : user.last_name, 'image' : user.profile_photo}
			return dumps({'message' : 'null', 'key' : data['key'], 'user' : obj})
			
		else:
			return dumps({'message' : 'TERMINATED', 'key' : 'null', 'user' : {} })
			
	except InvalidTokenError:
		return dumps({'message' : 'INVALID KEY', 'key' : 'null', 'user' : {} })



@app.route('/api/users/login', methods = ['POST'])
def userlogin():
	data = request.get_json()
	user = UserProfile.query.filter_by(username = data['email']).first()
	if user == None:
		return dumps({'message' : 'Invalid User'})
	elif user.passwordMatch(data['password']):
		login_user(user)
		
		obj = {'userid' : user.id, 'email' : user.username, 'firstname' : user.first_name, 'lastname' : user.last_name, 'image' : user.profile_photo}
		key = encode({'email' : user.username, 'password' : data['password']}, str(app.secret_key), algorithm = 'HS256')
		
		return dumps({'message' : 'null', 'key' : key, 'user' : obj})
	else:
		return dumps({'message' : 'Invalid Password'})

@app.route('/api/users/<userid>/wishlist', methods = ['POST', 'GET'])
# @login_required
def userWishList(userid):
	
	data = request.get_json()
	if request.method == 'POST':
		try:
			decoded = decode(data['key'], str(app.secret_key), algorithms='HS256')
			username = decoded['email']
			password = decoded['password']
			
			user = UserProfile.query.filter_by(username = username).first()
			
			if user == None:
				return dumps({'message' : 'Session Lost'})
				
			elif user.passwordMatch(password):
				
		 		message = data['message']
		 		
		 		if message == 'GET':
		 			return getThumbnails(data['url'])
		 		else:
		 			wish = WishedItem(userid = userid, title = data['title'], description = data['description'], weburl = data['url'], thumbnail = data['thumbnail'])
					db.session.add(wish)
			 		db.session.commit()
			 		return dumps({'message' : '200-OK'})
			 	return dumps({'message' : '404-ERROR'})
			else:
				return dumps({'message' : '404-ERROR'})
				
		except InvalidTokenError:
			return dumps({'message' : 'INVALID KEY'})
	elif request.method == 'GET':
		user = UserProfile.query.filter_by(id = int(userid)).first()
		if user == None:
			return dumps({'message' : 'Session Lost'})
		else:
			wishes = WishedItem.query.all()
			myWish = []
			for wish in wishes:
				if int(wish.userid) == int(userid):
					w = {'id' : wish.id, 'user' : wish.userid, 'title' : wish.title, 'description' : wish.description, 'weburl' : wish.weburl, 'thumbnail' : wish.thumbnail}
					myWish.append(w)
			if len(myWish) == 0:
				return dumps({'message' : 'EMPTY', 'wishes' : myWish})
			return dumps({'message' : 'SUCCESS', 'wishes' : myWish})
	else:
		return dumps({'message' : '404', 'wishes' : []})


@app.route('/api/thumbnails')
# @login_required
def getThumbnails(url = None):
	try:
		if url == None:
			return dumps({'message' : '404-ERROR', 'images' : []})
		result = requests.get(url)
		soup = BeautifulSoup(result.text, "lxml")
		
		images = []
		for img in soup.findAll("img", src=True):
			images += [img["src"]]
		
		if len(images) == 0:
			return dumps({'message' : '404-ERROR', 'images' : []})
		return dumps({'message' : '200-OK', 'images' : images})
	except MissingSchema:
		return dumps({'message' : '400-ERROR', 'error' : 'Invalid URL'})
	
@app.route('/api/users/<userid>/wishlist/<itemid>', methods=['DELETE'])
# @login_required
def deleteWish(userid, itemid):
	wishes = WishedItem.query.filter_by(userid = int(userid)).all()
	for wish in wishes:
		if int(wish.id) == int(itemid):
			db.session.delete(wish)
			db.session.commit()
			return dumps({'message' : '200-OK'})
	return dumps({'message' : '400-ERROR'})

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
	


    
    
    
# ****************************************************
