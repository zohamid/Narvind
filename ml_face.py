# Original Reference : https://github.com/ahhda/Face-Recogntion/blob/master/imageproc.py

import os, cv2
from numpy import *
import numpy as np
from PIL import Image
from sklearn.decomposition import PCA, RandomizedPCA
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
# import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.externals import joblib

cascadeLocation = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadeLocation)

def prepare_dataset(directory):
	row = 100
	col = 100
	images = []
	labels = []
	for label in os.listdir(directory):
		temp = os.path.join(directory, label)
		for image in os.listdir(temp):
			image_pil = Image.open(os.path.join(temp, image)).convert('L')
			image = np.array(image_pil, 'uint8')
			faces = faceCascade.detectMultiScale(image)
			for (x,y,w,h) in faces:
				if len(image[y:y+col,x:x+row].flatten()) == row * col:
					images.append(image[y:y+col,x:x+row])
					labels.append(label)
	return images,labels


def train(directory):
	images, labels = prepare_dataset(directory)
	n_components = 10
	pca = RandomizedPCA(n_components=n_components, whiten=True)

	param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
              	'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1], }
	clf = GridSearchCV(SVC(kernel='rbf', class_weight='auto', probability=True),param_grid)

	testing_data = []
	for i in range(len(images)):
		print images[i].flatten().shape
		testing_data.append(images[i].flatten())

	pca = pca.fit(testing_data)

	transformed = pca.transform(testing_data)
	clf.fit(transformed,labels)
	scores = cross_val_score(clf, transformed, labels, cv=5)
	print("Mean cross-validation accuracy")
	print(sum(scores) / 5)
	joblib.dump(clf,"svm.pkl")
	joblib.dump(pca,"pca.pkl")


def test(image_path, pca, clf):
	row = 100
	col = 100
	pred_image_pil = Image.open(image_path).convert('L')
	pred_image = np.array(pred_image_pil, 'uint8')
	faces = faceCascade.detectMultiScale(pred_image)
	detected = []
	for (x,y,w,h) in faces:
		if len(np.array(pred_image[y:y+col,x:x+row]).flatten()) == row*col:
			X_test = pca.transform(np.array(pred_image[y:y+col,x:x+row]).flatten())
			mynbr = clf.predict_proba(X_test)
			detected.append(mynbr)
	return detected

#train("images")
