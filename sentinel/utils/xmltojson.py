""" converting the xml report to json """
import sys
from pprint import pprint
import xmltodict
from json import loads, dumps



def to_dict(ordered_dict):
    """ converts OrderedDict to dict """
    return loads(dumps(ordered_dict))


def xmltojson(filename):
    """ convert xml to json """
    with open(filename) as f:
        xml_content = f.read()
    ordered_dict = xmltodict.parse(xml_content)
    return to_dict(ordered_dict)


if __name__ == '__main__':
    filename = sys.argv[1]
    json = xmltojson(filename)
    pprint(json)
