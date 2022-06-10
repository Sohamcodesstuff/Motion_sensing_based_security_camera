import cv2
import winsound
import smtplib
import imghdr
import time
from pushbullet import Pushbullet
from email.message import EmailMessage



from pushbullet import Pushbullet

pb = Pushbullet()
push = pb.push_note("Status update", "Security system enabled")
print("security system online")



def sendmail():
    try:
        Sender_Email = ""
        Reciever_Email = ""
        Password = ('')

        newMessage = EmailMessage()                         
        newMessage['Subject'] = "INTRUDER ALERT!" 
        newMessage['From'] = Sender_Email                   
        newMessage['To'] = Reciever_Email                   
        newMessage.set_content('security camera detected intruder please proceed with caution!') 

        with open('C:/Users/soham/Desktop/security_cam-main/opencvsecurity.png', 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name

        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                
            smtp.login(Sender_Email, Password)              
            smtp.send_message(newMessage)
            smtp.quit()
    except:
        push = pb.push_note("Warning", "Something went wrong with security system")
        print("sent error message")

        push = pb.push_note("Warning", "INTRUDER DETECTED CHECK IMAGE TO CONFIRM:-")
        with open("C:/Users/soham/Desktop/security_cam-main/opencvsecurity.png", "rb") as pic:
            file_data = pb.upload_file(pic, "opencvsecurity.png")
        push = pb.push_file(**file_data)
        print("sent mail with image")
        

    else:
        push = pb.push_note("Warning", "INTRUDER DETECTED CHECK IMAGE TO CONFIRM:-q")
        with open("C:/Users/soham/Desktop/security_cam-main/opencvsecurity.png", "rb") as pic:
            file_data = pb.upload_file(pic, "opencvsecurity.png")
        push = pb.push_file(**file_data)
        print("sent mail with image")
        





cam = cv2.VideoCapture(0)
while cam.isOpened():
    
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    cv2.drawContours(frame1, contours, -1, (200, 255, 0), 2)
    for c in contours:
        if cv2.contourArea(c) < 50000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        winsound.PlaySound("C:/Users/soham/Desktop/security_cam-main/alert.wav",winsound.SND_FILENAME)
        return_value, image = cam.read()
        cv2.imwrite('opencv'+'security'+'.png', image)
        
        sendmail()
        
            
        



        

            
        
    if cv2.waitKey(10) == ord('q'):
        push = pb.push_note("status update", "Camera is being manually disabled!\n if not done by you,proceed with caution.")
        print("disengaging security system")
        time.sleep(4)
        
        break
   
    
        
    cv2.imshow('security Cam', frame1)