# Parking-car-flow-tracking-G06
Repte Tracking - Grup 06 - Mètodes Avançats de Processament de Senyal, Imatge i Vídeo - 2023

## Descripción:

Este proyecto tiene como objetivo determinar el número de coches que suben y bajan en una carretera utilizando el algoritmo de YOLOv8. Esta solución es útil para controlar el flujo de vehículos en una carretera o para determinar el grado de ocupación de un estacionamiento.

## Instrucciones:

1. **Configuración previa**:
   - Asegúrese de tener instaladas las bibliotecas `cv2` y `ultralytics`.
   - Asegúrese de tener el modelo de YOLOv8 y el archivo de video que se quiere procesar.

2. **Ejecución**:
   - Modifique la variable `video_path` en `main.py` para apuntar al archivo de video deseado.
   - Ejecute el script `main.py`. Durante la ejecución, se mostrará un video que resalta los objetos y coches detectados, su velocidad y contará el número de coches que suben y bajan a través de una Región de Interés (ROI).

3. **Resultados**:
   - Al final de la ejecución, el script imprimirá el número total de coches que han subido y bajado, y también mostrará el tiempo total de ejecución.

## Características:

- **Detección y Seguimiento**: Utiliza YOLOv8 para detectar y seguir coches en un video.
- **Cálculo de Velocidad**: Calcula y muestra la velocidad de cada coche en km/h.
- **Conteo de Coches**: Cuenta el número de coches que sube y baja a través de una ROI definida.
  
## Notas:

- La Región de Interés (ROI) se puede ajustar modificando las variables `x_start`, `y_start`, `width` y `height` en `main.py`.
- El intervalo de actualización del seguimiento y el cálculo de velocidad se pueden ajustar mediante las variables `tracking_update_interval` y `vel_update_interval`.

---

## Contribuciones y Agradecimientos:

Este proyecto fue desarrollado basándose en el enfoque de seguimiento de objetos YOLOv8 y utilizando la biblioteca ultralytics.


### Equipo:
Carlos Leta - 1599255@uab.cat,
Abel Espín - 1605961@uab.cat,
Andreu Cuevas - 1570422@uab.cat
