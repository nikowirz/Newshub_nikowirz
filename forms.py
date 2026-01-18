from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 5, max = 11)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 5, max = 11)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')


class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField(
        'Category',
        choices=[('general', 'General'), ('sports', 'Sports'), ('business', 'Business'), ('health', 'Health'), ('innovation', 'Innovation'), ('culture', 'Culture'), ('arts', 'Arts'), ('travel', 'Travel'), ('earth', 'Earth')])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')
