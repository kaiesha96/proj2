from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, TextAreaField
from wtforms.validators import InputRequired, Length, Regexp, Required


class LoginForm(FlaskForm):
    username = StringField("Username/Email", validators = [InputRequired()], render_kw = {'placeholder' : 'Username'})
    password = PasswordField("Password", validators = [InputRequired()], render_kw = {'placeholder' : 'Password'})
    
class RegisterForm(FlaskForm):
    firstname = StringField("Firstname", validators = [InputRequired()], render_kw = {'placeholder' : 'First Name'})
    lastname = StringField("Lastname", validators = [InputRequired()], render_kw = {'placeholder' : 'Last Name'})
    username = StringField("Username", validators = [InputRequired()], render_kw = {'placeholder' : 'Username'})
    password = PasswordField("Password", validators = [InputRequired()], render_kw = {'placeholder' : 'Password'})
    confirmpass = PasswordField("Confirm Password", validators = [InputRequired()], render_kw = {'placeholder' : 'Confrim Password'})
    image = FileField('Profile Photo', validators = [])
    
    
class WishForm(FlaskForm):
    wishtitle = StringField("Title", validators = [InputRequired()], render_kw = {'placeholder' : 'Title'})
    description = TextAreaField('Description', 	validators 	= [ InputRequired(), Length(max = 200) ], render_kw = {'placeholder' : 'A short description....', 'rows' : '5'})
    weburl = StringField("Web URL", validators = [InputRequired()], render_kw = {'placeholder' : 'www.wishlist.com/hello-world'})