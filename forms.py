from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length

class AddUser(FlaskForm):
    '''Creates new users'''
    
    username = StringField(
        "Username", 
        validators=[
            DataRequired("username is required"),
            Length(max=20)])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired("password is required")])
    email = EmailField(
        "Email",
        validators=[
            DataRequired("email is required"),
            Length(max=50)])
    first_name = StringField(
        "First Name",
        validators=[
            DataRequired("first name is required"),
            Length(max=30)])
    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired("last name is required"),
            Length(max=30)])

class LoginUser(FlaskForm):
    '''Authenticates a user'''
    
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="username is required"),
            Length(max=20)])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="password is required")])

class AddFeedback(FlaskForm):
    '''Form to submit feedback'''
    
    title = StringField(
        "Title",
        validators=[
            DataRequired(message="title is required"),
            Length(max=100)]),
    content = TextAreaField(
        "Content",
        validators=[
            DataRequired(message="content is required")])