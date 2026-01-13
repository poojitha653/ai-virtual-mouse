import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math

# ------------- Setup -------------
pyautogui.FAILSAFE = False
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
face = mp_face.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

frameR = 100
smoothening = 7
prev_x, prev_y = 0, 0

blink_thresh = 4.5
blink_cooldown = 0
right_click_cooldown = 0

def dist(p1, p2):
    return math.dist(p1, p2)

# ------------- Main Loop -------------
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(imgRGB)
    face_results = face.process(imgRGB)

    # ---------------- HAND TRACKING ----------------
    if hand_results.multi_hand_landmarks:
        for hand in hand_results.multi_hand_landmarks:
            # Draw hand skeleton
            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

            lm = [(int(l.x * w), int(l.y * h)) for l in hand.landmark]

            thumb = lm[4]
            index = lm[8]
            middle = lm[12]

            # Draw finger tips
            cv2.circle(img, index, 8, (0,255,0), cv2.FILLED)
            cv2.circle(img, middle, 8, (255,0,0), cv2.FILLED)
            cv2.circle(img, thumb, 8, (0,0,255), cv2.FILLED)

            # ---- Cursor Move ----
            x3 = np.interp(index[0], (frameR, w-frameR), (0, screen_w))
            y3 = np.interp(index[1], (frameR, h-frameR), (0, screen_h))

            curr_x = prev_x + (x3 - prev_x) / smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # ---- Scroll (index & middle together) ----
            if abs(index[1] - middle[1]) < 30:
                if index[1] < middle[1]:
                    pyautogui.scroll(40)
                else:
                    pyautogui.scroll(-40)

            # ---- Right Click (thumb + index pinch) ----
            if dist(index, thumb) < 30 and right_click_cooldown == 0:
                pyautogui.rightClick()
                right_click_cooldown = 20

            if right_click_cooldown > 0:
                right_click_cooldown -= 1

    # ---------------- EYE BLINK ----------------
    if face_results.multi_face_landmarks:
        faceLms = face_results.multi_face_landmarks[0].landmark

        # Left eye landmarks
        top = (int(faceLms[159].x * w), int(faceLms[159].y * h))
        bottom = (int(faceLms[145].x * w), int(faceLms[145].y * h))

        # Draw eye points
        cv2.circle(img, top, 5, (0,255,0), cv2.FILLED)
        cv2.circle(img, bottom, 5, (0,255,0), cv2.FILLED)
        cv2.line(img, top, bottom, (0,255,0), 2)

        # Blink = Left Click
        if dist(top, bottom) < blink_thresh and blink_cooldown == 0:
            pyautogui.click()
            blink_cooldown = 15

        if blink_cooldown > 0:
            blink_cooldown -= 1

    cv2.imshow("AI Virtual Mouse", img)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
