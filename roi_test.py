import cv2
import os
from datetime import datetime
from ultralytics import YOLO

# Load your trained YOLO model
model = YOLO("V1_head.1_ICF_RYK_V1_best.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Create folder if not exist
save_dir = "New Alert"
os.makedirs(save_dir, exist_ok=True)

# Define ROI zones
zone_A = (100, 100, 400, 400)  # x1, y1, x2, y2
zone_B = (450, 100, 750, 400)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO detection
    results = model(frame, stream=True)

    # Draw ROI zones
    cv2.rectangle(frame, (zone_A[0], zone_A[1]), (zone_A[2], zone_A[3]), (255, 0, 0), 2)
    cv2.putText(frame, "Zone A", (zone_A[0], zone_A[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.rectangle(frame, (zone_B[0], zone_B[1]), (zone_B[2], zone_B[3]), (0, 255, 0), 2)
    cv2.putText(frame, "Zone B", (zone_B[0], zone_B[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Loop detections
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]

            # Center of the box
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

            # Default color
            color = (0, 0, 255)
            zone_label = "Outside"

            # Check zones
            if zone_A[0] < cx < zone_A[2] and zone_A[1] < cy < zone_A[3]:
                color = (255, 0, 0)
                zone_label = "Zone A"
            elif zone_B[0] < cx < zone_B[2] and zone_B[1] < cy < zone_B[3]:
                color = (0, 255, 0)
                zone_label = "Zone B"

                # ✅ Save frame if head detected in Zone B
                if label.lower() == "head":  # agar tumhara class name 'head' hai
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    filename = os.path.join(save_dir, f"frame_{timestamp}.jpg")
                    cv2.imwrite(filename, frame)
                    print(f"[ALERT] Head detected in Zone B → frame saved: {filename}")

            # Draw detection and zone info
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, (cx, cy), 5, color, -1)
            cv2.putText(frame, f"{label} ({zone_label})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Show frame
    cv2.imshow("ROI Test", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()



# import cv2
# import os
# from datetime import datetime
# from ultralytics import YOLO

# # Load your trained YOLO model
# model = YOLO("V1_head.1_ICF_RYK_V1_best.pt")  # apna model path lagao

# # Open webcam
# cap = cv2.VideoCapture(0)

# # Create folder if not exist
# save_dir = "New Alert/roi_test"
# os.makedirs(save_dir, exist_ok=True)

# # Define ROI zones
# zone_A = (80, 50, 380, 200)  # x1, y1, x2, y2
# zone_B = (450, 100, 750, 400)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # YOLO detection
#     results = model(frame, stream=True)

#     # Draw ROI zones
#     cv2.rectangle(frame, (zone_A[0], zone_A[1]), (zone_A[2], zone_A[3]), (255, 0, 0), 2)
#     cv2.putText(frame, "Zone A", (zone_A[0], zone_A[1] - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

#     cv2.rectangle(frame, (zone_B[0], zone_B[1]), (zone_B[2], zone_B[3]), (0, 255, 0), 2)
#     cv2.putText(frame, "Zone B", (zone_B[0], zone_B[1] - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     # Loop detections
#     for r in results:
#         boxes = r.boxes
#         for box in boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             conf = float(box.conf[0])
#             cls = int(box.cls[0])
#             label = model.names[cls]

#             # Center of the box
#             cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

#             # Default color
#             color = (0, 0, 255)
#             zone_label = "Outside"

#             # Check zones
#             if zone_A[0] < cx < zone_A[2] and zone_A[1] < cy < zone_A[3]:
#                 color = (255, 0, 0)
#                 zone_label = "Zone A"

#                 # ✅ Save frame if head detected in Zone A
#                 if label.lower() == "head":
#                     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
#                     filename = os.path.join(save_dir, f"frame_{timestamp}.jpg")
#                     cv2.imwrite(filename, frame)
#                     print(f"[ALERT] Head detected in Zone A → frame saved: {filename}")

#             elif zone_B[0] < cx < zone_B[2] and zone_B[1] < cy < zone_B[3]:
#                 color = (0, 255, 0)
#                 zone_label = "Zone B"

#             # Draw detection and zone info
#             cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#             cv2.circle(frame, (cx, cy), 5, color, -1)
#             cv2.putText(frame, f"{label} ({zone_label})", (x1, y1 - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#     # Show frame
#     cv2.imshow("ROI Test", frame)
#     if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
#         break

# cap.release()
# cv2.destroyAllWindows()
