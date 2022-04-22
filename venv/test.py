from flask import Flask
import requests
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
	return "<p>Berhasil Terhubung ke API</p>"
@app.route('/province')
def province():
  url = 'https://api.rajaongkir.com/starter/province'
  headers = {'key': "6dc38f19f72ed7426e25ef5f42ace6a3"}
  response = requests.get(url,headers=headers)
  return response.headers