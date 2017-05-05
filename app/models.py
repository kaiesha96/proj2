#!/usr/bin/env python
from . import db
from time import time
from datetime import date
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

#from flask import json, jsonify

class UserProfile(db.Model, UserMixin):
	__tablename__ = 'UserProfileInfo'
	id = db.Column(db.Integer, primary_key=True)
	first_name 		= db.Column(db.String(80))
	last_name 		= db.Column(db.String(80))
	username 		= db.Column(db.String(80), unique=True)
	password		= db.Column(db.String(80))
	profile_photo 	= db.Column(db.String(80))

	def __init__(self, first_name, last_name, username, password, profile_photo):
		self.id		 		= UserProfile.get_new_id()
		self.first_name 	= first_name
		self.last_name 		= last_name
		self.username 		= username
		self.password 		= generate_password_hash(password)
		self.profile_photo  = profile_photo

	
	@staticmethod
	def get_new_id():
		new_id = long(time())
		return new_id #michelle advertising 
		
	@staticmethod
	def timeinfo():
		"""Forats the date and time"""
		d = date.today();
		return "{0:%A}, {0:%B} {0:%d}, {0:%y}".format(d)
	
	def passwordMatch(self, password):
		return check_password_hash(self.password, password)
		
	def __repr__(self):
		return '<User %r>' % (self.username)

	def get_image_url(self):
		return '/uploads/{0}'.format(self.image)
	
	def is_authenticated(self):
		return True
	
	def is_active(self):
		return True
	
	def is_anonymous(self):
		return False
	
	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

class WishedItem(db.Model):
    __tablename__ = 'Wishes'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer) #the user that it is assigned to
    #wishListID = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    weburl = db.Column(db.String(500))
    thumbnail = db.Column(db.String(200))
    
    def __init__(self, userid, title, description, weburl, thumbnail):
		self.id	= WishedItem.get_new_id()
		#self.wishListID = wishListID
		self.userid = userid
		self.title = title
		self.description = description
		self.weburl = weburl
		self.thumbnail = thumbnail
	
	
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    @staticmethod
    def get_new_id():
        new_id = long(time())
        return new_id
