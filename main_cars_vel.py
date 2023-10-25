import cv2
from ultralytics import YOLO
from collections import defaultdict

# Cargar el modelo YOLOv8
model = YOLO('yolov8n.pt')
  
# Abrir el archivo de video
video_path = "output7.mp4"
cap = cv2.VideoCapture(video_path)

# Definir la Región de Interés (ROI)
x_start, y_start, width, height = 60, 700, 375, 250  # Ajustar estos valores según video (izquierda, arriba, derecha, abajo)
roi = (x_start, y_start, width, height)

# Almacenar el historial de seguimiento
track_history = defaultdict(lambda: [])

# Contadores para los coches
coches_bajando = 0
coches_subiendo = 0

# Ancho del video para determinar la dirección de los coches
video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

# Variables para calcular velocidad
    # Tasa de fotogramas del vídeo
fps = cap.get(cv2.CAP_PROP_FPS)
    # Escala espacial (píxeles por metro)
scale = 450
    # Diccionario para almacenar las últimas posiciones de los coches
last_positions = {}
    # Contador de frames para saber cuando actualizar la velocidad mostrada
vel_frame_counter = 0 
    # Actualizar la velocidad cada x frames
vel_update_interval = 1
    # Diccionario para almacenar las últimas velocidades de los coches
last_speeds = {}

# Bucle a través de los fotogramas del video
while cap.isOpened():
    success, frame = cap.read() # leer cada frame (success -> si se ha leído o no el frame, true o false)
    if success:
        vel_frame_counter += 1  # Incrementar el contador de frames

        results = model.track(frame, persist=True) # para detectar y seguir objetos del frame
        annotated_frame = results[0].plot() # detecciones realizadas se dibujan en el frame
        boxes = results[0].boxes.xywh.cpu() # cajas delimitadoras de los objetos (de ahi se saca x,y,w,h)
        track_ids = results[0].boxes.id.int().cpu().tolist() # extraer ids unicos de seguimiento para los objetos, pra seguir el mismo a lo largo de varios frames
        class_ids = results[0].boxes.cls.cpu().tolist() # class ids que tiene YOLO para ese objeto (0: person, 1:bici, 2:car, 3:moto...)

        for box, track_id, class_id in zip(boxes, track_ids, class_ids):
            x, y, w, h = box # de cada box de las boxes se saca x,y (coordenadas del centro objeto) y w,h (ancho y alto de la caja / box)
            if class_id == 2:  # Comprobar si el objeto es un coche (En YOLO el coche tiene un class ID de 2)
                if x_start < x < x_start + width and y_start < y < y_start + height:  # Verificar si el coche está dentro de la ROI ('x' e 'y' son las coordenadas del centro del coche)
                    if track_id not in track_history: # se mira si ese coche ya no estaba registrado ya
                        if x < video_width / 2: # si el coche está en la mitad izquierda del video entero significará que está bajando y sino subiendo
                            coches_bajando += 1
                        else:
                            coches_subiendo += 1
                    track_history[track_id].append((float(x), float(y))) # se registra la posicion actual del coche en el diccionario asociada a su track id

                    #Calculo de la velocidad
                    if track_id in last_positions:
                        if vel_frame_counter % vel_update_interval == 0:  # Actualizar solo si el contador es un múltiplo de N
                            last_x, last_y = last_positions[track_id]
                            distance_moved = ((x - last_x)**2 + (y - last_y)**2)**0.5 / scale  # en metros
                            speed = distance_moved * fps * 3.6  # en km/h
                            last_positions[track_id] = (float(x), float(y))
                            last_speeds[track_id] = speed  # Guardar la última velocidad calculada

                    else:
                        last_positions[track_id] = (float(x), float(y))
        
                    # Mostrar la velocidad en el vídeo usando el último valor calculado
                    speed_to_show = last_speeds.get(track_id, 0)  # Usar 0 si el track_id no está en last_speeds
                    cv2.putText(annotated_frame, f"Speed: {speed_to_show:.2f} km/h", (int(x), int(y) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.rectangle(annotated_frame, (x_start, y_start), (x_start + width, y_start + height), (0, 255, 0), 2)  # Dibujar la ROI
        cv2.putText(annotated_frame, f"Coches bajando: {coches_bajando}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # muestra los coches bajando
        cv2.putText(annotated_frame, f"Coches subiendo: {coches_subiendo}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # muestra los coches subiendo
        
        cv2.imshow("YOLOv8 Tracking", annotated_frame) # muestra el frame

        if cv2.waitKey(1) & 0xFF == ord("q"): # si se clicka la 'q' se acaba
            break
    else:
        break


print(f"Coches que han subido (ida): {coches_subiendo}")
print(f"Coches que han bajado (vuelta): {coches_bajando}")

cap.release()
cv2.destroyAllWindows()
