from cv2 import *
import time
def capture(camera_index,name_of_window,save_name):
    cam = VideoCapture(camera_index)   # 0 -> index of camera
    if cam is None or not cam.isOpened():
       print('Warning: unable to open image source: ', camera_index)
       exit()
    s, img = cam.read()
    if s:    # frame captured without any errors
        if name_of_window != False:
            namedWindow(name_of_window)
            imshow(name_of_window,img)
            waitKey(0)
            destroyWindow(name_of_window)
        if save_name != False:
            imwrite(save_name,img) #save image

            
def vidcapture(camera_index,name_of_window,save_name,key_for_exit):
    #Capture video from webcam
    vid_capture = cv2.VideoCapture(camera_index)
    if vid_capture is None or not vid_capture.isOpened():
       print('Warning: unable to open image source: ', camera_index)
       exit()

    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    if save_name != False:
        output = cv2.VideoWriter(save_name, vid_cod, 20.0, (640,480))        
    
    while(True):
         # Capture each frame of webcam video
         ret,frame = vid_capture.read()
         cv2.imshow(name_of_window, frame) 
         if save_name != False:
             output.write(frame)
         # Close and break the loop after pressing "x" key
         if cv2.waitKey(1) &0XFF == ord(key_for_exit):
             break
    # close the already opened camera
    vid_capture.release()
    # close the already opened file
    if save_name != False:
        output.release()
    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

    
def auto_vidcapture(camera_index,name_of_window,save_name,time_for_exit):
    #Capture video from webcam
    vid_capture = cv2.VideoCapture(camera_index)
    if vid_capture is None or not vid_capture.isOpened():
       print('Warning: unable to open image source: ', camera_index)
       exit()
    
    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    if save_name != False:
        output = cv2.VideoWriter(save_name, vid_cod, 20.0, (640,480))
    t = time_for_exit  
    while(True):
         # Capture each frame of webcam video
         ret,frame = vid_capture.read()          
         if save_name != False:
             output.write(frame)
         while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            time.sleep(1)
            t -= 1
         break
         break   
    # close the already opened camera
    vid_capture.release()
    # close the already opened file
    if save_name != False:
        output.release()
    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()    
def delay_imcapture(camera_index,name_of_window,save_name,delay_time):
    cam = VideoCapture(camera_index)   # 0 -> index of camera
    if cam is None or not cam.isOpened():
       print('Warning: unable to open image source: ', camera_index)
       exit()
    s, img = cam.read()
    time.sleep(delay_time)
    if s:    # frame captured without any errors
        if name_of_window != False:
            namedWindow(name_of_window)
            imshow(name_of_window,img)
            waitKey(0)
            destroyWindow(name_of_window)
        if save_name != False:
            imwrite(save_name,img) #save image    
def motion_detect(camera_index, key_for_exit,threshold,window_name):
    import os
    import numpy as np
    import sys
    from skimage.measure import compare_ssim
    from skimage.transform import resize
    from scipy.ndimage import imread
    print("Use from ecapture import motion as md")
    print("md.motion_detect(0,""x"",0.7,False)")
    print("Instead of from ecapture import ecapture as ec")
    print("ec.motion_detect(0,""x"",0.7,False)")
    
    #Capture video from webcam
    cam = cv2.VideoCapture(camera_index)   # 0 -> index of camera
    s, img = cam.read()
    if s:    # frame captured without any errors
        cv2.imwrite("1.jpg",img) #save image
    vid_capture = cv2.VideoCapture(camera_index)

    vid_cod = cv2.VideoWriter_fourcc(*'XVID')

    output = cv2.VideoWriter("test.avi", vid_cod, 20.0, (640,480))
    while(True):
    
        # Capture each frame of webcam video
        ret,frame = vid_capture.read()
        cv2.imwrite("2.jpg", frame)


    # get two images - resize both to 1024 x 1024
        img_a = cv2.imread("1.jpg")
        img_b = cv2.imread("2.jpg")

    # score: {-1:1} measure of the structural similarity between the images
        score, diff = compare_ssim(img_a, img_b, full=True, multichannel=True)
        if score < threshold:
            print("Detected")
            break
        else:
            print("Not Detected")
        if window_name != False:
            cv2.imshow(window_name, frame) 
             # Close and break the loop after pressing "x" key
        if cv2.waitKey(1) &0XFF == ord(key_for_exit):
            break
# close the already opened camera
    vid_capture.release()
# close the already opened file
    
    output.release()
# close the window and de-allocate any associated memory usage
    os.remove("1.jpg")
    os.remove("2.jpg")
    os.remove("test.avi")
    cv2.destroyAllWindows()


