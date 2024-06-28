import cv2 as cv
import uuid
from PIL import Image
import pytesseract as tess
import numpy as np

def recoginse_text(cut_image_path):
    """
    步骤：
    1、灰度，二值化处理
    2、形态学操作去噪
    3、识别
    :param image:
    :return:
    """
    # cut_image_path = cutPic(image_path)

    image = cv.imread(cut_image_path)
    # 灰度 二值化
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 如果是白底黑字 建议 _INV
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

    # 形态学操作 (根据需要设置参数（1，2）)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 2))  # 去除横向细线
    morph1 = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 1))  # 去除纵向细线
    morph2 = cv.morphologyEx(morph1, cv.MORPH_OPEN, kernel)
    # cv.imshow("Morph", morph2)

    # 黑底白字取非，变为白底黑字（便于pytesseract 识别）
    cv.bitwise_not(morph2, morph2)
    # cv.imshow("Morph", morph2)
    textImage = Image.fromarray(morph2)

    text = tess.image_to_string(textImage, lang='eng')
    print("识别结果：%s" % text)
    return text.strip()


def recoginse_color(image_path):
    hsv_list = [
        {
            "color": "red",
            "low": [0, 43, 46],
            "high": [10, 255, 255]
        },
        {
            "color": "green",
            "low": [35, 43, 46],
            "high": [77, 255, 255]
        },
        {
            "color": "blue",
            "low": [100, 43, 46],
            "high": [124, 255, 255]
        }
    ]
    src = cv.imread(image_path)
    """
    提取图中的红色部分
    """
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    result = []
    for i in hsv_list:
        low_hsv = np.array(i['low'])
        high_hsv = np.array(i['high'])

        mask = cv.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
        # 形态学操作 (根据需要设置参数（1，2）)

        kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 2))  # 去除横向细线
        morph1 = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 1))  # 去除纵向细线
        morph2 = cv.morphologyEx(morph1, cv.MORPH_OPEN, kernel)
        # 查看亮的像素点
        count = cv.countNonZero(morph2)
        result.append(count)
    cv.destroyAllWindows()
    return result


def cutPic(image_path):
    # 读取需要识别的数字字母图片，并显示读到的原图
    (filepath, tempfilename) = os.path.split(image_path)
    (filename, extension) = os.path.splitext(tempfilename)
    img = cv.imread(image_path)
    text_cropped = img[15:70, 550:800]  # 裁剪坐标为[y0:y1, x0:x1]
    red_cropped = img[100:150, 600:700]  # 裁剪坐标为[y0:y1, x0:x1]
    green_cropped = img[230:280, 600:700]  # 裁剪坐标为[y0:y1, x0:x1]
    blue_cropped = img[350:400, 600:700]  # 裁剪坐标为[y0:y1, x0:x1]
    text_name = filename + '-APOLLO' + extension
    text_path = os.path.join(filepath, text_name)
    red_name = filename + '-red' + extension
    red_path = os.path.join(filepath, red_name)
    green_name = filename + '-green' + extension
    green_path = os.path.join(filepath, green_name)
    blue_name = filename + '-blue' + extension
    blue_path = os.path.join(filepath, blue_name)
    cv.imwrite(text_path, text_cropped)
    cv.imwrite(red_path, red_cropped)
    cv.imwrite(green_path, green_cropped)
    cv.imwrite(blue_path, blue_cropped)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return (text_path, red_path, green_path, blue_path)


def savePicture(sn, factory=''):
    uid = str(uuid.uuid4())
    picture_name = ''.join(uid.split('-')) + '.png'
    # picture_name = '01.bmp'
    # cap = cv2.VideoCapture(0)
    path = "D:\\CabbageTool\\picture\\" + sn + "\\"
    if not os.path.exists(path):
        os.makedirs(path)
    # picture_name = '9d9a8ad0bfbe498586a4fc13438c245b.png'
    file_path = os.path.join(os.path.dirname(path), picture_name)
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)  # 打开摄像头
    cap.set(3, 1280)  # 设置分辨率
    cap.set(4, 720)
    ret, frame = cap.read()
    cv.imwrite(file_path, frame)
    cap.release()
    cv.destroyAllWindows()

    text_image_path, red_image_path, green_image_path, blue_image_path = cutPic(file_path)
    text = recoginse_text(text_image_path)

    redimage = cv.imread(red_image_path, cv.IMREAD_COLOR)
    r = redimage[:, :, 2]

    greenimage = cv.imread(green_image_path, cv.IMREAD_COLOR)
    g = greenimage[:, :, 0]
    print(g)
    blueimage = cv.imread(blue_image_path, cv.IMREAD_COLOR)
    b = blueimage[:, :, 1]
    red = 'fail'
    green = 'fail'
    blue = 'fail'
    if text != 'APOLLO':
        text = 'fail'
    if np.max(r) == np.min(r):
        red = str(np.min(r))
    if np.max(g) == np.min(g):
        green = str(np.min(g))
    if np.max(b) == np.min(b):
        blue = str(np.min(g))
    s = text + '|' + red + '|' + green + '|' + blue
    if 'fail' in s:
        showIMG(file_path)
    return text + '|' + red + '|' + green + '|' + blue


def showIMG(file_path):
    import matplotlib.pyplot as plt
    img = Image.open(file_path)
    plt.figure(figsize=(4, 4))
    plt.ion()
    plt.axis('off')
    plt.imshow(img)
    mngr = plt.get_current_fig_manager()
    mngr.window.wm_geometry("+380+210")
    plt.pause(5)
    plt.ioff()
    plt.clf()
    plt.close('all')
