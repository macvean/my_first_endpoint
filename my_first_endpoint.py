from flask import Flask

app = Flask(__name__)

@app.route("/hello")
def hello():
	return "Hello Endpoints"

@app.route("/reverse/<input_string>", methods=['GET'])
def reverse(input_string):
	reversed_string = input_string[::-1]
	return reversed_string

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)

