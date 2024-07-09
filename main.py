# main.py

import cv2
import mediapipe as mp
import numpy as np
from Lib.module import calculate_angle
from Lib.visual import draw_landmarks, draw_text, draw_counters

# Initialize MediaPipe pose class
mp_pose = mp.solutions.pose

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
            
            draw_text(image, str(bicep_curl_angle), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                           font_scale=0.5, color=(255, 255, 255), thickness=2)
            
            if shoulder_angle > 60:  # Condition to differentiate shoulder press from bicep curl
                # Shoulder Press Logic
                if bicep_curl_angle > 160:
                    shoulder_press_stage = "down"
                if bicep_curl_angle < 30 and shoulder_press_stage == 'down':
                    shoulder_press_stage = "up"
                    shoulder_press_counter += 1
                    print("Shoulder Press:", shoulder_press_counter)
            else:
                # Bicep Curl Logic
                if bicep_curl_angle > 160:
                    bicep_curl_stage = "down"
                if bicep_curl_angle < 30 and bicep_curl_stage == 'down':
                    bicep_curl_stage = "up"
                    bicep_curl_counter += 1
                    print("Bicep Curl:", bicep_curl_counter)
            
            # Squat
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            squat_angle = calculate_angle(hip, knee, ankle)
            draw_text(image, str(squat_angle), 
                           tuple(np.multiply(knee, [640, 480]).astype(int)), 
                           font_scale=0.5, color=(255, 255, 255), thickness=2)
            if squat_angle > 160:
                squat_stage = "up"
            if squat_angle < 90 and squat_stage == 'up':
                squat_stage = "down"
                squat_counter += 1
                print("Squat:", squat_counter)

            # Draw landmarks and counters
            draw_landmarks(image, results)
            draw_counters(image, bicep_curl_counter, squat_counter, shoulder_press_counter, 
                          bicep_curl_stage, squat_stage, shoulder_press_stage)
            
        except:
            pass

        # Display the image
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
