from flask import Flask
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/')
def index():
    return 'Index page'

@app.route('/user/<username>')
def show_user_profile(username):
    # show user profile
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Poes %d' % post_id

if __name__ == '__main__':
    app.debug = True
    app.run()