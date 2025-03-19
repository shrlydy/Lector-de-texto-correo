import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import pytesseract
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import difflib  # Para comparación de similitud de texto

# Función para enviar un correo
def enviar_correo(asunto, mensaje, destinatario_email):
    from_email = 'dp17613@gmail.com'  # Cambia esto por tu correo
    from_password = 'nqcw nrni jjnc hywd'  # Usa una contraseña de aplicación si es Gmail

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = destinatario_email
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    server.sendmail(from_email, destinatario_email, msg.as_string())
    server.quit()

# Función para calcular similitud de texto
def similaridad_texto(texto, frase_clave, umbral_similitud=0.2):
    similitud = difflib.SequenceMatcher(None, texto.lower(), frase_clave.lower()).ratio()
    return similitud >= umbral_similitud

# Cargar la imagen en escala de grises
ruta_imagen = "Pelon.jpeg"
img = cv.imread(ruta_imagen, cv.IMREAD_GRAYSCALE)

assert img is not None, "No se pudo leer la imagen."

# Preprocesamiento de la imagen para mejorar la detección del texto
_, thresh = cv.threshold(img, 120, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
blurred = cv.GaussianBlur(thresh, (5, 5), 0)
equalized = cv.equalizeHist(blurred)

# Extraer texto con pytesseract
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(equalized, config=custom_config)

# Imprimir el texto extraído
print("Texto extraído con OCR:")
print(text)

#Crea una mascara blanca en la imagen
mask = np.zeros_like(img)
#efdfdg
#Quita objetos pequeños
#for cnt in contours:
 #   area = cv.contourArea(cnt)
  #  if area > 500:
   #     cv.drawContours(mask, [cnt], -1, (255), thickness=cv.FILLED)

#Aplicar mascara a la imagen original
result = cv.bitwise_and(blurred, mask)

#Resultados con matplotlib
plt.figure(figsize=(10,4))
# Definir las frases clave
frases_clave = ["De: Karen", "Para: Dylan"]

# Verificar si alguna frase clave aparece con al menos 50% de similitud
enviar_correo_flag = any(similaridad_texto(text, frase, umbral_similitud=0.2) for frase in frases_clave)

if enviar_correo_flag:
    # Enviar correo con el texto extraído
    asunto = "Texto Detectado en Imagen"
    mensaje = f"Se detectó una coincidencia en la imagen.\n\nTexto extraído:\n{text}"
    destinatario_email = "a01541014@tec.mx"  # Cambia esto por el email del destinatario

    enviar_correo(asunto, mensaje, destinatario_email)
    print("Correo enviado exitosamente.")
else:
    print("No se detectó ninguna coincidencia significativa.")

# Mostrar imágenes procesadas
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
