from flask import Flask, request
import os
import subprocess
import configparser
import json
import requests

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

JENKINS_USER = config.get('JENKINS_CREDENTIALS', 'username')
JENKINS_PASS = config.get('JENKINS_CREDENTIALS', 'password')
JENKINS_JOB = config.get('JENKINS_CREDENTIALS', 'job')
JENKINS_URL = config.get('JENKINS_CREDENTIALS', 'url')
JENKINS_PORT = config.get('JENKINS_CREDENTIALS', 'port')

JENKINS_DIR = default = "/var/lib/jenkins/workspace/" + JENKINS_JOB


@app.route('/')
def hello():
    stream = os.popen('pwd')
    output = stream.read()
    return output


@app.route('/declarative-linter')
def linter():
    filename = request.args.get("filename", default=JENKINS_DIR + "/Jenkinsfile", type=str)
    command = "java -jar jenkins-cli.jar -s http://%s:%s -auth %s:%s declarative-linter < %s" \
              % (JENKINS_URL, JENKINS_PORT, JENKINS_USER, JENKINS_PASS, filename)
    stream = subprocess.Popen(command, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = stream.communicate()[0].decode("utf-8")
    err = stream.communicate()[1].decode("utf-8")
    return output if output else err


@app.route('/replay-job')
def replay_job():
    build_nr = request.args.get("build_nr", default=get_current_build_number(), type=int)
    filename = request.args.get("filename", default=JENKINS_DIR + "/Jenkinsfile", type=str)
    command = " java -jar jenkins-cli.jar -s http://%s:%s -auth %s:%s replay-pipeline %s -n %i < %s" \
              % (JENKINS_URL, JENKINS_PORT, JENKINS_USER, JENKINS_PASS, JENKINS_JOB, build_nr, filename)
    stream = subprocess.Popen(command, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = stream.communicate()[0].decode("utf-8")
    err = stream.communicate()[1].decode("utf-8")
    return output if output else err


@app.route('/request-shell')
def handle_inject_shell_req():
    command = "./inject-shell.sh %s:%s" % (JENKINS_URL, JENKINS_PORT)
    stream = subprocess.Popen(command, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = stream.communicate()[0].decode("utf-8")
    err = stream.communicate()[1].decode("utf-8")
    return output if output else err


def get_current_build_number():
    data = json.loads(requests.get
                      ("http://%s:%s/job/%s/api/json" % (JENKINS_URL, JENKINS_PORT, JENKINS_JOB))
                      .text)
    return data["builds"][0]["number"]
