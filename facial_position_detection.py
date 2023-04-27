import urllib.request
import cv2
import numpy as np
from PIL import Image
import mediapipe as mp
import os
import face_recognition
import mediapipe as mp
import random
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils 
def getFrames(path):
    cap = cv2.VideoCapture(path)
    frames=[]
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames
def MediapipeProccess(frames):
    average_output_points=[]
    for frame in frames:
        averageX=0
        averageY=0
        pointcount=0
        with mp_face_mesh.FaceMesh( static_image_mode=True, max_num_faces=2, min_detection_confidence=0.5) as face_mesh:
            results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            annotated_image = frame.copy()
            
            if not results.multi_face_landmarks:
                continue
            for face_landmarks in results.multi_face_landmarks:
                for points in face_landmarks.landmark:
                    averageX+=points.x
                    averageY+=points.y
                    pointcount+=1
        average_output_points.append([averageX/pointcount ,averageY/pointcount])
    return average_output_points
def facerecog(basepath,frames):
    workcount=0
    known_image = face_recognition.load_image_file(basepath)
    known_image_Embed = face_recognition.face_encodings(known_image)[0]
    for frame in frames:
        try:
            unknown_encoding = face_recognition.face_encodings(frame)[0]
            result = face_recognition.compare_faces([known_image_Embed], unknown_encoding)[0]
        except:
            pass
        if result:
            workcount=+1
    if workcount/len(frames)>0.6:
        return True 
    return False
def run(path , pointlist , ):
    videoframes=getFrames(path)
    allPointsAverage=MediapipeProccess(videoframes)
    checklistArray=[]
    for  i in pointlist:
        checklistArray.append(i)
    for point in allPointsAverage:
        xmin,ymin,xmax,ymax=checklistArray[0]
        if point[0]>xmin and point[0]<xmax and point[1]>ymin and point[1]<ymax:
            if len(checklistArray)==1:
                checklistArray=[]
                break
            checklistArray=checklistArray[1:]
    randomFrames=random.sample(videoframes, 10)
    if len(checklistArray)==0 and facerecog('testimage.jpg',videoframes):
        return 1
    return 0


print(run('output.mov',[[0.3,0.2,0.4,0.7],[0.4,0.2,0.5,0.95]]))