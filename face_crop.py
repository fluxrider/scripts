'''
mkdir -p out
for f in /pics/*.jpg; do
  filename=$(basename "$f")
  name="${filename%.*}"
  ext="${filename##*.}"
  echo "$filename..."
  python face_crop.py "$f" "out/$name.{}.$ext"
done
'''

import os
import sys
import cv2

# args
file_in = sys.argv[1]
file_out_pattern = sys.argv[2] # e.g. 'out{}.png'

# load image
img = cv2.imread(file_in)

# find the faces
classifier = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml')
faces = classifier.detectMultiScale(img)

# save them all
for i in range(len(faces)):
  (x,y,w,h) = faces[i]
  cv2.imwrite(file_out_pattern.format(i), img[y:y+h, x:x+w])
