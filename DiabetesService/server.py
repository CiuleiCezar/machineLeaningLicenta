import numpy as np
from flask import Flask, request, jsonify
import pickle

from flask_cors import cross_origin

app = Flask(__name__)

# Load the model
model = pickle.load(open('modelKnn.pkl', 'rb'))


@app.route('/api', methods=['POST'])
@cross_origin()
def predict():
    # Get the data from the POST request.
    print(model.predict([[1, 1, 1, 1, 1, 1, 1, 1]]))

    data = request.json
    aux = data.items()
    print(aux)


    prediction = model.predict([[data["Pregnancies"], data["Glucose"], data["BloodPressure"], data["SkinThickness"],
                                 data["Insulin"], data["BMI"], data["DiabetesPedigreeFunction"], data["Age"]]])
    # Take the first value of prediction

    output = prediction[0]
    print(output)
    x = int(output)
    print(x)
    return jsonify(x)


if __name__ == '__main__':
    app.run(5000, debug=True)
