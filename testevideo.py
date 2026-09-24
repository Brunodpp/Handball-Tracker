import os

import cv2
from ultralytics import YOLO


model = YOLO("yolov8n.pt")

path = "videos_raw/fuchseberlin.webm"
cap = cv2.VideoCapture(path)
cont = 0
FRAME_SKIP = 10
a = os.listdir("data")
if a:
    cont = int(a[-1][3:-4])

# Extended key codes returned by cv2.waitKeyEx on Windows.
LEFT_ARROW = 2424832
RIGHT_ARROW = 2555904

while True:
    ret, frame = cap.read()
    if not ret:
        print("Fim do video ou erro ao ler o frame.")
        break

    frame = cv2.resize(frame, (1280, 720))
    #results = model(frame, verbose=False)

    # for result in results:
    #     for box in result.boxes:
    #         # Valores da bounding box no formato x1, y1, x2, y2.
    #         x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().tolist())
    #         confidence = float(box.conf[0].cpu())
    #         class_id = int(box.cls[0].cpu())
    #         class_name = result.names[class_id]
    #         label = f"{class_name} {confidence:.2f}"
    #         color = (0, 255, 0)

    #         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    #         # Desenha um fundo solido para o rotulo ficar legivel.
    #         (text_width, text_height), baseline = cv2.getTextSize(
    #             label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
    #         )
    #         label_bottom = max(y1, text_height + baseline + 4)
    #         cv2.rectangle(
    #             frame,
    #             (x1, label_bottom - text_height - baseline - 4),
    #             (x1 + text_width + 4, label_bottom),
    #             color,
    #             -1,
    #         )
    #         cv2.putText(
    #             frame,
    #             label,
    #             (x1 + 2, label_bottom - baseline - 2),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             0.6,
    #             (0, 0, 0),
    #             2,
    #             cv2.LINE_AA,
    #         )

    cv2.imshow("Handball Tracker - YOLOv8", frame)
    key = cv2.waitKeyEx(25)

    if key == ord("c"):
        cont += 1
        cv2.imwrite(f"data/img{cont}.jpg", frame)
        print("salvo")
    elif key == ord("q"):
        break
    elif key in (LEFT_ARROW, RIGHT_ARROW):
        # cap.read() leaves the position at the frame after the displayed one.
        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
        direction = -4 if key == LEFT_ARROW else 4
        target_frame = max(0, current_frame + direction * FRAME_SKIP)
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

cap.release()
cv2.destroyAllWindows()
