import calendar
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request

from common.Commit import Commit

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index_template():
    return render_template('index.html')


@app.route('/graph', methods=['POST'])
def graph_template():
    return render_template('graph.html', username=request.form['username'])


@app.route('/graph/<string:username>', methods=['POST'])
def ajax_request(username):
    request = requests.get("https://github.com/" + username);
    content = request.content

    soup = BeautifulSoup(content, "html.parser")
    elements = soup.find_all("rect") # Gets all the cubes in the users commit

    commits = [Commit(element['data-count'], datetime.strptime(element['data-date'], '%Y-%m-%d')) for element in elements]
	
	# Turns it into a set then list so there aren't any duplicated values
    unique_dates = list(set([f"{commit.date.month}/1/{commit.date.year}" for commit in commits]));
	
    commit_amounts = {}
	
	# Loops through the person's commit and creates a keyset with the "month_name_and_year" and the value of the commit amount.
    for commit in commits:
		# "calender.month_name" get's the month name from the month's number
        month_name_and_year = f"{calendar.month_name[commit.date.month]}/{commit.date.year}"
		
		# If the current date is not in the "commit_amount", create it
        if month_name_and_year not in commit_amounts:
            commit_amounts[month_name_and_year] = []

		# Gets the current commit_amount and adds the commit's amount to it
        commit_amounts.get(month_name_and_year).append(commit.amount)

    status = "OK"
    if len(unique_dates) == 0 or len(commit_amounts) == 0:
        status = "NOT FOUND"

    return jsonify(commit_amounts=commit_amounts, unique_dates=unique_dates, status=status)


if __name__ == '__main__':
    app.run()
