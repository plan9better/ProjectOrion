from time import sleep

import cv2

# Open the default camera
cap = cv2.VideoCapture('input.mp4')

# Get the default frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

while True:
    ret, frame = cap.read()

    if(ret==True):
        # Write the frame to the output file
        out.write(frame)

        # Display the captured frame
        cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if ret==False or cv2.waitKey(1) == 27:
        break

    # display frame for 1/30 of a second (30fps)
    sleep(1/30)

# Release the capture and writer objects
cap.release()
out.release()
cv2.destroyAllWindows()