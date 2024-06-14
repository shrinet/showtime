from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DecimalField, DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me',
                             validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Submit')

class VenueForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    place = StringField("Place", validators=[DataRequired()])
    capacity = IntegerField("Capacity", validators=[DataRequired()])
    submit = SubmitField('Submit')


class ShowForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    #tags = db.Column(db.String(64))
    price = DecimalField("Capacity", validators=[DataRequired()])
    date_from = DateField("Start Date",validators=[DataRequired()])
    date_to   = DateField("End Date",validators=[DataRequired()])
    showTime = StringField('time', validators=[DataRequired()])
    #timing = db.Column(db.String(255))
    #timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))




class BookingForm(FlaskForm):
    date = StringField("date", validators=[DataRequired()])
    showTime = StringField("showTime", validators=[DataRequired()])
    sheats = StringField("sheats", validators=[DataRequired()])
    price = IntegerField("price", validators=[DataRequired()])
    show_id = IntegerField('show', validators=[DataRequired()])

class ImageUploadForm(FlaskForm):
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    caption   =  StringField("Caption", validators=[DataRequired()])
     
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    body = TextAreaField('Say something', validators=[DataRequired()])
    ratings = StringField('Rating', validators=[DataRequired()])
    submit = SubmitField('Submit')    