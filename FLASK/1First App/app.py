from flask import Flask

app = Flask(__name__)   #wsgi application


#decorator   # / = homepage
@app.route('/')   #parameter = rule,option   #rule contains url
def welcome():
    return "Welcome to my youtube channel.Please subscribe my channel"

@app.route('/members')   #parameter = rule,option   #rule contains url
def members():
    return "Welcome to my youtube channel members."

if __name__ =='__main__':
    app.run(debug=True)  #paramters = host,port,debug
    #debug automaticaly restarts the server after making changes.