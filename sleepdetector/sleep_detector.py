import cv2
import time
import winsound

# Try playing the sound once to make sure it loads
try:
    winsound.PlaySound('alarm.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
    winsound.PlaySound(None, winsound.SND_PURGE) # Stop it immediately
    alarm_sound_loaded = True
except Exception as e:
    print(f"Error loading alarm sound: {e}")
    alarm_sound_loaded = False

# Load OpenCV cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

# Thresholds
SLEEP_TIME_THRESHOLD = 10.0 # Number of seconds eyes are not detected to sound alarm

eyes_closed_start_time = None
alarm_on = False

# Open Webcam
cap = cv2.VideoCapture(0)

print("Starting Sleep Detector... Press 'q' to quit.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    eyes_detected = False
    
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
        
        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
        for (ex,ey,ew,eh) in eyes:
            eyes_detected = True
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
    if not eyes_detected:
        # No eyes found (eyes closed or looking away)
        if eyes_closed_start_time is None:
            eyes_closed_start_time = time.time()
            
        closed_duration = time.time() - eyes_closed_start_time
        
        cv2.putText(image, f"EYES CLOSED: {closed_duration:.1f}s", (30, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Check if eyes have been closed for a sufficient amount of time
        if closed_duration >= SLEEP_TIME_THRESHOLD:
            if not alarm_on and alarm_sound_loaded:
                winsound.PlaySound('alarm.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
                alarm_on = True
            
            cv2.putText(image, "WAKE UP!!!", (200, 250), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    else:
        # Eyes are detected
        eyes_closed_start_time = None
        cv2.putText(image, "EYES OPEN", (30, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        if alarm_on and alarm_sound_loaded:
            winsound.PlaySound(None, winsound.SND_PURGE) # Stop the sound
            alarm_on = False
    
    cv2.imshow('Sleep Detector', image)
    
    # Exit on pressing 'q'
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if alarm_sound_loaded:
    winsound.PlaySound(None, winsound.SND_PURGE)
