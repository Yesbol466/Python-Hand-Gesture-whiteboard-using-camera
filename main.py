import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

canvas = np.zeros((480, 640, 3), dtype=np.uint8)

cap = cv2.VideoCapture(0)

prev_tip = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            finger_tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP]
            tip_positions = []
            for tip in finger_tips:
                tip_positions.append((int(hand_landmarks.landmark[tip].x * frame.shape[1]),
                                      int(hand_landmarks.landmark[tip].y * frame.shape[0])))

           
            fingers_up = [lm.y < hand_landmarks.landmark[id - 2].y for id, lm in enumerate(hand_landmarks.landmark) if id in [8, 12, 16]]  # Index, Middle, Ring

            if fingers_up.count(True) == 1:  # Drawing
                if prev_tip:
                    cv2.line(canvas, prev_tip, tip_positions[0], (0, 255, 255), 5)
                prev_tip = tip_positions[0]
            elif fingers_up.count(True) == 3:  # Erasing
                for tip in tip_positions:
                    cv2.circle(canvas, tip, 20, (0, 0, 0), -1)
                prev_tip = None
            else:
                prev_tip = None

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    frame = cv2.add(frame, canvas)

    cv2.imshow('Interactive Whiteboard', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break


cap.release()
cv2.destroyAllWindows()
