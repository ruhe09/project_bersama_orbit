from flask import Flask, request, jsonify
from flask import render_template
import numpy as np
import joblib
import requests
import os

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
	return render_template('dashboard.html',landing=1,title='YourService!')
@app.route('/badan',methods=['GET','POST'])
def badan():
    if request.method == 'GET':
        return render_template('dashboard.html',landing=2,title='Deteksi Berat Badan')
    elif request.method == 'POST':
        print(dict(request.form))
        features = dict(request.form).values()
        features = np.array([float(x) for x in features])
        model, std_scaler = joblib.load("model-development/berat_badan.pkl")
        features = std_scaler.transform([features])
        print(features)
        result = model.predict(features)
        trans = {
            '1' : 'Male',
            '-1' : 'Female'
        }
        result = format(result[0], '.2f')
        return render_template('dashboard.html',result=[trans[dict(request.form)['gender']], dict(request.form)['height'], result],landing=2,title='Deteksi Berat Badan')
    
@app.route("/province",methods=['GET','POST'])
def province():    
    if request.method == 'GET':
        return render_template('dashboard.html',form=1,title='Raja Ongkir Province')
    elif request.method == 'POST':
        pathh = request.form['provid']
        url = 'https://api.rajaongkir.com/starter/province'
        headers = {'key': "6dc38f19f72ed7426e25ef5f42ace6a3"}
        parameter = dict(id=pathh)
        response = requests.request('GET',url,headers=headers,params=parameter)
        quer = response.json()
        quer_ex=quer['rajaongkir']['results']['province']
        dispp = render_template('dashboard.html',lokasi=quer_ex,form=1,title='Raja Ongkir Province')
        return f"""
        {dispp}

        """
if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    app.run(port=51366)