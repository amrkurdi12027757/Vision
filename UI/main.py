import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
import threading


RED = []
GREEN = []
BLUE = []

# Open the text file for reading
with open("R_values.txt", "r") as file:
    # Read the lines from the file
    lines = file.readlines()
    
    # Iterate over the lines
    for line in lines:
        # Split the line by ":"
        parts = line.split(":")
        
        # Extract the numeric value from the second part
        value = float(parts[1].strip())
        
        # Append the value to the tab1 array
        RED.append(value)
        
with open("G_values.txt", "r") as file:
    # Read the lines from the file
    lines = file.readlines()
    
    # Iterate over the lines
    for line in lines:
        # Split the line by ":"
        parts = line.split(":")
        
        # Extract the numeric value from the second part
        value = float(parts[1].strip())
        
        # Append the value to the tab1 array
        GREEN.append(value)
        
with open("B_values.txt", "r") as file:
    # Read the lines from the file
    lines = file.readlines()
    
    # Iterate over the lines
    for line in lines:
        # Split the line by ":"
        parts = line.split(":")
        
        # Extract the numeric value from the second part
        value = float(parts[1].strip())
        
        # Append the value to the tab1 array
        BLUE.append(value)



# Initialize the GUI window
root = tk.Tk()
root.title("Vision: Gestures Detector")
root.geometry()


# Create a frame to hold the left-side components
left_frame = ttk.Frame(root, width=400, height=600)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


# Create the tabs with range sliders and a button in each
# Create three tabs for the sliders
tab_control = ttk.Notebook(left_frame)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab1, text="R")
tab_control.add(tab2, text="G")
tab_control.add(tab3, text="B")
tab_control.pack(expand=1, fill="both")


# Create labels:
# tab1 : Red
tab1_label1 = ttk.Label(tab1, text="H MIN : 0")
tab1_label2 = ttk.Label(tab1, text="H MAX : 0")
tab1_label3 = ttk.Label(tab1, text="S MIN : 0")
tab1_label4 = ttk.Label(tab1, text="S MAX : 0")
tab1_label5 = ttk.Label(tab1, text="V MIN : 0")
tab1_label6 = ttk.Label(tab1, text="V MAX : 0")

# tab2 : Green
tab2_label1 = ttk.Label(tab2, text="H MIN : 0")
tab2_label2 = ttk.Label(tab2, text="H MAX : 0")
tab2_label3 = ttk.Label(tab2, text="S MIN : 0")
tab2_label4 = ttk.Label(tab2, text="S MAX : 0")
tab2_label5 = ttk.Label(tab2, text="V MIN : 0")
tab2_label6 = ttk.Label(tab2, text="V MAX : 0")

# tab3 : Blue
tab3_label1 = ttk.Label(tab3, text="H MIN :0")
tab3_label2 = ttk.Label(tab3, text="H MAX :0")
tab3_label3 = ttk.Label(tab3, text="S MIN :0")
tab3_label4 = ttk.Label(tab3, text="S MAX :0")
tab3_label5 = ttk.Label(tab3, text="V MIN :0")
tab3_label6 = ttk.Label(tab3, text="V MAX :0")


# Create sliders:
# tab1 : Red
tab1_slider1 = ttk.Scale(tab1, from_=0, to=255, orient=tk.HORIZONTAL)
tab1_slider2 = ttk.Scale(tab1, from_=0, to=255, orient=tk.HORIZONTAL)
tab1_slider3 = ttk.Scale(tab1, from_=0, to=255, orient=tk.HORIZONTAL)
tab1_slider4 = ttk.Scale(tab1, from_=0, to=255, orient=tk.HORIZONTAL)
tab1_slider5 = ttk.Scale(tab1, from_=0, to=255, orient=tk.HORIZONTAL)
tab1_slider6 = ttk.Scale(tab1, from_=0, to=255, orient=tk.HORIZONTAL)

tab1_slider1.set(RED[0])
tab1_slider2.set(RED[1])
tab1_slider3.set(RED[2])
tab1_slider4.set(RED[3])
tab1_slider5.set(RED[4])
tab1_slider6.set(RED[5])

# tab2 : Green
tab2_slider1 = ttk.Scale(tab2, from_=0, to=100, orient=tk.HORIZONTAL)
tab2_slider2 = ttk.Scale(tab2, from_=0, to=100, orient=tk.HORIZONTAL)
tab2_slider3 = ttk.Scale(tab2, from_=0, to=100, orient=tk.HORIZONTAL)
tab2_slider4 = ttk.Scale(tab2, from_=0, to=100, orient=tk.HORIZONTAL)
tab2_slider5 = ttk.Scale(tab2, from_=0, to=100, orient=tk.HORIZONTAL)
tab2_slider6 = ttk.Scale(tab2, from_=0, to=100, orient=tk.HORIZONTAL)

tab2_slider1.set(GREEN[0])
tab2_slider2.set(GREEN[1])
tab2_slider3.set(GREEN[2])
tab2_slider4.set(GREEN[3])
tab2_slider5.set(GREEN[4])
tab2_slider6.set(GREEN[5])

# tab3 : Blue
tab3_slider1 = ttk.Scale(tab3, from_=0, to=100, orient=tk.HORIZONTAL)
tab3_slider2 = ttk.Scale(tab3, from_=0, to=100, orient=tk.HORIZONTAL)
tab3_slider3 = ttk.Scale(tab3, from_=0, to=100, orient=tk.HORIZONTAL)
tab3_slider4 = ttk.Scale(tab3, from_=0, to=100, orient=tk.HORIZONTAL)
tab3_slider5 = ttk.Scale(tab3, from_=0, to=100, orient=tk.HORIZONTAL)
tab3_slider6 = ttk.Scale(tab3, from_=0, to=100, orient=tk.HORIZONTAL)

tab3_slider1.set(BLUE[0])
tab3_slider2.set(BLUE[1])
tab3_slider3.set(BLUE[2])
tab3_slider4.set(BLUE[3])
tab3_slider5.set(BLUE[4])
tab3_slider6.set(BLUE[5])


# packing to frames
# tab1: Red
tab1_label1.pack()
tab1_slider1.pack()
tab1_label2.pack()
tab1_slider2.pack()
tab1_label3.pack()
tab1_slider3.pack()
tab1_label4.pack()
tab1_slider4.pack()
tab1_label5.pack()
tab1_slider5.pack()
tab1_label6.pack()
tab1_slider6.pack()

# tab2:Green
tab2_label1.pack()
tab2_slider1.pack()
tab2_label2.pack()
tab2_slider2.pack()
tab2_label3.pack()
tab2_slider3.pack()
tab2_label4.pack()
tab2_slider4.pack()
tab2_label5.pack()
tab2_slider5.pack()
tab2_label6.pack()
tab2_slider6.pack()

#tab 3 : Blue
tab3_label1.pack()
tab3_slider1.pack()
tab3_label2.pack()
tab3_slider2.pack()
tab3_label3.pack()
tab3_slider3.pack()
tab3_label4.pack()
tab3_slider4.pack()
tab3_label5.pack()
tab3_slider5.pack()
tab3_label6.pack()
tab3_slider6.pack()

# make save button:
# tab1: Red
tab1_button = ttk.Button(tab1, text="Save", command=lambda: save_slider_values(1))
tab1_button.pack(side=tk.BOTTOM, anchor=tk.CENTER)

# tab2: Green
tab2_button = ttk.Button(tab2, text="Save", command=lambda: save_slider_values(2))
tab2_button.pack(side=tk.BOTTOM, anchor=tk.CENTER)

# tab3: Blue
tab3_button = ttk.Button(tab3, text="Save", command=lambda: save_slider_values(3))
tab3_button.pack(side=tk.BOTTOM, anchor=tk.CENTER)


# Create a function to save the slider values to a text file
def save_slider_values(tab_num):
    if tab_num == 1:
        file_name = "R_values.txt"
        slider1_val = tab1_slider1.get()
        slider2_val = tab1_slider2.get()
        slider3_val = tab1_slider3.get()
        slider4_val = tab1_slider4.get()
        slider5_val = tab1_slider5.get()
        slider6_val = tab1_slider6.get()
    elif tab_num == 2:
        file_name = "G_values.txt"
        slider1_val = tab2_slider1.get()
        slider2_val = tab2_slider2.get()
        slider3_val = tab2_slider3.get()
        slider4_val = tab2_slider4.get()
        slider5_val = tab2_slider5.get()
        slider6_val = tab2_slider6.get()
    elif tab_num == 3:
        file_name = "B_values.txt"
        slider1_val = tab3_slider1.get()
        slider2_val = tab3_slider2.get()
        slider3_val = tab3_slider3.get()
        slider4_val = tab3_slider4.get()
        slider5_val = tab3_slider5.get()
        slider6_val = tab3_slider6.get()
    
    with open(file_name, "w") as f:
        f.write(f"R_H_MIN Value: {slider1_val}\n")
        f.write(f"R_H_MAX Value: {slider2_val}\n")
        f.write(f"G_S_MIN Value: {slider3_val}\n")
        f.write(f"G_S_MAX Value: {slider4_val}\n")
        f.write(f"B_V_MIN Value: {slider5_val}\n")
        f.write(f"B_V_MAX Value: {slider6_val}\n")

# Create a function to update each slider label


    
    
# Create a frame to hold the right-side components
right_frame = ttk.Frame(root, width=400, height=600)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create a label to display the camera stream
stream_label = ttk.Label(right_frame)
stream_label.pack(side=tk.TOP, padx=10, pady=10)

# Define a function to capture video from the camera and display it in the label
def update_camera_stream():
    cap = cv2.VideoCapture(1)
    
    while True:
        _, frame = cap.read()
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = PIL.ImageTk.PhotoImage(image=img)
        stream_label.imgtk = imgtk
        stream_label.configure(image=imgtk)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

# Start the camera stream in a new thread

camera_thread = threading.Thread(target=update_camera_stream)
camera_thread.start()

# Start the GUI main loop
root.mainloop()
