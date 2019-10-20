import flask
from flask import request, jsonify
from bs4 import BeautifulSoup
import requests

app = flask.Flask(__name__)
app.config['DEBUG'] = True
BASE_URL = 'http://jobs.prudential.com'

@app.route('/')
def home():
    return 'nothing to see here...'

@app.route('/api/<term>/', defaults = {'location': ''})
@app.route('/api/<term>/<location>')
def search(term, location):
    req = requests.get(f'http://jobs.prudential.com/job-listing.php?keyword={ term }&jobType=any&location={ location }&jobLabel=&jobLocation={ location }&IsThisACampusRequisition=Yes')
    soup = BeautifulSoup(req.text, 'html.parser')
    # parse for urls and titles of each job. then go to the url of the job and parse the job description.
    d = {}
    for i in soup.find("div", {"id": "searchResults"}):
#        with open ('output.txt','w') as f:
        d[BASE_URL + i.a['href']] = i.a.h3.string
    # use jsonify to return the data in json format
    # example return below
    return jsonify(d)

app.run()
