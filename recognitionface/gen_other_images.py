import cv2  
import os  
import sys  
   
IMAGE_DIR = './image'  
   
OUTPUT_DIR = './other_people'  
if not os.path.exists(OUTPUT_DIR):  
    os.makedirs(OUTPUT_DIR)  
   
# http://blog.topspeedsnail.com/archives/10511  
# wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml  
face_haar = cv2.CascadeClassifier("/home/cps/haarcascade_frontalface_default.xml")  
   
for (dirpath, dirnames, filenames) in os.walk(IMAGE_DIR):  
    for filename in filenames:  
     try:   
        if filename.endswith('.jpg'):  
            image_path = os.path.join(dirpath, filename)  
            print('process: ', image_path)  
            img = cv2.imread(image_path)  
              
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
            faces = face_haar.detectMultiScale(gray_image, 1.3, 5)  
     except Exception as err:
            print(err);
            print("error..")
            continue
            for face_x,face_y,face_w,face_h in faces:  
                face = img[face_y:face_y+face_h, face_x:face_x+face_w]  
   
                face = cv2.resize(face, (64, 64))  
   
                cv2.imshow("img", face)  
                cv2.imwrite(os.path.join(OUTPUT_DIR, filename), face)  

            key = cv2.waitKey(30) & 0xff  
            if key == 27:  
                sys.exit(0)  