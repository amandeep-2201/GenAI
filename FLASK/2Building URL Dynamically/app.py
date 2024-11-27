# Building URL Dynamically
# Variable Rules and URL Building

from flask import Flask,redirect,url_for

app=Flask(__name__)

@app.route("/")
def welcome():
    return 'Welcome to my youtube channel'

@app.route("/success/<int:score>")
def success(score):
    return "<html><body><h1>The person has passed.</html></body></h1>"

@app.route("/fail/<int:score>")
def fail(score):
    return 'The person has failed and the marks is '+ str(score)

### Result Checker
@app.route('/result/<int:marks>')
def result(marks):
    if marks<50:
        result = "fail"
    else :
        result = "success"
    return redirect(url_for(result,score=marks))


if __name__ == '__main__':
    app.run(debug=True)
