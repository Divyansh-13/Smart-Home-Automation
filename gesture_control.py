import cv2
import mediapipe as mp
import requests

ESP_IP = "http://"IP CODE GIVEN BY ARDUINO""


mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)

cap = cv2.VideoCapture(0)

last_command = ""
bulb1 = False  # Track bulb states for display
bulb2 = False

# Sending command to ESP
def send(cmd):
    global last_command, bulb1, bulb2
    if cmd != last_command:
        try:
            requests.get(ESP_IP + cmd, timeout=1)
            print("Sent:", cmd)
            last_command = cmd
            # Update local state
            if   cmd == "/r1/on":  bulb1 = True
            elif cmd == "/r1/off": bulb1 = False
            elif cmd == "/r2/on":  bulb2 = True
            elif cmd == "/r2/off": bulb2 = False
            elif cmd == "/all/on":  bulb1 = bulb2 = True
            elif cmd == "/all/off": bulb1 = bulb2 = False
        except:
            print("Error - Check ESP IP:", ESP_IP)

# Count raised fingers
def count_fingers(lm):
    tips  = [8, 12, 16, 20]   # Index, Middle, Ring, Pinky tip IDs
    bases = [6, 10, 14, 18]   # Corresponding base IDs
    count = 0
    for tip, base in zip(tips, bases):
        if lm[tip].y < lm[base].y:   # tip higher than base = finger up
            count += 1
    # Thumb (compare x instead of y)
    if lm[4].x < lm[3].x:
        count += 1
    return count

# Gesture → Command mapping
#   0 fingers (FIST)   → ALL OFF
#   1 finger  (INDEX)  → Bulb 1 ON
#   2 fingers          → Bulb 2 ON
#   3 fingers          → Both ON (ALL ON)
#   5 fingers (OPEN)   → ALL ON
#
def get_command(finger_count):
    if   finger_count == 0: return "/all/off"
    elif finger_count == 1: return "/r1/on"
    elif finger_count == 2: return "/r2/on"
    elif finger_count == 3: return "/all/on"
    elif finger_count == 5: return "/all/on"
    return None

# UI helpers ────────────────────────────────────────────
def draw_ui(frame, gesture_name, finger_count, b1, b2):
    h, w, _ = frame.shape

    # Semi-transparent top bar
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 70), (15, 15, 30), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    # Title
    cv2.putText(frame, "Hand Gesture Bulb Control",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (245, 166, 35), 2)

    # Finger count
    cv2.putText(frame, f"Fingers: {finger_count}",
                (10, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

    # Gesture name
    cv2.putText(frame, gesture_name,
                (w - 280, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (100, 220, 100), 2)

    # Bottom status panel
    overlay2 = frame.copy()
    cv2.rectangle(overlay2, (0, h - 80), (w, h), (15, 15, 30), -1)
    cv2.addWeighted(overlay2, 0.7, frame, 0.3, 0, frame)

    # Bulb 1 status
    b1_color = (0, 255, 100) if b1 else (80, 80, 80)
    b1_icon  = "BULB 1: ON " if b1 else "BULB 1: OFF"
    cv2.circle(frame, (30, h - 45), 12, b1_color, -1)
    cv2.putText(frame, b1_icon, (50, h - 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, b1_color, 2)

    # Bulb 2 status
    b2_color = (0, 255, 100) if b2 else (80, 80, 80)
    b2_icon  = "BULB 2: ON " if b2 else "BULB 2: OFF"
    cv2.circle(frame, (w // 2 + 10, h - 45), 12, b2_color, -1)
    cv2.putText(frame, b2_icon, (w // 2 + 30, h - 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, b2_color, 2)

    # ESC hint
    cv2.putText(frame, "ESC to quit", (10, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 100, 100), 1)

# Gesture label for display ─────────────────────────────
def gesture_label(n):
    labels = {
        0: "FIST  → ALL OFF",
        1: "1 Finger → Bulb 1 ON",
        2: "2 Fingers → Bulb 2 ON",
        3: "3 Fingers → ALL ON",
        4: "4 Fingers → (none)",
        5: "OPEN HAND → ALL ON",
    }
    return labels.get(n, "")

# Main loop ─────────────────────────────────────────────
print("=" * 40)
print("  Gesture Control Started")
print(f"  ESP IP: {ESP_IP}")
print("=" * 40)
print("  FIST      (0) → ALL OFF")
print("  1 finger  (1) → Bulb 1 ON")
print("  2 fingers (2) → Bulb 2 ON")
print("  3 fingers (3) → ALL ON")
print("  Open hand (5) → ALL ON")
print("  ESC            → Quit")
print("=" * 40)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)   # Mirror for natural feel
    rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_count = -1
    gesture_name = "No hand detected"

    if result.multi_hand_landmarks:
        for hand_lm in result.multi_hand_landmarks:
            # Draw hand skeleton
            mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(245,166,35), thickness=2, circle_radius=3),
                mp_draw.DrawingSpec(color=(200,200,200), thickness=2))

            lm = hand_lm.landmark
            finger_count = count_fingers(lm)
            gesture_name = gesture_label(finger_count)

            cmd = get_command(finger_count)
            if cmd:
                send(cmd)

    draw_ui(frame, gesture_name, finger_count if finger_count >= 0 else 0, bulb1, bulb2)

    cv2.imshow("Gesture Control - ESP8266 Bulbs", frame)
    if cv2.waitKey(1) & 0xFF == 27:   # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
print("Stopped.")
