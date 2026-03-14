import numpy as  np
import time 

inicio = time.time()
a = np.random.rand(1000,1000)
b = np.random.rand(1000,1000)
fim = time.time() 
print(f"Tempo pra multiplicar as 2 matriz: {fim - inicio}")