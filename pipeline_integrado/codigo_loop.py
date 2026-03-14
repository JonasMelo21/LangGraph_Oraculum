import pandas as pd

df = pd.read_csv('/dados/orders.csv')
frete_mais_caro = df['freight'].max()
print(frete_mais_caro)