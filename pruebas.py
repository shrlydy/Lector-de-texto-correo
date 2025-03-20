import numpy as np
from matplotlib import pyplot as plt
import pytesseract
from email.mime.text import MIMEText

# *Configuración de correos*
correo_general = "dp17613@gmail.com"
contraseña_general = "nqcw nrni jjnc hywd"
destinatario_general = "a01540618@tec.mx"

correo_dylan = "moscanegra@gmail.com"  #Otro correo para enviar si es de Dylan a Karen
contraseña_dylan = "cacacaca"
destinatario_dylan = "karencorreo@gmail.com"

# *Frase clave para detección flexible*
frase_dylan_a_karen = "De: Dylan Para: Karen"

# *Lógica para envío de correos*
if text:
    if similaridad_texto(text, frase_dylan_a_karen):
        # Extraer el texto debajo de "De: Dylan Para: Karen"
        texto_bajo = text.split(frase_dylan_a_karen, 1)[1].strip() if frase_dylan_a_karen in text else text
        print(f"Texto debajo: {texto_bajo}")

        # Enviar desde el otro correo
        asunto = "Mensaje de Dylan a Karen Detectado"
        mensaje = f"Se ha detectado un mensaje de Dylan para Karen.\n\nTexto extraído:\n'{texto_bajo}'"
        enviar_correo(asunto, mensaje, destinatario_dylan, correo_dylan, contraseña_dylan)

    else:
        # Enviar desde el correo general
        asunto = "Texto Detectado en Imagen"
        mensaje = f"Se detectó el siguiente texto en la imagen:\n\n{text}"
        enviar_correo(asunto, mensaje, destinatario_general, correo_general, contraseña_general)

else:
    print("No se detectó texto en la imagen.")

# *Mostrar imágenes procesadas*
plt.figure(figsize=(10, 4))

plt.subplot(1, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('1. Imagen Original')
plt.xticks([]), plt.yticks([])

plt.subplot(1, 3, 2)
plt.imshow(blurred, cmap='gray')
plt.title('2. Umbral + Blur')
plt.xticks([]), plt.yticks([])

plt.subplot(1, 3, 3)
plt.imshow(equalized, cmap='gray')
plt.title('3. Contraste Mejorado')
plt.xticks([]), plt.yticks([])

plt.tight_layout()
plt.show()