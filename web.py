#!/bin/python3
from flask import *
import picture
import exam
import os
app = Flask(__name__)

@app.route('/picture', methods=['GET'])
def picture_page():
    name = request.args.get('name')
    picture.draw_pic(name)
    if os.path.exists('temp/'+name+'.png'):
        with open('temp/'+name+'.png', 'rb') as f:
            return f.read()
    return ''

@app.route('/picture_ranking', methods=['GET', 'POST'])
def picture_ranking_page():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args['name']

    picture.draw_pic_ranking(name)
    if os.path.exists('temp/'+name+'_ranking.png'):
        with open('temp/'+name+'_ranking.png', 'rb') as f:
            return f.read()
    return ''

@app.route('/student', methods=['GET', 'POST'])
def student_page():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args['name']
    return exam.to_html(exam.tests, exam.tests_names, name)

import group
@app.route('/group', methods=['GET', 'POST'])
def group_page():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args['name']
    return group.gen_group(name)

@app.route('/')
def index_page():
    with open('login.html', 'rb') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='8180')
