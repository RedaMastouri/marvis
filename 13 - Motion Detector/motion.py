import cv2,time  #加入time  延时camera
from datetime import datetime
import pandas #储存时间



first_frame=None   #numpy用于存放数据

status_list=[None,None] #空List
times=[] #记录变化的时间点
df =  pandas.DataFrame(columns=["Start","End"])    #存放时间的起始和终止


video=cv2.VideoCapture(0)  #number 表示camera 

while True:
    check, frame = video.read()  #最开始的一帧

    status =0
    #time.sleep(3)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #把frame变为灰度图
    gray=cv2.GaussianBlur(gray,(21,21),0)    #高斯模糊

    if first_frame is None:  #初始化为gray
        first_frame=gray
        continue        #跳过后续                    #
    #计算第一个图和第二个图的差别
    delta_frame = cv2.absdiff(first_frame,gray)   #比较两者差异
        


    #差别大于30 变为白色
    #差别小于30 变为黑色
    thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]           #30以内的 变为黑色   [0] 用不到 [1]用得到（变化后的array）

    thresh_frame=cv2.dilate(thresh_frame,None,iterations=2)     #dilate的程度  白色区域锐度降低

    #进行轮廓监测
    (cnts,_) =cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #传入赋值array  #得到external  #找到轮廓的method
    
    for contour in cnts:
        if cv2.contourArea(contour) <10000:  #小于1000个像素 找更大的
            continue
        status=1

        (x,y,w,h)=cv2.boundingRect(contour)        #创建tuple  给出x,y,w,h
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),3)

    status_list.append(status)    

    status_list=status_list[-2:] #只需要最后两个元素 节省空间
    if status_list[-1]==1 and status_list[-2]==0:  #从0变到1
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:  #从1变到0
        times.append(datetime.now())
    
    cv2.imshow("c",gray)    
    cv2.imshow("capturing",delta_frame)     #输出差异图
    cv2.imshow("Tresh",thresh_frame)
    cv2.imshow("Frame",frame)
    key=cv2.waitKey(1)  #每个n ms 换图 
    #先wait 再release 
#用while循环实现对视频的捕捉
    

    if key == ord('q'):  #输入q则退出
        if status == 1:
            times.append(datetime.now())
        break 

print(status_list)  
print(times)  

for i in range(0,len(times),2):       #每隔2个
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

df.to_csv("Times.csv")  #保存为csv格式

video.release()     
cv2.destroyAllWindows()
