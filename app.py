from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    render_template('index.html')

@app.route('/scrap')
def scrap():
    pass

if __name__ == '__main__':
    app.run(debug=True)