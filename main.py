import cv2
import mediapipe as mp
import random

# 1. ตั้งค่าตัวตรวจจับมือ
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# 2. เปิดกล้อง
cap = cv2.VideoCapture(0)

print("คาถาแยกเงาพันร่าง... เริ่มทำงาน! (กด 'q' เพื่อเลิกรา)")

while cap.isOpened():
    success, img = cap.read()
    if not success: break

    img = cv2.flip(img, 1) # กลับด้านซ้ายขวาให้เหมือนกระจก
    h, w, c = img.shape
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            # วาดเส้นโครงกระดูกมือ
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            
            # ตรรกะ: ถ้าตรวจพบมือ ให้สร้างวงกลม (ร่างแยกจำลอง) กระจายออกมา
            for i in range(5): 
                cv2.circle(img, (random.randint(0, w), random.randint(0, h)), 20, (255, 255, 255), -1)
                cv2.putText(img, "CLONE", (random.randint(0, w), random.randint(0, h)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Shadow Clone Jutsu", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
