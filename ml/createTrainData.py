import numpy as np
import cv2
import os

samples =  np.empty((0,875))
responses = []

print("Read directorys 0-9:")
for i,_,_ in os.walk('data'):
    if i != 'data':
        num = i.strip()[-1]
        print(num, end=' ')
        files = os.listdir(i)
        files.remove('.DS_Store')
        
        for file in files:
            roi = cv2.imread(i + '/' + file)
            gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            #blur = cv2.GaussianBlur(gray,(5,5),0)
            #thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
            roismall = cv2.resize(gray,(25,35))
            responses.append(int(num))
            sample = roismall.reshape((1,875))
            samples = np.append(samples,sample,0)

responses = np.array(responses,np.float32)
responses = responses.reshape((responses.size,1))

np.savetxt('generalsamples.data',samples)
np.savetxt('generalresponses.data',responses)

print ("\nmodel creation complete", "🍺")