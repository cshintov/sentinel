from flask.ext.wtf import Form

# Import Form elements
from wtforms import SelectField, StringField

class ScanlistForm(Form):
    date = SelectField('scans')
    site = StringField('site')

