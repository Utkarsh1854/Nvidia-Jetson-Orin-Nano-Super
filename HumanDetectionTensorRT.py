import cv2
import time
from ultralytics import YOLO

def get_gst_str():
    """
    Enhanced GStreamer string for IMX477.
    - flicker-mode=2: Indoor 50Hz stabilization.
    - ispdigitalgainrange: Limits digital noise during motion.
    - exposuretimerange: Prevents the shutter from 'hunting' during movement.
    """
    return (
        "nvarguscamerasrc sensor-id=0 flicker-mode=2 "
        "ispdigitalgainrange='1 8' "
        "exposuretimerange='13000 683709000' ! "
        "video/x-raw(memory:NVMM), width=3840, height=2160, framerate=30/1, format=NV12 ! "
        "nvvidconv ! "
        "video/x-raw, width=1920, height=1080, format=BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=BGR ! "
        "appsink drop=True"
    )

def main():
    print("Loading TensorRT Engine...")
    try:
        model = YOLO("yolov8n.engine", task='detect')
    except:
        model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(get_gst_str(), cv2.CAP_GSTREAMER)
    
    if not cap.isOpened():
        print("Camera Failed. Restarting daemon...")
        return

    # Warmup
    model.predict(source=None, imgsz=(480, 640), device=0, verbose=False)
    prev_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # INFERENCE
        results = model.predict(
            source=frame, 
            classes=[0], 
            conf=0.45, 
            device=0, 
            imgsz=(480, 640), 
            stream=True, 
            verbose=False
        )

        # MANUAL DRAWING (Higher Performance than r.plot())
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                
                # Draw Box
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                # Label
                cv2.putText(frame, f"Person {conf:.2f}", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Count Display
            cv2.putText(frame, f"Humans: {len(boxes)}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        # FPS Calculation
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (50, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("IMX477 Optimized Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
