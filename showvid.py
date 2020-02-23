import cv2

def vidsh(path):
    vs = cv2.VideoCapture(path)
    while True:
        frame = vs.read()
        frame = frame[1]
        cv2.namedWindow("Press Q")        
        cv2.moveWindow("Press Q",650,70)
        frame=cv2.resize(frame,(700,500))
        cv2.imshow("Press Q", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
                    break
    vs.release()
    cv2.destroyAllWindows()

def imgsh(path):
    while True:
        frame = cv2.imread(path)
        cv2.namedWindow("Press Q")        
        cv2.moveWindow("Press Q",650,70)
        cv2.imshow("Press Q", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
                    break
    cv2.destroyAllWindows()
