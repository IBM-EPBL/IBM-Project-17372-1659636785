from flask import Flask, render_template, redirect, url_for, request,jsonify
import requests

API_KEY = "_jEZ9faTKtRDlZDFHcrrAbuQFdvxbBeiu8W1D8-4z7ng"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Main Page.html")


@app.route("/Page 1",methods = ['POST','GET'])
def input():
    return render_template("Page 1.html")

@app.route("/", methods = ['POST','GET'])
def prediction():
    if request.method == 'POST':
        arr = []
        for i in ["GRE Score","TOEFL Score","University Rating","SOP","LOR","CGPA","Research"]:
            val = request.form[i]
            if val == '':
                return redirect(url_for("Page 1.html"))
            arr.append(float(val))
        #print(arr)
        # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
        
        payload_scoring = {
            "input_data": [{"fields":[  'GRE Score',
                                        'TOEFL Score',
                                        'University Rating',
                                        'SOP',
                                        'LOR ',
                                        'CGPA',
                                        'Research'], 
                            "values": [arr]
                            }]
                        }

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/ed4ff532-801c-457b-85b9-ffa103d3a064/predictions?version=2022-11-18', json=payload_scoring,headers=header).json()
        print(response_scoring)
        result = response_scoring['predictions'][0]['values']
        print(result)
        
        if result[0][0] > 0.5:
            return redirect(url_for('chance', percent=result[0][0]*100))
        else:
            return redirect(url_for('no_chance', percent=result[0][0]*100))
    else:
        return redirect(url_for("Page 1"))
    return ""





@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])

@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("noChance.html", content=[percent])

    

@app.route('/<path:path>')
def catch_all(path):
    return render_template("Page 1.html")

if __name__ == "__main__":
    app.run()