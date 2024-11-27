### Integrate HTML with Flask
### HTTP verb GET And POST
from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)

@app.route("/")
def welcome():
    return render_template('index.html')

@app.route("/finalresults/<int:score>")
def finalresults(score):
    res = ""
    if score>=50:
        res="PASS"
    else:
        res="FAIL"
        
    return render_template('result.html', result=res)

# Result checker html page
@app.route('/submit', methods=['POST','GET'])
def submit():
    total_score=0
    if request.method=='POST':
        science = float(request.form['science'])
        maths = float(request.form['maths'])   #we are writing ids in the bracket
        c = float(request.form['c'])
        data_science = float(request.form['datascience'])
        total_score = (science+maths+c+data_science)/4
        res = ""
        return redirect(url_for('finalresults',score=total_score))
    
    
if __name__ == '__main__':
    app.run(debug=True)
