import argparse
import time
import sys
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

# from roi_test import zone_A

import cv2
from ultralytics import YOLO

# 🔹 Load environment variables
load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")

#------------------------------------------------------>>>> Gmail Alert Code <<<<<--------------------------------#

def send_email_alert(image_path):
    """Send Gmail alert with the detected image"""
    try:
        msg = EmailMessage()
        msg["Subject"] = "🚨 YOLO ALERT: Head Detected"
        msg["From"] = GMAIL_USER
        msg["To"] = ALERT_EMAIL
        msg.set_content(f"A head was detected. See attached image.\n\nFile: {image_path}")

        # attach image
        with open(image_path, "rb") as f:
            img_data = f.read()
            msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename=os.path.basename(image_path))

        # send mail
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.send_message(msg)
        print(f"📩 Gmail alert sent successfully → {ALERT_EMAIL}")

    except Exception as e:
        print(f"⚠️ Error sending email: {e}")
#------------------------------------------------------>>>> Gmail Alert Code <<<<<--------------------------------#




#------------------------------------------------------>>>> YOLO Live Code <<<<<--------------------------------
def parse_args():
    p = argparse.ArgumentParser(description='Live YOLO on webcam')
    p.add_argument('--model', type=str, default='V1_head.1_ICF_RYK_V1_best.pt', help='path to YOLO model (.pt)')
#######---------- agr default 0 kro gai to live webcam chale ga ----------- agr offlibe video chala na he to us ka path lagawo-------###################
    p.add_argument('--source', type=str, default='0', help='webcam index or video file')
########---------- agr default 0 kro gai to live webcam chale ga ----------- agr offlibe video chala na he to us ka path lagawo-------#################
    p.add_argument('--conf', type=float, default=0.40, help='confidence threshold')
    p.add_argument('--show', type=lambda s: s.lower() not in ['false','0'], default=True, help='show window')
    return p.parse_args()


def main():
    args = parse_args()

    save_dir = "New Alert"
    os.makedirs(save_dir, exist_ok=True)

    try:
        import torch
        device = 0 if torch.cuda.is_available() else 'cpu'
    except Exception:
        device = 'cpu'

    print(f"Loading model {args.model} on device {device} ...")
    model = YOLO(args.model)

    try:
        class_names = model.names
    except Exception:
        class_names = None

    src = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        print('ERROR: Could not open video source:', src)
        sys.exit(1)

    prev_time = 0
    fps = 30
    print('Press q to quit')

    while True:
        ret, frame = cap.read()
        if not ret:
            print('Stream ended or cannot fetch frame')
            break

        results = model(frame, device=device, conf=args.conf, verbose=False)
        r = results[0]
        boxes = getattr(r, 'boxes', None)

        head_detected = False

        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                xyxy = box.xyxy[0].tolist()
                conf = float(box.conf[0]) if hasattr(box, 'conf') else 0.0
                cls_id = int(box.cls[0]) if hasattr(box, 'cls') else None

                x1, y1, x2, y2 = map(int, xyxy)
                label = f"id:{cls_id} {conf:.2f}"
                if class_names and cls_id in class_names:
                    label = f"{class_names[cls_id]} {conf:.2f}"

                if class_names and class_names[cls_id].lower() == "head":
                    head_detected = True

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), (0, 255, 0), -1)
                cv2.putText(frame, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

        # ✅ Save frame and send email alert if head detected
        if head_detected:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            save_path = os.path.join(save_dir, f"frame_{timestamp}.jpg")
            cv2.imwrite(save_path, frame)
            print(f"[ALERT] Head detected → frame saved: {save_path}")
            send_email_alert(save_path)

        curr_time = time.time()
        fps = 0.9 * fps + 0.1 * (1.0 / (curr_time - prev_time)) if prev_time != 0 else 0
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        if args.show:
            cv2.imshow('YOLO Live', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


# if __name__ == '__main__':
main()

########################################### updated code ###########################################

# import argparse
# import time
# import sys
# import os
# from datetime import datetime
# import smtplib
# from email.message import EmailMessage
# from dotenv import load_dotenv
# load_dotenv()

# # import ROI helpers
# from roi_test import zone_A, draw_zone

# import cv2
# from ultralytics import YOLO


# # ------------------------------------------------------>>>> Gmail Alert Code <<<<<--------------------------------
# GMAIL_USER = os.getenv("GMAIL_USER")
# GMAIL_PASS = os.getenv("GMAIL_PASS")
# ALERT_EMAIL = os.getenv("ALERT_EMAIL")


# def send_email_alert(image_path):
#     """Send Gmail alert with the detected image"""
#     try:
#         msg = EmailMessage()
#         msg["Subject"] = "🚨 YOLO ALERT: Head Detected in Zone A"
#         msg["From"] = GMAIL_USER
#         msg["To"] = ALERT_EMAIL
#         msg.set_content(f"A head was detected inside Zone A.\n\nFile: {image_path}")

#         with open(image_path, "rb") as f:
#             img_data = f.read()
#             msg.add_attachment(img_data, maintype="image", subtype="jpeg",
#                                filename=os.path.basename(image_path))

#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#             smtp.login(GMAIL_USER, GMAIL_PASS)
#             smtp.send_message(msg)

#         print(f"📩 Gmail alert sent successfully → {ALERT_EMAIL}")

#     except Exception as e:
#         print(f"⚠️ Error sending email: {e}")
# # ------------------------------------------------------>>>> Gmail Alert Code <<<<<--------------------------------


# # ------------------------------------------------------>>>> YOLO Live Code <<<<<--------------------------------
# def parse_args():
#     p = argparse.ArgumentParser(description='Live YOLO on webcam or video')
#     p.add_argument('--model', type=str, default='V1_head.1_ICF_RYK_V1_best.pt',
#                    help='path to YOLO model (.pt)')
#     # '0' for webcam, or provide video path
#     p.add_argument('--source', type=str, default='0',
#                    help='webcam index or video file')
#     p.add_argument('--conf', type=float, default=0.40,
#                    help='confidence threshold')
#     p.add_argument('--show', type=lambda s: s.lower() not in ['false', '0'],
#                    default=True, help='show window')
#     return p.parse_args()


# def main():
#     args = parse_args()

#     save_dir = "New Alert"
#     os.makedirs(save_dir, exist_ok=True)

#     try:
#         import torch
#         device = 0 if torch.cuda.is_available() else 'cpu'
#     except Exception:
#         device = 'cpu'

#     print(f"Loading model {args.model} on device {device} ...")
#     model = YOLO(args.model)
#     class_names = getattr(model, 'names', None)

#     src = int(args.source) if args.source.isdigit() else args.source
#     cap = cv2.VideoCapture(src)
#     if not cap.isOpened():
#         print('ERROR: Could not open video source:', src)
#         sys.exit(1)

#     prev_time = 0
#     fps = 30
#     print('Press q to quit')

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print('Stream ended or cannot fetch frame')
#             break

#         results = model(frame, device=device, conf=args.conf, verbose=False)
#         r = results[0]
#         boxes = getattr(r, 'boxes', None)

#         head_in_zoneA = False

#         if boxes is not None and len(boxes) > 0:
#             for box in boxes:
#                 xyxy = box.xyxy[0].tolist()
#                 conf = float(box.conf[0]) if hasattr(box, 'conf') else 0.0
#                 cls_id = int(box.cls[0]) if hasattr(box, 'cls') else None

#                 x1, y1, x2, y2 = map(int, xyxy)
#                 label = f"id:{cls_id} {conf:.2f}"
#                 if class_names and cls_id in class_names:
#                     label = f"{class_names[cls_id]} {conf:.2f}"

#                 # draw detection box
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
#                 cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), (0, 255, 0), -1)
#                 cv2.putText(frame, label, (x1, y1 - 4),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

#                 # ✅ check if head is inside Zone A
#                 if class_names and class_names[cls_id].lower() == "head":
#                     if zone_A(x1, y1, x2, y2):
#                         head_in_zoneA = True

#         # ✅ if head detected inside Zone A → save frame & alert
#         if head_in_zoneA:
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
#             save_path = os.path.join(save_dir, f"frame_{timestamp}.jpg")
#             cv2.imwrite(save_path, frame)
#             print(f"[ALERT] Head detected in Zone A → frame saved: {save_path}")
#             send_email_alert(save_path)

#         # draw ROI zone
#         frame = draw_zone(frame)

#         # show FPS
#         curr_time = time.time()
#         fps = 0.9 * fps + 0.1 * (1.0 / (curr_time - prev_time)) if prev_time != 0 else 0
#         prev_time = curr_time
#         cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

#         if args.show:
#             cv2.imshow('YOLO Live with Zone A', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == '__main__':
#     main()
