from flask import Flask, render_template

app = Flask(_name_)

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/test')
def test():
    return "Render is working"

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)
