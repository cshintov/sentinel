""" home controllers """

import urllib
from flask import Blueprint, render_template, request,\
                  redirect, url_for

# Import the database object from the main app module
from sentinel import db

# Import module models 
from sentinel.models import User, Report

# Import module forms
from sentinel.home.forms import ScanlistForm

# Import utility functions
from sentinel.utils.extract_info import risk_histo, uri_histo, top_of_hist,\
     frequency_of_alerts 

# Define the blueprint: 'auth', set its url prefix: app.url/auth
home = Blueprint('home', __name__, url_prefix='/home')

# Set the route and accepted methods
@home.route('/welcome/<username>', methods=['GET', 'POST'])
def welcome(username):
    """ welcome """
    user = User.objects().get(username=username)
    return render_template("home/welcome.html", user=user)


@home.route('/scanlist/<path:site>', methods=['GET', 'POST'])
def scanlist(site):
    scans = Report.objects(__raw__={'OWASPZAPReport.site.@name':site})
    dates = [(scan['OWASPZAPReport']['@generated'], scan['OWASPZAPReport']['@generated'])
             for scan in scans]
    form = ScanlistForm()
    form.date.choices = dates
    return render_template("home/scanlist.html", site=site, form=form)


@home.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = ScanlistForm(request.form)
    report = Report.objects(__raw__={'OWASPZAPReport.site.@name':form.site.data,
                                      'OWASPZAPReport.@generated':form.date.data})
    report = report[0].OWASPZAPReport
   
    risk_hist = risk_histo(report)
    alerts = frequency_of_alerts(report)
    top10_uris = top_of_hist(uri_histo(report), 10)
    context = {'risk_hist': risk_hist, 'alerts': alerts, 'top10_uris':top10_uris}
    #return render_template("home/dashboard.html", risk_hist=risk_hist, top10_uris=top10_uris)
    return render_template("home/dashboard.html", context=context)
