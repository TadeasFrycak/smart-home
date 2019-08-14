if __name__ == "__main__":
    pass

from flask import Flask, jsonify, request, render_template

app = Flask(__name__, static_url_path='/static')

@app.route("/hello", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        print("Method: POST")
        test = request.get_json()
        print(test)
        return "Success", 200

    else:
        print("Method: GET")
        return "Hello from Python-Flask"

@app.route("/run")
def test_page():
    return render_template("index.html")

@app.route("/test")
def test():
    return "<a href='/hello'>Odkaz z Pythonu</a>"

Flask.run(self=None)
