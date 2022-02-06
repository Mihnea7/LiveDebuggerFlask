import configparser
import json
import requests

config = configparser.ConfigParser()
config.read('config.ini')

JENKINS_JOB = config.get('JENKINS_CREDENTIALS', 'job')
JENKINS_PORT = config.get('JENKINS_CREDENTIALS', 'port')
JENKINS_URL = config.get('JENKINS_CREDENTIALS', 'url')


def get_current_build_number():
    data = json.loads(requests.get
                      ("http://%s:%s/job/%s/api/json" % (JENKINS_URL, JENKINS_PORT, JENKINS_JOB))
                      .text)
    return data["builds"][0]["number"]


print(get_current_build_number())
