import pandas

df = pandas.read_csv('/dados/orders.csv')
soma_frete = df['freight'].sum()
print(soma_frete)