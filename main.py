import cv2
import datetime

# === FONNI O'ZGARISHDAN AJRATISH FUNKSIYASI ===
def get_motion_mask(frame, bg_subtractor):
    mask = bg_subtractor.apply(frame)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    _, mask = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)
    return mask

# === KONTURLARNI TOPISH VA TEKSHIRISH FUNKSIYASI ===
def find_motion_contours(mask, min_area=1000):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    return valid_contours

# === ABYEKTNI BELGILASH FUNKSIYASI ===
def draw_motion_objects(frame, contours):
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Harakat!", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return frame

# === VIDEO YOZISH FUNKSIYASI ===
def start_video_writer(frame, filename="motion_output.avi"):
    height, width = frame.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(filename, fourcc, 20.0, (width, height))

# === ASOSIY DASTUR ===
def main():
    cap = cv2.VideoCapture(0)  # 0 - kamera raqami
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50)
    
    ret, frame = cap.read()
    video_writer = start_video_writer(frame)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Fon va harakatni ajratish
        mask = get_motion_mask(frame, bg_subtractor)
        
        # Konturlarni topish
        contours = find_motion_contours(mask)
        
        # Agar harakat bo‘lsa obyektni belgila
        frame_with_motion = draw_motion_objects(frame.copy(), contours)
        
        # Natijani ko‘rsatish
        cv2.imshow("Asl video", frame)
        cv2.imshow("Harakat maskasi", mask)
        cv2.imshow("Harakat aniqlangan video", frame_with_motion)
        
        # Harakat bo‘lsa yozish
        if contours:
            video_writer.write(frame_with_motion)
        
        key = cv2.waitKey(30)
        if key == 27:  # ESC bosilsa chiqadi
            break

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
