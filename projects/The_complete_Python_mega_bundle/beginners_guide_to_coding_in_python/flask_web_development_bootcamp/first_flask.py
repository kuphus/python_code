from flask import Flask, render_template, jsonify
from flask_ngrok import run_with_ngrok

app = Flask(__name__, template_folder='./templates')

run_with_ngrok(app)

@app.route('/')
def index():
    return "<h1>Welcome to the index!</h1>  <p>Under construction</p>"


@app.route('/about')
def about():
    return "About us... We are awesome!"


@app.route('/profile/ik')
def profile():
    return "<h2>Welcome to my profile!!!</h2>"


@app.route('/products/<name>')
def product_page(name):
    return "<h3>Product " + name + "</h3>"


@app.route('/products/<name>/<price>')
def product_information(name, price):
    return "<h4>The " + name + " will cost you " + price + " euro's</h4>"


@app.route('/first-template')
def first_template():
    return render_template('first_template.html')


@app.route('/profile/<username>')
def show_profile(username):
    return render_template('profile.html', name=username)


Courses = [
    {'id': 1, 
     'title': 'Hello coding', 
     'image_url': 'https://img-c.udemycdn.com/course/240x135/2776760_f176_10.jpg'},
    {'id': 2,
     'title': 'Machine Learning for Everybody',
     'image_url': 'https://img-c.udemycdn.com/course/240x135/950390_270f_3.jpg'},
    {'id': 3,
     'title': 'Boring Stuff',
     'image_url': 'https://img-c.udemycdn.com/course/240x135/543600_64d1_4.jpg"'}
]


@app.route('/api/courses')
def api_courses():
    return jsonify(Courses)


@app.route('/courses')
def courses():
    return render_template('all_courses.html', courses = Courses)

if __name__ == '__main__':
    app.run()