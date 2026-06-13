# import argparse
# import time
# import sys
# import os
# from datetime import datetime

# import cv2
# from ultralytics import YOLO


# def parse_args():
#     p = argparse.ArgumentParser(description='Live YOLO on webcam')
#     p.add_argument('--model', type=str, default='V1_head.1_ICF_RYK_V1_best.pt', help='path to YOLO model (.pt)')
#     p.add_argument('--source', type=str, default='0', help='webcam index or video file')
#     p.add_argument('--conf', type=float, default=0.40, help='confidence threshold')
#     p.add_argument('--show', type=lambda s: s.lower() not in ['false','0'], default=True, help='show window')
#     return p.parse_args()


# def main():
#     args = parse_args()

#     # Create output folder if not exists
#     save_dir = "New Alert"
#     os.makedirs(save_dir, exist_ok=True)

#     # choose device automatically
#     try:
#         import torch
#         device = 0 if torch.cuda.is_available() else 'cpu'
#     except Exception:
#         device = 'cpu'

#     print(f"Loading model {args.model} on device {device} ...")
#     model = YOLO(args.model)

#     # get class names
#     try:
#         class_names = model.names
#     except Exception:
#         class_names = None

#     # open video source
#     src = int(args.source) if args.source.isdigit() else args.source
#     cap = cv2.VideoCapture(src)
#     if not cap.isOpened():
#         print('ERROR: Could not open video source:', src)
#         sys.exit(1)

#     prev_time = 0
#     fps = 30
#     print('Press q to quit')

#     frame_count = 0

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print('Stream ended or cannot fetch frame')
#             break

#         results = model(frame, device=device, conf=args.conf, verbose=False)
#         r = results[0]
#         boxes = getattr(r, 'boxes', None)

#         head_detected = False  # flag

#         if boxes is not None and len(boxes) > 0:
#             for box in boxes:
#                 xyxy = box.xyxy[0].tolist()
#                 conf = float(box.conf[0]) if hasattr(box, 'conf') else 0.0
#                 cls_id = int(box.cls[0]) if hasattr(box, 'cls') else None

#                 x1, y1, x2, y2 = map(int, xyxy)
#                 label = f"id:{cls_id} {conf:.2f}"
#                 if class_names and cls_id in class_names:
#                     label = f"{class_names[cls_id]} {conf:.2f}"

#                 # check if class name == 'head'
#                 if class_names and class_names[cls_id].lower() == "head":
#                     head_detected = True

#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
#                 cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), (0, 255, 0), -1)
#                 cv2.putText(frame, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

#         # ✅ Save frame if head detected
#         if head_detected:
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
#             save_path = os.path.join(save_dir, f"frame_{timestamp}.jpg")
#             cv2.imwrite(save_path, frame)
#             print(f"[ALERT] Head detected → frame saved: {save_path}")

#         # FPS calculation
#         curr_time = time.time()
#         fps = 0.9 * fps + 0.1 * (1.0 / (curr_time - prev_time)) if prev_time != 0 else 0
#         prev_time = curr_time
#         cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

#         if args.show:
#             cv2.imshow('YOLO Live', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == '__main__':
#     main()




###################################################### This is whatsapp sending code #######################################################


# import argparse
# import time
# import sys
# import os
# from datetime import datetime

# import cv2
# from ultralytics import YOLO
# from twilio.rest import Client  # 👈 Twilio import added


# def parse_args():
#     p = argparse.ArgumentParser(description='Live YOLO on webcam')
#     p.add_argument('--model', type=str, default='V1_head.1_ICF_RYK_V1_best.pt', help='path to YOLO model (.pt)')
#     p.add_argument('--source', type=str, default='0', help='webcam index or video file')
#     p.add_argument('--conf', type=float, default=0.40, help='confidence threshold')
#     p.add_argument('--show', type=lambda s: s.lower() not in ['false', '0'], default=True, help='show window')
#     return p.parse_args()


# def send_whatsapp_alert(message_text):
#     """Send WhatsApp message using Twilio API"""
#     # 👇 replace these credentials with your Twilio details
#     account_sid = "SKc575832e9adf54cf3944e2b0578eaccd"
#     auth_token = "bf6bbdeef47ce0fa8530f351df3eca95"
#     from_whatsapp = "whatsapp:+12294083173"   # Twilio sandbox number
#     to_whatsapp = "whatsapp:+923048344944"    # your number (with country code)

#     try:
#         client = Client(account_sid, auth_token)
#         message = client.messages.create(
#             body=message_text,
#             from_=from_whatsapp,
#             to=to_whatsapp
#         )
#         print(f"✅ WhatsApp alert sent! Message SID: {message.sid}")
#     except Exception as e:
#         print("❌ WhatsApp alert failed:", e)


# def main():
#     args = parse_args()

#     # Create folder for alert frames
#     save_dir = "New Alert"
#     os.makedirs(save_dir, exist_ok=True)

#     # Choose device automatically
#     try:
#         import torch
#         device = 0 if torch.cuda.is_available() else 'cpu'
#     except Exception:
#         device = 'cpu'

#     print(f"Loading model {args.model} on device {device} ...")
#     model = YOLO(args.model)

#     # Get class names
#     try:
#         class_names = model.names
#     except Exception:
#         class_names = None

#     # Open camera/video
#     src = int(args.source) if args.source.isdigit() else args.source
#     cap = cv2.VideoCapture(src)
#     if not cap.isOpened():
#         print('ERROR: Could not open video source:', src)
#         sys.exit(1)

#     prev_time = 0
#     fps = 0
#     print('Press q to quit')

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print('Stream ended or cannot fetch frame')
#             break

#         results = model(frame, device=device, conf=args.conf, verbose=False)
#         r = results[0]
#         boxes = getattr(r, 'boxes', None)

#         head_detected = False

#         if boxes is not None and len(boxes) > 0:
#             for box in boxes:
#                 xyxy = box.xyxy[0].tolist()
#                 conf = float(box.conf[0]) if hasattr(box, 'conf') else 0.0
#                 cls_id = int(box.cls[0]) if hasattr(box, 'cls') else None
#                 x1, y1, x2, y2 = map(int, xyxy)

#                 if class_names and cls_id in class_names:
#                     label = f"{class_names[cls_id]} {conf:.2f}"
#                 else:
#                     label = f"id:{cls_id} {conf:.2f}"

#                 # Check if detected object is "head"
#                 if class_names and class_names[cls_id].lower() == "head":
#                     head_detected = True

#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
#                 cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), (0, 255, 0), -1)
#                 cv2.putText(frame, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

#         # ✅ If head detected, save frame and send WhatsApp alert
#         if head_detected:
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
#             save_path = os.path.join(save_dir, f"frame_{timestamp}.jpg")
#             cv2.imwrite(save_path, frame)
#             print(f"[ALERT] Head detected → frame saved: {save_path}")

#             # Send WhatsApp alert
#             send_whatsapp_alert(f"🚨 Head detected on camera!\nSaved frame: {save_path}")

#         # FPS calculation
#         curr_time = time.time()
#         fps = 0.9 * fps + 0.1 * (1.0 / (curr_time - prev_time)) if prev_time != 0 else 0
#         prev_time = curr_time
#         cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

#         if args.show:
#             cv2.imshow('YOLO Live', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == '__main__':
#     main()



############################### Gamil Alert Code #########################################################

import argparse
import time
import sys
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage
try:
    from dotenv import load_dotenv  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]
except Exception:
    # Fallback if python-dotenv isn't installed; keeps runtime working without env loading
    def load_dotenv():
        return False

import cv2
from ultralytics import YOLO

# 🔹 Load environment variables
load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")


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


def parse_args():
    p = argparse.ArgumentParser(description='Live YOLO on webcam')
    p.add_argument('--model', type=str, default='V1_head.1_ICF_RYK_V1_best.pt', help='path to YOLO model (.pt)')
    p.add_argument('--source', type=str, default='0', help='webcam index or video file')
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


if __name__ == '__main__':
    main()







