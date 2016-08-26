from flask import Flask,url_for,request,redirect,render_template

app = Flask(__name__)

@app.route('/hello/')
def hello_world():
    return  "Hello World!"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/Users/bjhl/Documents/uploaded_file.txt')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'post'
    else:
        return 'get'

@app.route('/user')
@app.route('/user/<string:username>')
def show_user(username=None):
    return "<h1>%s</h1>" % username

with app.test_request_context():
    print url_for('show_user',username='zhangsan')
if __name__ == '__main__':
    app.run(debug=True)