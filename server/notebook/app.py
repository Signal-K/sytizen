from flask import Flask, render_template
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle

app = Flask(__name__)

@app.route("/")
def home():
    iris = load_iris()
    model = KNeighborsClassifier(n_neighbors = 3)
    X_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target)
    model.fit(X_train, y_train)
    pickle.dumps(model, open("iris.pkl", "wb"))

    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    pass

if __name__ == "__main__":
    app.run(debug=True)