import cv2

vidcap = cv2.VideoCapture('/home/obayashi/data/first_video/test/00002_1.mp4')

count = 0

while(vidcap.isOpened()):
    count_zero = str(count).zfill(5)
    ret, image = vidcap.read()
    # 이미지 사이즈 960x540으로 변경
    #image = cv2.resize(image, (960, 540))

    # 30프레임당 하나씩 이미지 추출
    if(int(vidcap.get(1)) % 30 == 0):
        print('Saved frame number : ' + str(int(vidcap.get(1))))
        # 추출된 이미지가 저장되는 경로
        cv2.imwrite("/home/obayashi/data/first_video/test/resized_video/%s.png" % count_zero, image)
        #print('Saved frame%s.png' % count)
        count += 1

vidcap.release()
