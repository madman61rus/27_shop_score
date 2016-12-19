from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def score():
    return render_template('score.html')

if __name__ == "__main__":
    app.run()
