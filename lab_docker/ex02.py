import os 

senha = os.getenv("DB_PASSWORD")

if senha:
    print("\n\tBem vindo ao text to insight\n\n")
else:
    print("Cilada, bino! Senha não encontrada")