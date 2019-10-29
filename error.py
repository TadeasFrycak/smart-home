from flask import Flask
import sys

SEPARATOR = "::"
app = Flask(__name__)

print(sys.argv)
@app.route("/")
def index():
    f = open("templates/error.html", "r")
    content = f.readlines()
    f.close()

    return "".join(content).replace(SEPARATOR + "header" + SEPARATOR, sys.argv[1]).replace(SEPARATOR + "error" + SEPARATOR, "Exited with code: {0}".format(sys.argv[2]))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

else:
    print("Error")
