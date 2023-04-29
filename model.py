import pandas
import argparse
from pandas.core.api import DataFrame
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from enum import Enum

class PredictedSignal(Enum):
    """
    In csv data we represent signals as single number - every number has specific meaning
    """
    SELL = 0
    NOTHING = 1
    BUY = 2

class Model:
    def __init__(self, df: DataFrame):
        features = ['Open', 'High', 'Low', 'Close', 'Volume']
        target = 'Buy/Sell'
        self.model = self.__generate_model(df, features, target)

    def predict_signal(self, df: DataFrame) -> PredictedSignal:
        prediction = self.model.predict(df)[0]
        return PredictedSignal(prediction)

    def __generate_model(self, df: pandas.DataFrame, features: list[str], target: str) -> DecisionTreeClassifier:
        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
        clf = DecisionTreeClassifier()
        clf = clf.fit(X_train, y_train)

        return clf

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input data file in csv format", required=True)
    args = parser.parse_args()

    df = pandas.read_csv(args.input)
    # df = pandas.read_csv("data/btc/target/btc-usd_2018-04-23_2023-04-23_target.csv")
    model = Model(df)
    dtree = model.model
    print(f"Importances: {dtree.feature_importances_}")

