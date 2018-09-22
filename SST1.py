import sqlite3
import datetime
#python-jenkins wrapper
import jenkins
import json
import sys
import urllib
import urllib2

jenkinsUrl = "localhost:8080/job"

def getjobstatus(jobname):
    try:
        jenkinsStream = urllib2.urlopen(jenkinsUrl + jobName + "/lastBuild/api/json")
    except urllib2.HTTPError, e:
        print "URL Error: " + str(e.code)
        print "      (job name [" + jobName + "] probably wrong)"
        return

    try:
        buildStatusJson = json.load(jenkinsStream)
    except:
        print "Failed to parse json"
        return

    if buildStatusJson.has_key("result"):
        print "[" + jobName + "] build status: " + buildStatusJson["result"]
        return buildStatusJson["result"]

db = sqlite3.connect(':memory:')
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE jobs(id INTEGER PRIMARY KEY, status TEXT,
                       time TIMESTAMP )
''')
db.commit()

server = jenkins.Jenkins('http://localhost:8080', username='admin', password='53c00a069a0047f0a092cdb1d586728e')
jobs = server.get_jobs()

for job in jobs:
    jobName = job['name']
    jobStatus = getjobstatus(jobName)
    dateNow = datetime.datetime.now()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO jobs(status, time)
                      VALUES(?,?)''', (jobStatus, dateNow))



db.close()

