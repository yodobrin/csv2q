from flask import Flask, render_template           
app = Flask(__name__)             # create an app instance

@app.route("/")                   # at the end point /
# def hello():                      # call method hello
#     return "I like sabich!"         # which returns "hello world"
def index():
    return render_template("index.html")

if __name__ == "__main__":        # on running python app.py
    app.run()                     # run the flask app