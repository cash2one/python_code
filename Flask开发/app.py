#ecoding:utf-8
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/user/')
@app.route('/user/<name>')
def user(name=None):
    return render_template('index.html',user=name)

if __name__ == '__main__':
    app.run(debug=True)