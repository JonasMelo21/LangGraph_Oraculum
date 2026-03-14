import subprocess 

# [DIÁRIO DE BORDO - INTEGRAÇÃO]
# Usamos o subprocess.run() em vez de comandos manuais porque o orquestrador 
# precisará instanciar sandboxes dinamicamente e capturar os erros via stderr.

comando_build = ["docker","build","-t","imagem_sandbox","-f",
                 "pipeline_integrado/Dockerfile_sandbox","."]
resultado_build = subprocess.run(comando_build,capture_output=True,text=True)

if resultado_build.returncode == 0:
    print("Deu certo! Build Executado")
    print(resultado_build.stdout)
else:
    print(resultado_build.stderr)
    