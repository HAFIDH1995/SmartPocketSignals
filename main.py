from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signals')
def signals():
    return render_template('signals.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)



