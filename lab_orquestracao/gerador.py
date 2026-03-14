import os
from dotenv import load_dotenv
from google import genai 

# Carrega as variáveis do arquivo .env
load_dotenv("/home/jonasmelo/ProjectsAndStudies/text-to-insight-lab/.env")

# Puxa a variável GEMINI_API_KEY
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Abre o arquivo do schema
with open("/home/jonasmelo/ProjectsAndStudies/text-to-insight-lab/northwind/docs_northwind/tabelas_descricao.txt") as f:
    schema_banco = f.read()

print("Chave API carregada com sucesso!\n\n")
print(schema_banco[:150])

# Bloco try para checar chave, conectar à API e fazer requisição
try:
    if not gemini_api_key:
        raise ValueError("Erro: Chave não encontrada!")
    
    client = genai.Client(api_key=gemini_api_key)
    print("\nConexão com API Gemini estabelecida com sucesso!")
    
    prompt = f"""
Aja como analista de dados e retorna APENAS e EXCLUSIVAMENTE código python usando biblioteca pandas.
Está proibido uso de crases, markdown, caracteres especiais e etc. Apenas codigo python.
Evite saudações também. APENAS CODIGO PYTHON.
Mande um codigo para ler esse arquivo {schema_banco} e mostrar o preço médio do frete (Freight)
"""
    
    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
    print("\nResposta da API Gemini recebida com sucesso!\n")
    print(response.text)

except Exception as e:
    print(f"Erro: {e}")
    exit()