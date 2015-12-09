""" extracts info from the xml report """

import sys
from xmltojson import xmltojson
from utils import risk_histogram, get_alerts
from pprint import pprint


def risk_histo(report):
    """ computes the histogram of the risklevel of vulnerabilities """
    return risk_histogram(get_alerts(report))


def frequency_of_alerts(report):
    """
    Returns : list of dict of the format {alert_id: , count: , alert: }
    Parameters : ZAP report in json
    """
    alerts = get_alerts(report)
    error_count = [{'alert_id': str(alert['pluginid']), 'count': int(alert['count']),
                                             'alert': str(alert['alert'])}
                                             for alert in alerts]

    return sorted(error_count, key=lambda x: x['count'], reverse=True)


def top_of_hist(hist, topn=-1):
    """ given a histogram returns the topn number of highest elements """
    sorted_keys = sorted(hist.keys(), key=lambda dkey:hist[dkey], reverse=True)
    if topn != -1:
        sorted_keys = sorted_keys[:topn]
    top_n_items = []
    for key in sorted_keys:
        top_n_items.append({'uri':key, 'count':hist[key]})
    return top_n_items


def uri_histo(report):
    """ computes the histogram of uri instances having a vulnerability"""
    alerts = get_alerts(report)
    uri_histo = {}
    for alert in alerts:
        uri_instances = alert['instances']['instance']
        if isinstance(uri_instances, dict):
            uri = uri_instances['uri']
            uri_histo[str(uri)] = uri_histo.get(uri, 0) + 1
        elif isinstance(uri_instances, list):
            for instance in uri_instances:
                uri = instance['uri']
                uri_histo[str(uri)] = uri_histo.get(uri, 0) + 1

    return uri_histo 


if __name__ == '__main__':
    filename = sys.argv[1]
    json_report  = xmltojson(filename)
    print "RISK LEVELS"
    pprint(risk_histo(json_report))
    print

    alerts = frequency_of_alerts(json_report)
    print "ALERT COUNTS"
    pprint(alerts)
    print

    instances = uri_histo(json_report)
    print "TOP 10 VULNERABLE URIS"
    pprint( top_of_hist(instances, topn=10, sortkey=lambda key:key.values()[0]))
