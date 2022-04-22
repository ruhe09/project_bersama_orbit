from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def iris_prediction():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        print(dict(request.form))
        features = dict(request.form).values()
        features = np.array([float(x) for x in features])
        model, std_scaler = joblib.load("model-development/weight-prediction.pkl")
        features = std_scaler.transform([features])
        print(features)
        result = model.predict(features)
        trans = {
            '1' : 'Male',
            '-1' : 'Female'
        }
        result = format(result[0], '.2f')
        return render_template('index.html', result=[trans[dict(request.form)['gender']], dict(request.form)['height'], result])
    else:
        return "Unsupported Request Method"


if __name__ == '__main__':
    app.run(port=5000, debug=True)