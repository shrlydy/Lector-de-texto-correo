import numpy as np  # Biblioteca para operaciones numéricas
from matplotlib import pyplot as plt  # Para mostrar imágenes y gráficos
import cv2 as cv  # OpenCV para manipulación de imágenes
import pytesseract  # OCR para extraer texto de imágenes
import smtplib  # Para el envío de correos electrónicos
from email.mime.text import MIMEText  # Para formatear correos con texto
from email.mime.multipart import MIMEMultipart  # Para enviar correos con múltiples partes
import difflib  # Para comparación de similitud entre textos

# Función para enviar un correo
def enviar_correo(asunto, mensaje, destinatario_email, from_email, from_password):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Servidor SMTP de Gmail y puerto
        server.starttls()  # Iniciar cifrado TLS para seguridad
        server.login(from_email, from_password)  # Iniciar sesión en el servidor SMTP

        msg = MIMEMultipart()  # Crear el mensaje de correo
        msg['From'] = from_email  # Remitente
        msg['To'] = destinatario_email  # Destinatario
        msg['Subject'] = asunto  # Asunto del correo
        msg.attach(MIMEText(mensaje, 'plain'))  # Adjuntar el mensaje como texto plano

        server.sendmail(from_email, destinatario_email, msg.as_string())  # Enviar el correo
        server.quit()  # Cerrar conexión con el servidor SMTP
        print(f"Correo enviado desde {from_email} a {destinatario_email}")  # Confirmación en consola
    
    except Exception as e:
        print(f"Error al enviar correo: {e}")  # Manejo de errores

# Función para comparar similitud de texto
def similaridad_texto(texto, frase_clave, umbral_similitud=0.5):
    similitud = difflib.SequenceMatcher(None, texto.lower(), frase_clave.lower()).ratio()  # Calcular similitud
    return similitud >= umbral_similitud  # Devolver True si la similitud supera el umbral

# Carga y procesamiento de imagen
ruta_imagen = "Pelon.jpeg"  # Ruta de la imagen
img = cv.imread(ruta_imagen, cv.IMREAD_GRAYSCALE)  # Cargar imagen en escala de grises
assert img is not None, "No se pudo leer la imagen."  # Verificar que la imagen se cargó correctamente

# Preprocesamiento para mejorar la detección del texto
_, thresh = cv.threshold(img, 120, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)  # Aplicar umbral adaptativo
blurred = cv.GaussianBlur(thresh, (5, 5), 0)  # Aplicar desenfoque para reducir ruido
equalized = cv.equalizeHist(blurred)  # Mejorar el contraste con ecualización del histograma

# Extraer texto con pytesseract
custom_config = r'--oem 3 --psm 6'  # Configuración del OCR para mejor precisión
text = pytesseract.image_to_string(equalized, config=custom_config).strip()  # Extraer texto y limpiar espacios

# Imprimir el texto extraído
print("\n--- Texto extraído con OCR ---")
print(text)

# Configuración de correos
correo_general = "dp17613@gmail.com"  # Correo principal
contraseña_general = "nqcw nrni jjnc hywd"  # Contraseña del correo principal
destinatario_general = "a01540618@tec.mx"  # Destinatario del correo general

correo_dylan = "dp17613@gmail.com"  # Correo secundario para envíos específicos
contraseña_dylan = "nqcw nrni jjnc hywd"  # Contraseña del correo secundario
destinatario_dylan = "a01541014@tec.mx"  # Destinatario del correo secundario

# Frase clave para detección flexible
frase_dylan_a_karen = "De: Dylan Para: Karen"  # Frase que se busca en el texto extraído

# Lógica para envío de correos
if text:  # Verificar si se detectó texto en la imagen
    if similaridad_texto(text, frase_dylan_a_karen):  # Verificar si el texto extraído contiene la frase clave
        # Extraer el texto debajo de "De: Dylan Para: Karen"
        texto_bajo = text.split(frase_dylan_a_karen, 1)[1].strip() if frase_dylan_a_karen in text else text  # Obtener solo el mensaje
        print(f"Texto debajo: {texto_bajo}")  # Imprimir el texto encontrado

        # Enviar desde el otro correo
        asunto = "Mensaje de Dylan a Karen Detectado"
        mensaje = f"Se ha detectado un mensaje de Dylan para Karen.\n\nTexto extraído:\n'{texto_bajo}'"
        enviar_correo(asunto, mensaje, destinatario_dylan, correo_dylan, contraseña_dylan)  # Enviar correo
    else:
        # Enviar desde el correo general
        asunto = "Texto Detectado en Imagen"
        mensaje = f"Se detectó el siguiente texto en la imagen:\n\n{text}"
        enviar_correo(asunto, mensaje, destinatario_general, correo_general, contraseña_general)  # Enviar correo general
else:
    print("No se detectó texto en la imagen.")  # Mensaje si no hay texto en la imagen

# Mostrar imágenes procesadas
plt.figure(figsize=(10, 4))  # Definir el tamaño de la figura para visualización

plt.subplot(1, 3, 1)  # Primera imagen
plt.imshow(img, cmap='gray')  # Mostrar imagen original en escala de grises
plt.title('1. Original Image')  # Título de la imagen
plt.xticks([]), plt.yticks([])  # Ocultar ejes

plt.subplot(1, 3, 2)  # Segunda imagen
plt.imshow(blurred, cmap='gray')  # Mostrar imagen procesada con umbral + desenfoque
plt.title('2. Umbral + Blur')
plt.xticks([]), plt.yticks([])

plt.subplot(1, 3, 3)  # Tercera imagen
plt.imshow(equalized, cmap='gray')  # Mostrar imagen con contraste mejorado
plt.title('3. With Contrast')
plt.xticks([]), plt.yticks([])

plt.tight_layout()  # Ajustar diseño de las imágenes
plt.show()  # Mostrar las imágenes procesadas