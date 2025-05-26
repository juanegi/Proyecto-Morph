import torch
import time

print("Probando rendimiento en GPU (si está disponible)...")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Usando:", device)

# Crear un tensor grande
x = torch.randn(10000, 10000).to(device)

# Medir tiempo en GPU
start = time.time()
for _ in range(100):
    y = x @ x
torch.cuda.synchronize()  # Esperar que termine todo
end = time.time()

print(f"Tiempo en {device}: {end - start:.4f} segundos")
