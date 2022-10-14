import pickle
from flask import Flask, render_template, request
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    iris = load_iris()
    model = KNeighborsClassifier(n_neighbors = 3)
    X_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target)
    model.fit(X_train, y_train)
    pickle.dump(model, open("iris.pkl", "wb"))

    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    sepal_length = request.form['sepal_length'] # Save user input in function (later export to mongo)
    sepal_width = request.form['sepal_width']
    petal_length = request.form['petal_length']
    petal_width = request.form['petal_width']

    form_array = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    model = pickle.load(open("iris.pkl", "rb"))
    prediction = model.predict(form_array)[0]

    if prediction == 0:
        result = "Iris Setosa"
    elif prediction == 1:
        result = "Iris Versocolor"
    else:
        result = "Iris Virginica"

    return render_template("result.html", result = result)

if __name__ == "__main__":
    app.run(debug=True)