from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)


Jobs = [
  {
    'id': 1,
    'title': 'Data Analyst',
    'location': 'Bengaluru, India',
    'salary': '$100,000'
  },
  {
    'id': 2,
    'title': 'Data Scientist',
    'location':'Delhi, India',
    'salary': '$150,000'
  },
    {
      'id': 3,
      'title': 'Frontend Engineer',
      'location': 'Remote',
      'salary': '$120,000'
    },
  {
     'id': 4,
      'title': 'Backend Engineer',
      'location': 'San Francisco, USA',
      'salary': '$150,000'
  }
]

@app.route('/')
@app.route('/home')
def home():
  return render_template('home.html', jobs=Jobs)

@app.route('/api/jobs')
def list_jobs():
  return jsonify(Jobs)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
