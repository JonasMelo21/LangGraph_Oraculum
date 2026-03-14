import os
from dotenv import load_dotenv
from google import genai 
import subprocess

# Carrega as variáveis do arquivo .env
load_dotenv("/home/jonasmelo/ProjectsAndStudies/text-to-insight-lab/.env")

# Puxa a variável GEMINI_API_KEY
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)
pergunta = "Qual foi o frete (freight) mais caro na tabela /dados/orders.csv ?"
prompt = f"""
            Escreva apenas codigo python,
            nada de markdown,crase ou caracteres especiais.
            Apenas codigo python para responder a essa pergunta: {pergunta}"""

response = client.models.generate_content(model='gemini-2.5-flash',contents=prompt)
codigo_gerado = response.text
with open('pipeline_integrado/codigo_loop.py','w') as f:
    f.write(codigo_gerado)

raiz = os.getcwd()
vol_dados = f"{raiz}/northwind:/dados"
vol_codigo = f"{raiz}/pipeline_integrado:/app"

comando_run = [
    "docker", "run", "--rm",
    "-v", vol_dados,
    "-v", vol_codigo,
    "imagem_sandbox", 
    "python", "/app/codigo_loop.py" # O comando CMD dinâmico!
]


resultado = subprocess.run(comando_run, capture_output=True, text=True)

if resultado.returncode == 0:
      saida = resultado.stdout 
else:
        saida = resultado.stderr

prompt_juiz = f"""
              Você é um juiz de codigo.
              Analise os fatos abaixo 
              E diga se o resultado é válido ou se houve erro logico/falha
              Seja direto na avaliação.
              pergunta:{pergunta}
              codigo executado:{codigo_gerado}
              saida do temrinal: {saida}
             """

resposta_juiz = client.models.generate_content(model='gemini-2.5-flash',contents=prompt_juiz)

print("======== Sentença do Juiz ========\n\n")
print("Resposta do juiz:\n",resposta_juiz.text)