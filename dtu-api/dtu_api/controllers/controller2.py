#!/usr/bin/python

from myapplication import app

@app.route('/page3.html')
def page3():
	return 'Page3.'

@app.route('/page4.html')
def page4():
	return "Page4"