""" utility functions for home """


def get_alerts(report):
    """ get list of alerts from report """
    return report['site']['alerts']['alertitem']


def risk_histogram(alerts):
    """ create a histogram of low, medium, and high risk alerts 
        :alerts a list of alerts (dicts)
        :risk_hist a dict histogram of risklevels
    """
    risk_hist = {'low':0, 'medium':0, 'high':0}
    for alert in alerts:
        if alert['riskcode'] == '1':
            risk_hist['low'] += 1
        elif alert['riskcode'] == '2':
            risk_hist['medium'] += 1
        elif alert['riskcode'] == '3':
            risk_hist['high'] += 1
    return risk_hist


def convert_histogram(hist):
    """ convert a histogram to percentage 
    :hist a dict histogram with integer counts
    :hist_pcent a histogram with percentage values
    """
    total = sum(hist.values())
    hist_pcent = {key: hist[key] / float(total) for key in hist.keys()}
    return hist_pcent


