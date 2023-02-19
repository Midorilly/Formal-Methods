import pandas as pd
import re

def load_data():
    df = pd.read_csv("split_pm_output.csv")
    return df

def split(df):
    split_dataset = []


    return split_dataset


def main():
    dataset = load_data()
    dt = split(dataset)
    print(dt)
    return

if __name__ == "__main__":
    main()