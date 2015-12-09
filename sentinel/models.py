""" models used by the sentinel application """

from sentinel import db
from utils import xmltojson

class User(db.Document):
    """ user of the application """
    username = db.StringField()
    password = db.StringField()
    isAdmin = db.BooleanField()
    ownedSites = db.ListField()
    dateCreated = db.DateTimeField()

    def __repr__(self):
        return "<User %r>" % (self.username)


class Report(db.Document):
    """ a report document """
    OWASPZAPReport = db.DynamicField()

    def insert(self, xmlreport):
        """ inserts the report to the database """
        json_rep = xmltojson(xmlreport)
        self.OWASPZAPReport= json_rep['OWASPZAPReport']
        self.save()

    def __repr__(self):
        return "<Report %r at %r >" % (self.OWASPZAPReport['site']['@name'], self.OWASPZAPReport['@generated'])
