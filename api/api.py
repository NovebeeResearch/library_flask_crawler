import flask
from flask import Flask,render_template, request, jsonify
import json




#with open('model/web_scraper/data/data.json') as file:
#    data_json = json.load(file)

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]



app = flask.Flask(__name__)
app.config["DEBUG"] = True

#{"Name":val_attri[0],"Author":val_attri[1],"Length":val_attri[2]}


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"



@app.route('/dashboard', methods=['GET'])
def api_all():
    return render_template("dashboard.html")



@app.route('/api/v1/aimodel/resource/squrce', methods=['GET'])
def sq_op():
    return "<h1>result of sq</h1><p>ss</p>"




if __name__=="__main__":
    app.run(debug=True)


