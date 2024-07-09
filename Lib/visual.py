import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils

def draw_landmarks(image, results):
    """
    Draw landmarks on the image.
    
    Args:
    image: The input image.
    results: The pose landmarks results.
    """
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2), 
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

def draw_text(image, text, position, font_scale=0.5, color=(255, 255, 255), thickness=2):
    """
    Draw text on the image.
    
    Args:
    image: The input image.
    text: The text to be drawn.
    position: Position to draw the text.
    font_scale: Font scale.
    color: Color of the text.
    thickness: Thickness of the text.
    """
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)

def draw_counters(image, bicep_curl_counter, squat_counter, shoulder_press_counter, 
                  bicep_curl_stage, squat_stage, shoulder_press_stage):
    """
    Draw exercise counters and stages on the image.
    
    Args:
    image: The input image.
    bicep_curl_counter, squat_counter, shoulder_press_counter: Counters for each exercise.
    bicep_curl_stage, squat_stage, shoulder_press_stage: Stages for each exercise.
    """
    # Setup status box
    cv2.rectangle(image, (0, 0), (225, 225), (245, 117, 16), -1)

    # Bicep Curl data
    draw_text(image, 'BICEP CURL REPS', (15, 12), 0.5, (0, 0, 0), 1)
    draw_text(image, str(bicep_curl_counter), (10, 60), 2, (255, 255, 255), 2)
    draw_text(image, 'STAGE', (110, 12), 0.5, (0, 0, 0), 1)
    draw_text(image, bicep_curl_stage if bicep_curl_stage else "None", (110, 60), 2, (255, 255, 255), 2)

    # Squat data
    draw_text(image, 'SQUAT REPS', (15, 90), 0.5, (0, 0, 0), 1)
    draw_text(image, str(squat_counter), (10, 138), 2, (255, 255, 255), 2)
    draw_text(image, 'STAGE', (110, 90), 0.5, (0, 0, 0), 1)
    draw_text(image, squat_stage if squat_stage else "None", (110, 138), 2, (255, 255, 255), 2)

    # Shoulder Press data
    draw_text(image, 'SHOULDER PRESS REPS', (15, 168), 0.5, (0, 0, 0), 1)
    draw_text(image, str(shoulder_press_counter), (10, 216), 2, (255, 255, 255), 2)
    draw_text(image, 'STAGE', (110, 168), 0.5, (0, 0, 0), 1)
    draw_text(image, shoulder_press_stage if shoulder_press_stage else "None", (110, 216), 2, (255, 255, 255), 2)
