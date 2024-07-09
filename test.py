import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe pose class
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Initialize exercise counters
bicep_curl_counter = 0
squat_counter = 0
shoulder_press_counter = 0

# Initialize exercise stages
bicep_curl_stage = None
squat_stage = None
shoulder_press_stage = None

# Initialize camera capture
cap = cv2.VideoCapture(0)

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Bicep Curl and Shoulder Press
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            
            bicep_curl_angle = calculate_angle(shoulder, elbow, wrist)
            shoulder_angle = calculate_angle(elbow, shoulder, hip)
            
            cv2.putText(image, str(bicep_curl_angle), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            if shoulder_angle > 60:  # Condition to differentiate shoulder press from bicep curl
                # Shoulder Press Logic
                if bicep_curl_angle > 160:
                    shoulder_press_stage = "down"
                if bicep_curl_angle < 30 and shoulder_press_stage == 'down':
                    shoulder_press_stage = "up"
                    shoulder_press_counter += 1
                    print("Shoulder Press:", shoulder_press_counter)
                cv2.putText(image, 'Shoulder Press', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            else:
                # Bicep Curl Logic
                if bicep_curl_angle > 160:
                    bicep_curl_stage = "down"
                if bicep_curl_angle < 30 and bicep_curl_stage == 'down':
                    bicep_curl_stage = "up"
                    bicep_curl_counter += 1
                    print("Bicep Curl:", bicep_curl_counter)
                cv2.putText(image, 'Bicep Curl', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Squat
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            squat_angle = calculate_angle(hip, knee, ankle)
            cv2.putText(image, str(squat_angle), 
                           tuple(np.multiply(knee, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            if squat_angle > 160:
                squat_stage = "up"
            if squat_angle < 90 and squat_stage == 'up':  # 90 is chosen to be more lenient
                squat_stage = "down"
                squat_counter += 1
                print("Squat:", squat_counter)
            
        except:
            pass
       
        # Render exercise counters
        # Setup status box
        cv2.rectangle(image, (0, 0), (225, 225), (245, 117, 16), -1)

        # Bicep Curl data
        cv2.putText(image, 'BICEP CURL REPS', (15, 12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(bicep_curl_counter), 
                    (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'STAGE', (110, 12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, bicep_curl_stage if bicep_curl_stage else "None", 
                    (110, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Squat data
        cv2.putText(image, 'SQUAT REPS', (15, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(squat_counter), 
                    (10, 138), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'STAGE', (110, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, squat_stage if squat_stage else "None", 
                    (110, 138), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Shoulder Press data
        cv2.putText(image, 'SHOULDER PRESS REPS', (15, 168), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(shoulder_press_counter), 
                    (10, 216), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'STAGE', (110, 168), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, shoulder_press_stage if shoulder_press_stage else "None", 
                    (110, 216), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))               
                
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
