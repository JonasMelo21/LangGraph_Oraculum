import time
import sys

while True:
    frase = "Analisando documento... Fantasma vivo!\n"
    
    # Imprime e força a saída imediata dupla
    print(frase, end="", flush=True)
    sys.stdout.flush()
    
    # Salva no arquivo
    with open('/output/historico.log', 'a') as f:
        f.write(frase)
        
    time.sleep(5)