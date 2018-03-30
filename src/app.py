import calendar
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request

from src.common.Commit import Commit

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
    elements = soup.find_all("rect")

    commits = []

    for element in elements:
        commits.append(Commit(element['data-count'], datetime.strptime(element['data-date'], '%Y-%m-%d')))

    unique_dates = []

    for commit in commits:
        date = f"{commit.date.month}/1/{commit.date.year}";
        if date not in unique_dates:
            unique_dates.append(date)

    commit_amounts = {}

    for commit in commits:
        month_name_and_year = f"{calendar.month_name[commit.date.month]}/{commit.date.year}"
        if month_name_and_year not in commit_amounts:
            commit_amounts[month_name_and_year] = []

        commit_amounts.get(month_name_and_year).append(commit.amount)

    status = "OK"
    if len(unique_dates) == 0 or len(commit_amounts) == 0:
        status = "NOT FOUND"

    return jsonify(commit_amounts=commit_amounts, unique_dates=unique_dates, status=status)


if __name__ == '__main__':
    app.run()
