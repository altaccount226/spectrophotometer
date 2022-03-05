# import the opencv library
import cv2
import os
import datetime

def capture_image(filename, device):
    
    for file in os.listdir(os.path.join(os.getcwd(), 'pics')):
        if file.startswith(filename):
            print("Error: file with name '" + filename + ".png' already exists!")
            return -1
    
    vid = cv2.VideoCapture(device, cv2.CAP_DSHOW)
  
    print("Press 'c' to capture image or 'q' to quit.")
    
    print("If the wrong camera is shown, try a different device number >= 0.")
    
    while(True):
        current_time = datetime.datetime.now()

        r, frame = vid.read()

        try:
            cv2.imshow('frame', frame)
        except:
            print("Error opening spectrophotometer camera, try a different device number.")
            return -1

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('c'):
            flag, image = vid.read()
            if flag:
                filename += '.png'
                #name = str(current_time.strftime("%Y-%m-%d-%H%M%S"))
                print("Saved " + filename + " to pics/" + filename)
                #cv2.imwrite(os.path.join(os.getcwd(), 'pics', "%(num)d_%(name)s.png") % {'num': count, 'name': name}, image)
                cv2.imwrite(os.path.join(os.getcwd(), 'pics', filename), image)
                break

    vid.release()
    cv2.destroyAllWindows()
    return filename
