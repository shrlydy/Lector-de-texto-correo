import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import pytesseract


# Carga la imagen en escala de frises
img = cv.imread('Karen2.jpeg', cv.IMREAD_GRAYSCALE)
assert img is not None, "File could not be read, check with os.path.exists()"

#Aplica un limite a las placas negras
_, thresh = cv.threshold(img, 100, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)



#Aplica una medio de borradopara eliminar ruido
blurred = cv.GaussianBlur(thresh, (5,5), 0)

# Encontrar contornos
contours, _ = cv.findContours(blurred, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#Crea una mascara blanca en la imagen
mask = np.zeros_like(img)

#Quita objetos pequeños
#for cnt in contours:
 #   area = cv.contourArea(cnt)
  #  if area > 500:
   #     cv.drawContours(mask, [cnt], -1, (255), thickness=cv.FILLED)

#Aplicar mascara a la imagen original
result = cv.bitwise_and(blurred, mask)

#Resultados con matplotlib
plt.figure(figsize=(10,4))

plt.subplot(1,3,1)
plt.imshow(img, cmap='gray')
plt.title('1. Imagen Original')
plt.xticks([]), plt.yticks([])

plt.subplot(1,3,2)
plt.imshow(blurred, cmap='gray')
plt.title('2. Umbral + Blur')
plt.xticks([]), plt.yticks([])

plt.subplot(1,3,3)
plt.imshow(result, cmap='gray')
plt.title('3. Barcode Removed')
plt.xticks([]), plt.yticks([])

plt.tight_layout()
plt.show()


#OCR
config = "--psm 6"  # Modo de segmentación óptimo para texto disperso
text = pytesseract.image_to_string(result, config=config)
print(text)

