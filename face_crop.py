'''
python face_crop.py in.png out{}.png 0

mkdir -p out
for f in /pics/*.jpg; do
  filename=$(basename "$f")
  name="${filename%.*}"
  ext="${filename##*.}"
  echo "$filename..."
  python face_crop.py "$f" "out/$name.{}.$ext" .3
done
'''

import os
import sys
import cv2

# args
file_in = sys.argv[1]
file_out_pattern = sys.argv[2] # e.g. 'out{}.png'
margin = float(sys.argv[3]) # e.g. .3

# load image
img = cv2.imread(file_in)

# find the faces (try with a different scaleFactor if nothing is found)
classifier = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml')
for scaleFactor in (1.1, 1.01):
  faces = classifier.detectMultiScale(img, scaleFactor, 3)
  if len(faces) > 0: break
if len(faces) == 0:
  print("WARNING: No results")

# save them all
for i in range(len(faces)):
  (x,y,w,h) = faces[i]
  # typical results crop the face, but I want hair and neck to show
  H = img.shape[0]
  W = img.shape[1]
  x -= int(w * margin)
  y -= int(h * margin)
  w += 2 * int(w * margin)
  h += 2 * int(h * margin)
  if x < 0: w += x; x = 0
  if y < 0: h += y; y = 0
  if x + w > W: w -= (x + w) - W
  if y + h > H: h -= (y + h) - H
  # save
  cv2.imwrite(file_out_pattern.format(i), img[y:y+h, x:x+w])
