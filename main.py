from flask import Flask
import pill

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Pill Box User'

@app.route('/start')
def start():
  pill.runpill()
  return 'Running...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)