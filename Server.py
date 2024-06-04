from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

model = tf.keras.models.load_model('./model/model.keras')


@app.route("/")
def hello():
    return "<p>Hello There</p>"


@app.route("/run", methods=['POST'])
def run():
    try:
        data = request.get_json()

        print(data)
        #ensure correct data is passed in
        if not data or 'gems' not in data:
            return jsonify({
                "error": "Invalid input data, 'gems' key is missing."
            }), 400


        #grab our data
        model_input = data['gems']
        

        if not isinstance(model_input, list):
            return jsonify({
                "error": "Invalid input data format for 'gems', expected list but got " + type(model_input)
            }), 400
        
        
        try:
            prediction = model.predict(np.array([model_input]))
            print(prediction) # Output:
            result = prediction.tolist()
            return jsonify({
                "data": result
            })
        except Exception as e:
            return jsonify({
                "error": "Error during model predction process.",
                "details": str(e)
            }), 500
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occoured.",
            "details": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)