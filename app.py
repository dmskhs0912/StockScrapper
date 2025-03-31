from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    
    elif request.method == 'POST':
        search_text = request.form.get('search_text')
        return render_template('search.html', search_text=search_text)

@app.route('/scrap')
def scrap():
    return render_template('scrap.html')

if __name__ == '__main__':
    app.run(debug=True)