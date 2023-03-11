import numpy as np
import cv2
import imutils
import time
import requests
from datetime import datetime

LINE_ACCESS_TOKEN = "LINE_ACCESS_TOKEN"
url = "https://notify-api.line.me/api/notify"

location = "location"
location_gps = "location_gps"

now = datetime.today()
message = f'{now.strftime("%d/%m/%Y")}   \n' \
        f'ตรวจพบปืน ที่ {location} เวลา {now.strftime("%I:%M:%S %p")} \n' \
        f'{location_gps} \n' \

def lineNotify(message,filepath):
    file = {'imageFile': open(filepath, 'rb')}
    data = {f'message': {message}}
    headers = {'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN}

    session = requests.Session()
    response = session.post(url, headers=headers, data=data, files=file)

gun_cascade = cv2.CascadeClassifier('cascade.xml')
image = cv2.imread("gun2.jpg")

while True:
    
    frame = image.copy()

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))

    for (x, y, w, h) in gun:

        frame = cv2.rectangle(frame,(x, y),(x + w, y + h),(255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    if len(gun) > 0:
        print(message)
        cv2.imwrite('output.jpg', frame)
        filepath = 'output.jpg'
        lineNotify(message,filepath)
        time.sleep(5)

cv2.destroyAllWindows()
