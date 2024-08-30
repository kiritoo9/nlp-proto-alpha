from flask import request, Flask, jsonify
from algorithms.sbert import init

app = Flask(__name__)

@app.route("/")
def welcome():
    return jsonify({
        "app_name": "NLP-Prototype-1.0.x-Alpha",
        "author": "Kirito"
    })

@app.route("/", methods=["POST"])
def search_engine():
    body = request.get_json()
    user_input = body.get("user_input")

    # call NLP library
    response = init(user_input, False) # second parameter is flagging to get response

    # response
    return jsonify({
        "user_input": user_input,
        "response": response
    })

# run app
if __name__ == "__main__":
    app.run(debug=True, port=5001)