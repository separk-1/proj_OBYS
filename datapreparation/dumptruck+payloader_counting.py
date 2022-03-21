import pandas as pd
import cv2

def get_payloader_count_from_time(time, df):
    peaktime_list = list(df["PeakTime"])
    for i in df.index:
        if (time<peaktime_list[0]):
            return 0
        elif (peaktime_list[-1]<=time):
            return df.index[-1]
        elif (peaktime_list[i]<=time) & (time<peaktime_list[i+1]):
            return i+1
        else:
            pass

def get_dumptruck_count_from_time(time, df):
    count_list = list()
    count = 1
    for i in df.index:
        if df.loc[i, "Existence"] == 0:
            count_list.append(0)
        else:
            count_list.append(count)
            count+=1
    df["count"] = count_list
    for i in df.index:
        if (df.loc[i, "InTime"]<=time) & (time<=df.loc[i, "OutTime"]) & (df.loc[i, "Existence"] == 1) :
            return df.at[i, "count"]

video_path = ("./data/cycle2.mp4") ### input video
payloader_counting_df = pd.read_csv("./data/payloader_counting.csv")  ### input csv file
dumptruck_counting_df = pd.read_excel("./data/dumptruck_counting.xlsx") ### input excel file

cap = cv2.VideoCapture(video_path)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('cycle2_dumptruck+payloader.mp4', fourcc, fps, (int(width), int(height))) ### output video

time = 0
dumptruck_count_text = "0"
while (True):
    ret, frame = cap.read()
    
    if frame is None:
        break

    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0, 0, 255)
    dumptruck_count = get_dumptruck_count_from_time(time, dumptruck_counting_df)
    if dumptruck_count is not None:
        dumptruck_count_text = dumptruck_count
    else:
        dumptruck_count_text = dumptruck_count_text

    payloader_count = get_payloader_count_from_time(time, payloader_counting_df)

    cv2.putText(frame,
                'Dump Truck %s'%(dumptruck_count_text), ### text
                (900, 50),
                font, 1.5,
                color,
                4,
                cv2.LINE_4)
    cv2.putText(frame,
                'Payloader %s'%(payloader_count), ### text
                (900, 100),
                font, 1.5,
                color,
                4,
                cv2.LINE_4)

    cv2.imshow('video', frame)
    time += 1

    out.write(frame)
    
    # q 입력시 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
