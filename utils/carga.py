
import pandas as pd


def load_excel(data):
    data = pd.read_excel(data)
    return data
def load_csv(data):
    data = pd.read_csv(data)
    return data
