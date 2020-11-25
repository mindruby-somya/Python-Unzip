import flask
from flask import request
from flask import jsonify
import zipfile
import requests
from io import BytesIO
import json


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['POST'])
def main():
    myZipFile = request.data
    headers = flask.request.headers
    respData = {}
    zipdata = BytesIO()
    zipdata.write(myZipFile)
    pID = headers.get('parent-id')
    returnURL = headers.get('return-url')
    print(pID)
    respIds = []
    #https://ccdev3-moneyspot.cs57.force.com/services/apexrest/GetSeperateFiles/
    if zipfile.is_zipfile(zipdata):
        with zipfile.ZipFile(zipdata) as zip_ref:
            for info in zip_ref.infolist():
                data = info.filename
                myHTML = zip_ref.read(data)
                headToSend = {}
                headToSend['parent-id'] = pID
                headToSend['name'] = data
                temp = {}
                req = requests.post(returnURL, data=myHTML, headers=headToSend)
                if req.status_code != 200:
                    temp['name'] = data
                    temp['status'] = 'failed'
                else :
                    temp['name'] = data
                    temp['status'] = 'success'
                    temp['id'] = req.text
                respIds.append(temp)
        respData['data'] = respIds
        respData['success'] = True
    else:
        respData['success'] = False

    response = app.response_class(
        response = json.dumps(respData),
        status = 200,
        mimetype = 'application/json'
    )
    return response

if __name__ == "__main__":
    app.run(debug=True)