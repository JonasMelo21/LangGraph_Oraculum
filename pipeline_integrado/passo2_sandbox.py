# [DIÁRIO DE BORDO]
# A flag '--rm' é VITAL no LangGraph. Ela diz pro Docker destruir o container 
# completamente assim que o código terminar de rodar, não deixando lixo no PC.

import os
from dotenv import load_dotenv
from google import genai 
import subprocess

# Carrega as variáveis do arquivo .env
load_dotenv("/home/jonasmelo/ProjectsAndStudies/text-to-insight-lab/.env")

# Puxa a variável GEMINI_API_KEY
gemini_api_key = os.getenv("GEMINI_API_KEY")

prompt = """
        Escreva apenas codigo python para ler o arquivo /dados/orders.csv 
        com pandas e mostrar a soma do valor do frete (coluna 'freight').
        Não use crases, markdown ou qualquer caractere especial. Apenas codigo python.
        """

client = genai.Client(api_key=gemini_api_key)
response = client.models.generate_content(model='gemini-2.5-flash',contents=prompt)

with open('pipeline_integrado/codigo_ia.py', 'w') as f:
        f.write(response.text)

raiz = os.getcwd()
vol_dados = f"{raiz}/northwind:/dados"
vol_codigo = f"{raiz}/pipeline_integrado:/app"

comando_run = [
    "docker", "run", "--rm",
    "-v", vol_dados,
    "-v", vol_codigo,
    "imagem_sandbox", 
    "python", "/app/codigo_ia.py" # O comando CMD dinâmico!
]

resultado = subprocess.run(comando_run, capture_output=True, text=True)

if resultado.returncode == 0:
        print("Sucesso! Saída do código:\n")
        print(resultado.stdout)
else:
        print("Deu erro:\n")
        print(resultado.stderr)