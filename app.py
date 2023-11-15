from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return "<p>Hello, world!<p>"

@app.route('/login')
def login():
    return redirect('https://flask-example.auth.us-east-1.amazoncognito.com/login?client_id=7pi13oefg6mpgver2aso0s0lqv&response_type=code&scope=email+openid+phone&redirect_uri=http%3A%2F%2Flocalhost:8080%2Flogged_in')

@app.route('/logged_in', methods=['GET'])
def logged_in():
    code = request.args.get('code', None)
    return f"<p>Logged in {code}!<p>"

@app.route('/logout')
def logout():
    pass

if __name__ == "__main__":
    app.run(debug = True,  host='0.0.0.0', port=8080)