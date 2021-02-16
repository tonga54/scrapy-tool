from flask import Flask, render_template, request
from flask_cors import cross_origin
from selenium import webdriver
from strategy.scraperContext import ScraperContext
import sys

app = Flask(__name__)

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search/search.html')

@cross_origin()
@app.route('/process', methods=['POST'])
def process():
    # location = {
    #     "latitude": 50.1109,
    #     "longitude": 8.6821,
    #     "accuracy": 100
    # }
    file = request.files.get("file")
    term = request.form.get('term')
    keywords = request.form.get('keywords')
    engine = request.form.get('engine')
    driver = request.form.get('driver')
    ignore = request.form.get('ignore')
    alexa_min = request.form.get('alexa_min')
    alexa_max = request.form.get('alexa_max')

    error = False
    if term is None:
        error = True
    if keywords is None:
        error = True
    if engine is None:
        error = True
    if driver is None:
        error = True
    if ignore is None:
        error = True
    if alexa_min is None:
        error = True
    if alexa_max is None:
        error = True

    if error is False:
        alexa_min = 0
        alexa_max = sys.maxsize
        if request.form.get('alexa_min') != "":
            alexa_min = int(request.form.get('alexa_min'))
        if request.form.get('alexa_max') != "":
            alexa_max = int(request.form.get('alexa_max'))

        if keywords == "":
            keywords = []
        else:
            keywords = keywords.split(',')

        context = ScraperContext()
        context.setDriver()
        context.setEngine()
        data = context.doSearch(searchInput= term, keywords= keywords, min_popularity= alexa_min, max_popularity= alexa_max, file= file)
        return data, 200
    else:
        return {"error": True}, 401

if __name__ == '__main__':
    app.run(port = 9007, debug = False)