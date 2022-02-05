import urllib.parse
import requests
import configparser
import argparse

parser = argparse.ArgumentParser(description='Toggle pause/resume for a Jenkins pipeline')
parser.add_argument("-n", "--number", type=int, help="The build number for the job to pause/resume.", required=True)
args = parser.parse_args()


config = configparser.ConfigParser()
config.read('config.ini')

JENKINS_USER = config.get('JENKINS_CREDENTIALS', 'username')
JENKINS_PASS = config.get('JENKINS_CREDENTIALS', 'password')
JENKINS_JOB = config.get('JENKINS_CREDENTIALS', 'job')
JENKINS_URL = config.get('JENKINS_CREDENTIALS', 'url')
JENKINS_PORT = int(config.get('JENKINS_CREDENTIALS', 'port'))


def toggle_jenkins_job(buildNo):
    print("Toggling job build")
    url = 'http://%s:%i/job/%s/%i/pause/toggle' % (JENKINS_URL, JENKINS_PORT, JENKINS_JOB, buildNo)
    parsed_url = urllib.parse.urlparse(url)
    crumb_issuer_url = urllib.parse.urlunparse((parsed_url.scheme,
                                                parsed_url.netloc,
                                                'crumbIssuer/api/json',
                                                '', '', ''))
    session = requests.session()

    # GET the Jenkins crumb
    auth = requests.auth.HTTPBasicAuth(JENKINS_USER, JENKINS_PASS)
    r = session.get(crumb_issuer_url, auth=auth)
    json = r.json()
    crumb = {json['crumbRequestField']: json['crumb']}

    # POST to the specified URL
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    headers.update(crumb)
    r = session.post(url, headers=headers, auth=auth)


toggle_jenkins_job(args.number)
