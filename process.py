import calendar
import os
import subprocess
import time
import cv2
import numpy as np

EXTENSION_OUT = ".jpg"


def match_image_invoice(file, cap):
    # converting to jpg
    img = cv2.imdecode(np.fromstring(
        file, np.uint8), cv2.IMREAD_UNCHANGED)

    img2 = cv2.imdecode(np.asarray(bytearray(cap.read()),
                        dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    img = crop_img(img, 0.80)
    img2 = crop_img(img2, 0.80)

    img = resize_image(img,(512,512))
    img2 = resize_image(img2,(512,512))

    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    error, diff = mse(img1, img2)
    print("Image matching Error between the two images:", error)
    if (error < 3):
        return extract_text_from_image(detecte_specific_value(img, img2))


# define the function to compute MSE between two images
def mse(img1, img2):
    try:
        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err/(float(h*w))
        return mse, diff
    except Exception as e:
        return 100, None


def extract_text_from_image(img1):
    out_content = subprocess.run(
        ['tesseract', img1, '-', '-l', 'eng'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    removeImgTemp(img1)
    print(out_content)
    if out_content != "":
        return out_content
    return None


def detecte_specific_value(img1, img2):
    _, threshold = cv2.threshold(img2, 110, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    maxCountours = []
    for cnt in contours:
        if i == 0:
            i = 1
            continue
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            if aspectRatio > 1.05:
                # draws boundary of contours.
                cv2.drawContours(img1, [approx], 0, (0, 0, 255), 2)
                maxCountours.append(cnt)
    # Get contour with maximum area
    c = max(maxCountours, key=cv2.contourArea)
    x1, y1, w1, h1 = cv2.boundingRect(c)
    crop = img1[y1:y1+h1, x1:x1+w1, :].copy()
    temp_img_cropped = generateNameTemp()
    cv2.imwrite(temp_img_cropped, crop)
    return temp_img_cropped


def crop_img(img, scale=1.0):
    _, center_y = img.shape[1] / 2, img.shape[0] / 2
    _, height_scaled = img.shape[1] * scale, img.shape[0] * scale
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
    img_cropped = img[int(top_y):int(bottom_y), :]
    return img_cropped


def removeImgTemp(img):
    try:
        os.remove(img)
    except:
        pass


def generateNameTemp():
    current_GMT = time.gmtime()
    return str(calendar.timegm(current_GMT)) + EXTENSION_OUT

def resize_image(img, size=(28,28)):
    h, w = img.shape[:2]
    c = img.shape[2] if len(img.shape)>2 else 1
    if h == w: 
        return cv2.resize(img, size, cv2.INTER_AREA)
    dif = h if h > w else w
    interpolation = cv2.INTER_AREA if dif > (size[0]+size[1])//2 else cv2.INTER_CUBIC
    x_pos = (dif - w)//2
    y_pos = (dif - h)//2
    if len(img.shape) == 2:
        mask = np.zeros((dif, dif), dtype=img.dtype)
        mask[y_pos:y_pos+h, x_pos:x_pos+w] = img[:h, :w]
    else:
        mask = np.zeros((dif, dif, c), dtype=img.dtype)
        mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = img[:h, :w, :]
    return cv2.resize(mask, size, interpolation)