from flask import Flask
app = Flask(__name__)

#MEEST BASIS FUNCTIONALITEIT
@app.route("/")
def indec():
    #render index
    return "<h1>Welkom enzo</h1>"


if __name__ == "__main__":
    app.run()