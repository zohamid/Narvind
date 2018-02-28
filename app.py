import os

from flask import Flask, render_template, request, redirect, url_for, jsonify
from sklearn.externals import joblib
import ml_face
app = Flask(__name__)

pca = joblib.load("pca.pkl")
clf = joblib.load("svm.pkl")

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/identify', methods=['POST'])
def identify():
  image = request.files['image']
  image.save("temp")
  faces=ml_face.test("temp",pca,clf)
  threshold=0.68
  if len(faces)==0:
    return jsonify({"Narendra Modi": "No","Arvind Kejriwal": "No"})
  else:
    def confidence(x):
      return abs(x[0][0]-x[0][1])
    faces=sorted(faces,key=confidence)
    faces=faces[::-1][:2]
    namo="No"
    kejri="No"
    print faces
    if len(faces)==1:
        if faces[0][0][0] > faces[0][0][1] and faces[0][0][0] >= threshold:
	  kejri="Yes"
        elif faces[0][0][1] > faces[0][0][0] and faces[0][0][1] >= threshold:
	  namo="Yes"
    if len(faces)==2:
      if faces[1][0][0] > faces[1][0][1] and faces[1][0][0] >= threshold:
        kejri="Yes"
      elif faces[1][0][1] > faces[1][0][0] and faces[1][0][1] >= threshold:
        namo="Yes"
    return jsonify({"Narendra Modi": namo,"Arvind Kejriwal": kejri})

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
