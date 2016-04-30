import pandas as pd
df = pd.read_csv("book5.csv")
df[["userid", "bookid", "rating"]].to_csv("linebook5.csv", header=False, index=False)
