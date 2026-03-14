import os
from dotenv import load_dotenv
from google import genai

# Carrega as variáveis do arquivo .env
load_dotenv("/home/jonasmelo/ProjectsAndStudies/text-to-insight-lab/.env")

# Puxa a variável GEMINI_API_KEY
gemini_api_key = os.getenv("GEMINI_API_KEY")

try:
    if not gemini_api_key:
        raise ValueError("Erro: Chave não encontrada")

    client = genai.Client(api_key=gemini_api_key)
    print("Conexão com API Gemini estabelecida com sucesso!\n")

    pergunta = "Qual foi o total gasto em frete pelo cliente Ana Trujillo?"
    schema = "Tabela orders: OrderID, customerID, freight. Tabela customers: customerID, contactName."
    
    # Código com erros de lógica
    codigo_errado = """df_orders = pd.read_csv('orders.csv')
df_customers = pd.read_csv('customers.csv')
merged_df = pd.merge(df_customers, df_orders, on='customerID', how='inner')
result = merged_df[merged_df['contactName'] == 'Ana Trujillo']['freight'].mean()
print(f'Total: {result}')"""
    
    prompt = f"""
Você é um juiz implacável de código Python.
Sua missão é validar se o código gerado responde corretamente à pergunta do usuário baseado no schema.
Não execute o código, apenas analise a lógica.
Se estiver certo, responda 'CORRETO'.
Se houver erro de lógica, responda 'ERRADO: [explique o erro brevemente]' e mostre a correção completa.

Pergunta do usuário: {pergunta}
Schema do banco: {schema}
Código gerado:
{codigo_errado}

Analise se a lógica está correta para responder a pergunta.
"""
    
    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
    print("=" * 80)
    print("ANÁLISE DO JUIZ:")
    print("=" * 80)
    print(response.text)
    print("=" * 80)
    
except ValueError as e:
    print(f"Erro de Valor: {e}")
    exit()
except Exception as e:
    print(f"Erro: {e}")
    exit()
