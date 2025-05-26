# estilo_nst.py

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import copy


stop_training = False  # Flag global para detener

def cancelar_entrenamiento():
    global stop_training
    stop_training = True



# --- TRANSFORMACIONES ---
loader = transforms.Compose([
    transforms.Resize((400, 400)),  # Ajusta según tu interfaz
    transforms.ToTensor()
])

unloader = transforms.ToPILImage()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def cargar_imagen(ruta):
    imagen = Image.open(ruta).convert("RGB")
    imagen = loader(imagen).unsqueeze(0)
    return imagen.to(device, torch.float)


# --- CAPAS DE ESTILO ---
class FeatureExtractor(nn.Module):
    def __init__(self, cnn):
        super(FeatureExtractor, self).__init__()
        self.selected_layers = {'0', '5', '10', '19', '28'}  # Capas conv relevantes
        self.model = nn.Sequential()
        for name, layer in cnn.features._modules.items():
            self.model.add_module(name, layer)
            if name == '29':
                break

    def forward(self, x):
        features = []
        for name, layer in self.model._modules.items():
            x = layer(x)
            if name in self.selected_layers:
                features.append(x)
        return features


# --- FUNCIONES DE PERDIDA ---
def gram_matrix(tensor):
    b, c, h, w = tensor.size()
    features = tensor.view(b * c, h * w)
    G = torch.mm(features, features.t())
    return G.div(b * c * h * w)


# --- FUNCIÓN PRINCIPAL ---
def aplicar_estilizado_nst(ruta_contenido, ruta_estilo, ruta_salida):
    contenido = cargar_imagen(ruta_contenido)
    estilo = cargar_imagen(ruta_estilo)
    input_img = contenido.clone()

    cnn = models.vgg19(pretrained=True).to(device).eval()
    extractor = FeatureExtractor(cnn).to(device)

    optimizer = torch.optim.LBFGS([input_img.requires_grad_()])
    style_features = extractor(estilo)
    content_features = extractor(contenido)

    style_grams = [gram_matrix(f) for f in style_features]

    # Pesos
    style_weight = 1e6
    content_weight = 1

    print("Iniciando transferencia de estilo...")

    steps = [0]
    #while steps[0] <= 300:
    #while steps[0] <= 500:
    global stop_training
    stop_training = False  # Reiniciar al comenzar

    while steps[0] <= 500 and not stop_training:

        def closure():
            input_img.data.clamp_(0, 1)
            optimizer.zero_grad()

            input_features = extractor(input_img)
            content_loss = F.mse_loss(input_features[2], content_features[2])

            style_loss = 0
            for i in range(len(style_grams)):
                G = gram_matrix(input_features[i])
                A = style_grams[i]
                style_loss += F.mse_loss(G, A)

            total_loss = content_weight * content_loss + style_weight * style_loss
            total_loss.backward(retain_graph=True) # Usamos retain_graph=True porque LBFGS llama múltiples veces a closure()
                                                   # y necesita reutilizar el grafo de cómputo sin que se liberen los tensores
            steps[0] += 1

            if steps[0] % 50 == 0:
                print(f"Paso {steps[0]} | Pérdida total: {total_loss.item():.4f}")

            return total_loss

        optimizer.step(closure)

    input_img.data.clamp_(0, 1)
    imagen_final = input_img.cpu().clone().squeeze(0)
    imagen_pil = unloader(imagen_final)
    imagen_pil.save(ruta_salida)
    print(f"Estilo aplicado y guardado en {ruta_salida}")