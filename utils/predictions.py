from sklearn.linear_model import LinearRegression
import numpy as np

def predict_next_day(df):

    df = df.copy()

    df["Target"] = df["Close"].shift(-1)

    df.dropna(inplace=True)

    X = np.arange(len(df)).reshape(-1, 1)

    y = df["Target"]

    model = LinearRegression()

    model.fit(X, y)

    next_day = np.array([[len(df)]])

    prediction = model.predict(next_day)

    return round(prediction[0], 2)