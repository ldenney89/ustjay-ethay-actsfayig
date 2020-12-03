import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText().strip()


def get_response(fact):
    response = requests.post('https://hidden-journey-62459.herokuapp.com/piglatinize/',
        allow_redirects=False, data={'input_text': fact})
    return response


@app.route('/')
def home():
    fact = get_fact()
    response = get_response(fact)
    url = response.headers['Location']
    body = '<body><a href="{}">Piglatinize this fact please: "{}"</a></body>'\
    .format(url, fact)
    # return url
    return Response(response=body, mimetype='text/html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
