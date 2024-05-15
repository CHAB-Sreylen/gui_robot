import tkinter as tk
from tkinter import *
import threading
from turtlesim.msg import Pose
from std_msgs.msg import String
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

from std_msgs.msg import Int32
from .data_publisher import DataPublisher
from .draw_circle import DrawCircleNode
from rclpy.executors import MultiThreadedExecutor

class MyGUI:
    def __init__(self, data_publisher_node=None):

        # Create the main window
        self.root = tk.Tk()
        self.root.title('Tkinter Frame')
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        
        self.frame1.pack(side=tk.LEFT,fill='both',expand=True)
        self.frame2.pack(side=tk.LEFT,fill='both',expand=True)
        
        #return value to publish
        self.cw = True
        
        #value of button start, if value true it started
        self.start_value = False
        
        #value of button retry, if value false it retried
        self.retry_value = True
        
        #Team color, True = red, false = blue
        self.color_value = True

        # Set the window size
        # window_width, window_height = 1366, 768
        # self.root.geometry(f'{window_width}x{window_height}')
        # self.root.configure(bg='darkgray')

        # Create label name Location
        self.frame_location = tk.Frame(self.frame1, width=700, height=400, bg='#3c3f44')
        self.frame_location.pack_propagate(False) # Prevents the frame from adjusting to its content
        self.frame_location.pack(pady=100)
        self.frame_location.pack()
        # self.frame_location.place(x=30, y=100)
        self.label_location = tk.Label(self.frame_location, text="Location",  bg='#3c3f44', font=('Arial 40'), fg='white')
        self.label_location.pack(pady=10)
        
        # Set Location of variable x, y and live real value 
        self.lbl_x_val = tk.Label(self.frame_location, text="", font=("Arial 50"), bg='#3c3f44', fg='lightgreen')
        # self.lbl_x_val.place(x=50, y=150)
        self.lbl_x_val.pack(pady=20)  
        
        self.lbl_y_val = tk.Label(self.frame_location, text="", font=("Arial 50"), bg='#3c3f44', fg='lightgreen' )
        # self.lbl_y_val.place(x=50, y=200)
        self.lbl_y_val.pack(pady=20)

        self.lbl_theta_val = tk.Label(self.frame_location, text="", font=("Arial 50"), bg='#3c3f44', fg='lightgreen',height=80 )
        # self.lbl_theta_val.place(x=50, y=250)
        self.lbl_theta_val.pack(pady=20)

        self.lbl_number_val = tk.Label(self.frame_location, text="", font=("Arial 50"), bg='#3c3f44', fg='lightgreen',height=80)
        # self.lbl_number_val.place(x=50, y=300)

        # self.create_frame(946, 228, 390, 100, 25, "Sensor Camera:")
        self.frame_sensor = tk.Frame(self.frame2, width=500, height=400, bg='#3c3f44')
        self.frame_sensor.pack_propagate(False)  
        self.frame_sensor.pack()
        self.frame_sensor.pack(pady=100,padx=10)
        # self.frame_sensor.place(x=390, y=100)
        self.label_sensor = tk.Label(self.frame_sensor, text="Sensor Camera:", bg='#3c3f44', font=('Arial 40'), fg='yellow')
        self.label_sensor.pack(pady=10)

        
        
        #Create frame of area
        self.frame_area = tk.Frame(self.root, width=1301, height=300, bg='#3c3f44')
        # self.frame_area.pack_propagate(True)
        # self.frame_area.pack(pady=100)
        self.frame_area.pack()
        self.frame_area.pack(side=tk.BOTTOM,expand=True)

        # self.frame_area.place(x=30, y=378)
        self.label_area = tk.Label(self.frame_area, text="Area 1", bg='#3c3f44', font=('Arial 30'), fg='white')
        self.label_area.pack(pady=25)

        #Set label name currennt task in x=50 and y=410
        self.currenttask = tk.Label(self.frame_area, text="Current task", font=("Arial 30"), bg='#3c3f44', fg='red')
        # self.currenttask.place(x=50, y=410)
        self.x = 50
        x_loc = 50
        z = 0
        for i in range(10):
            self.x = self.x+190
        #if i <=6 it display in y=460 and x=x+190
            if(i <= 6):
                label = tk.Label(self.frame_area,text=f"Text {i}", bg='#3c3f44', fg='lightgreen', font=("Arial 30"))
                label.place(x=x_loc, y=460)
                x_loc = x_loc + 190
        #if i > 6 display in y=510 and x=x+190
            else:
                x_loc = 50 + 190*z
                label = tk.Label(self.frame_area,text=f"Text {i}", bg='#3c3f44', fg='lightgreen',font=("Arial 30"))
                label.place(x=x_loc, y=510)
                x_loc = x_loc + 190
                z = z + 1
        #Create button retry
        self.button_retry = tk.Button(self.root, text='Retry', command=self.toggle_button_retry, font=('Arial 30'))
        self.button_retry.place(x=190, y=676, width=120, height=40)
        self.button_retry.configure(bg='white')
        self.button_retry["state"] = "normal"
        self.button_retry.pack(side=tk.BOTTOM)

        #Create button Connected
        self.button_connected = tk.Button(self.frame1, text="Connected", command=self.toggle_button1, bg="blue", font=('Arial 30'), fg='white')
        # self.button_connected.pack(padx=5)
        self.button_connected.pack(side=tk.TOP,padx=10, pady=10)

        # self.button_connected.place(x=30, y=30, width=200, height=60)
        self.button_connected["state"] = "normal"

        # Create the second button
        self.button_blue = tk.Button(self.frame2,text="Blue", command=self.toggle_button2, bg="blue", font=('Arial 30'), fg='white')
        self.button_blue.pack(side=tk.LEFT, padx=5)
        # self.button_blue.place(x=1220, y=30, width=200, height=60)
        self.button_blue["state"] = "normal"

        # Create the Start button
        self.button_start = tk.Button(self.root, text="Start", command=self.toggle_button_start, bg="white", font=('Arial 20'), fg='white')
        self.button_start.pack(side=tk.LEFT, padx=5)
        self.button_start.place(x=30, y=676, width=120, height=40)
        self.button_start["state"] = "normal"
    
    
    def run(self):
        self.root.mainloop()
        
    # Function to trigger text when conndition true
    def toggle_button1(self):
        if self.button_connected["text"] == "Connected":
            self.button_connected["text"] = "Disconnected"
            self.button_connected["bg"] = "red"
        else:
            self.button_connected["text"] = "Connected"
            self.button_connected["bg"] = "blue"

    def toggle_button2(self):
        
        self.color_value = not self.color_value
        if self.color_value:
            self.button_blue["text"] = "Red"
            self.button_blue["bg"] = "red"
        else:
            self.button_blue["text"] = "Blue"
            self.button_blue["bg"] = "blue"

    def toggle_button_start(self):
        # self.cw = not self.cw
        self.start_value = not self.start_value
        if self.start_value:
            self.retry_value = False
            self.button_start.config(text="Started", bg='green')
        else:
            self.button_start.config(text="Start", bg='red')
    
    def toggle_button_retry(self):
        self.retry_value = not self.retry_value
        if self.retry_value:
            self.start_value = False
            self.button_retry.config(text="Retried", bg='blue')
        else:
            self.button_retry.config(text="Retry", bg='red')

class ROSNode(Node):
    def __init__(self, gui: MyGUI):
        super().__init__("ros_node")
        self.gui = gui
        
        # Create a subscriber from data_Publisher
        self.subscription_num = self.create_subscription(
            Int32MultiArray, 
            '/array_number', 
            self.number_callback, 10
        )

        # Create a subscriber to receive data from turtlesim
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose', 
            self.pose_callback, 10
        )
    
    def number_callback(self, msg):
        number = msg.data
        start_value = number[0]
        retry_value = number[1]
        color_value = number[2]
        
        print(number)
        
        if(start_value == 1):
            self.gui.button_start.config(text=' Started', fg='white', bg='green')
        else:
            self.gui.button_start.config(text=' Start', fg='black', bg='red')
            
        if(retry_value == 1):
            self.gui.button_retry.config(text='Retried', fg='white', bg='green')
        else:
            self.gui.button_retry.config(text='Retry', fg='black', bg='red')
            
        if(color_value == 1):
            self.gui.button_blue.config(text='Blue', fg='white', bg='blue')
        else:
            self.gui.button_blue.config(text='Red', fg='black', bg='red')
        
        
        # self.gui.label_area.config(text=f"Area {number}") # Set value to label_area + value of number

    def pose_callback(self, msg):
        # print(msg)
        
        # Update GUI with received pose data
        self.gui.lbl_x_val.config(text=f"x: {msg.x:.1f} mm")
        # self.gui.lbl_x_val.config(text=f"{msg.x:.2f}")
        self.gui.lbl_y_val.config(text=f"y : {msg.y:.1f} mm")
        self.gui.lbl_theta_val.config(text=f"yaw angle : {msg.theta:.1f} degree")


def start_ros_node(gui):
    rclpy.init(args=None)
    node1 = ROSNode(gui)
    node2 = DataPublisher(gui)
    node3 = DrawCircleNode(gui)
    
    #create a MultiThreadExecutor
    executor = MultiThreadedExecutor()
    
    #Add nodes to the executor
    executor.add_node(node1)
    executor.add_node(node2)
    executor.add_node(node3)
    
    executor.spin()
    node1.destroy_node()
    node2.destroy_node()
    node3.destroy_node()
    rclpy.shutdown()


def main():
    gui = MyGUI()
    gui.node = threading.Thread(target=start_ros_node, args=(gui,))
    gui.node.start()
    gui.run()

if __name__ == "__main__":
    main()