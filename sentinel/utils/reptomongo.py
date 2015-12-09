""" writes the report to mongodb """

from xmltojson import xmltojson
import mongoengine as db
from datetime import datetime


def str_to_time(date_str):
    """ converts the date string to datetime object """
    date_fmt = "%a, %d %b %Y %H:%M:%S"
    return datetime.strptime(date_str, date_fmt)
    

db.connect('sentinel')

class Report(db.Document):
    """ a report document """
    OWASPZAPReport = db.DynamicField()

    def insert(self, json, collection='newreport'):
        """ inserts the report to the database """
        self.OWASPZAPReport= json['OWASPZAPReport']
        self.switch_collection(collection)
        self.save()




xmlreport = "full-report.xml"
json_report = xmltojson(xmlreport)
report = Report()
report_collection = 'ipc'
#report.insert(json_report, report_collection)    
report.insert(json_report)    
