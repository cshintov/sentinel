""" home controllers """

import urllib
from flask import Blueprint, render_template, request,\
                  redirect, url_for, session

from flask.ext.login import login_user , logout_user , current_user , login_required

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
@login_required
def welcome(username):
    """ welcome """
    user = User.objects().get(username=username)
    print session['username']
    if username != session['username']:
        return "You are a Liar!"
    return render_template("home/welcome.html", user=user)


@home.route('/scanlist/<path:site>', methods=['GET', 'POST'])
@login_required
def scanlist(site):
    scans = Report.objects(__raw__={'OWASPZAPReport.site.@name':site})

    dates = []
    for scan in scans:
        date = scan['OWASPZAPReport']['@generated']
        dates.append((date, date))

    form = ScanlistForm()
    form.date.choices = dates
    return render_template("home/scanlist.html", site=site, form=form)


@home.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ScanlistForm(request.form)
    if None in [form.site.data, form.date.data]:
        message = "You did not submit either the site or the date "
        return render_template("home/dashboard.html", message=message)

    report = Report.objects(__raw__={'OWASPZAPReport.site.@name':form.site.data,
                                      'OWASPZAPReport.@generated':form.date.data})
    try:
        report = report[0].OWASPZAPReport
    except IndexError:
        message = "no scans performed yet on this site"
        return render_template("home/dashboard.html", message=message)

    risk_hist = risk_histo(report)
    alerts = frequency_of_alerts(report)
    top10_uris = top_of_hist(uri_histo(report), 10)
    context = {'risk_hist': risk_hist, 'alerts': alerts, 'top10_uris':top10_uris}
    return render_template("home/dashboard.html", **context)
