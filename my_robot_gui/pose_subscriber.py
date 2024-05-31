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
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title('Tkinter Frame Example')

        # Initialize variables
        self.cw = True
        self.start_value = False
        self.retry_value = True
        self.color_value = True

        #Task value
        self.tasks = [
            "Hello World 1", 
            "Hello World 2", 
            "Hello World 3", 
            "Hello World 4", 
            "Hello World 5", 
            "Hello World 6"
        ] # only 6 value to this array

        # Set the window size
        window_width, window_height = 1366, 768
        self.root.geometry(f'{window_width}x{window_height}')
        self.root.configure(bg='darkgray')

        # Configure grid
        for i in range(6):
            self.root.grid_columnconfigure(i, weight=1) # weight refer to the extra space of column when the window resize 
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)

        # Create buttons
        self.button_connected = tk.Button(self.root, text="Connected", command=self.toggle_button1, bg="blue", font=('Arial 30 bold'), fg='white') 
        self.button_connected.grid(row=0, column=0, padx=30, pady=50, sticky="nsew")

        # n = north, s=south, e = east, w=west , expand with horizontal and vertical

        self.button_blue = tk.Button(self.root, text="Blue Team", command=self.toggle_button2, bg="blue", font=('Arial 30 bold'), fg='white')
        self.button_blue.grid(row=0, column=5, padx=30, pady=50, sticky="nsew")

        # Create frames and labels
        self.frame_location = tk.Frame(self.root, bg='#3c3f44')
        self.frame_location.grid(row=1, column=0, columnspan=2, padx=30, sticky="nsew")
        self.label_location = tk.Label(self.frame_location, text="Location", bg='#3c3f44', font=('Arial 30 bold'), fg='yellow')
        self.label_location.pack(pady=10)
        self.lbl_x_val = tk.Label(self.frame_location, text="", font=("Arial 50 bold"), bg='#3c3f44', fg='lightgreen')
        self.lbl_x_val.pack(pady=10)
        self.lbl_y_val = tk.Label(self.frame_location, text="", font=("Arial 50 bold"), bg='#3c3f44', fg='lightgreen')
        self.lbl_y_val.pack()
        self.lbl_yaw_val = tk.Label(self.frame_location, text="", font=("Arial 50 bold"), bg='#3c3f44', fg='lightgreen')
        self.lbl_yaw_val.pack()
        self.lbl_number_val = tk.Label(self.frame_location, text="", font=("Arial 50 bold"), bg='#3c3f44', fg='lightgreen')
        self.lbl_number_val.pack()

        self.frame_sensor = tk.Frame(self.root, bg='#3c3f44')
        self.frame_sensor.grid(row=1, column=2, columnspan=4, padx=30,  sticky="nsew")
        self.label_sensor = tk.Label(self.frame_sensor, text="Sensor of Ros1:", bg='#3c3f44', font=('Arial 30 bold bold'), fg='yellow')
        self.label_sensor.pack(pady=10)
        self.lbl_finder_X = tk.Label(self.frame_sensor,text="",font=("Arial 50 bold"),bg='#3c3f44', fg='lightgreen')
        self.lbl_finder_X.pack(pady=5)
        self.lbl_finder_Y = tk.Label(self.frame_sensor,text="",font=("Arial 50 bold"),bg='#3c3f44', fg='lightgreen')
        self.lbl_finder_Y.pack(pady=5)
        self.lbl_IMU_Z = tk.Label(self.frame_sensor,text="",font=("Arial 50 bold"),bg='#3c3f44', fg='lightgreen')
        self.lbl_IMU_Z.pack(pady=5,padx=50,anchor='w')
        self.lbl_proximity=tk.Label(self.frame_sensor,text="",font=("Arial 50 bold"),bg='#3c3f44', fg='lightgreen')
        self.lbl_proximity.pack(pady=5)

        self.frame_area = tk.Frame(self.root, bg='#3c3f44')
        self.frame_area.grid(row=2,rowspan=3, column=0, columnspan=6, padx=30, pady=10, sticky="nsew")
        self.label_area = tk.Label(self.frame_area, text="Area1", bg='#3c3f44', font=('Arial 30 bold'), fg='yellow')
        self.label_area.pack(pady=10)
        self.currenttask = tk.Label(self.frame_area, text="Current Task:", font=("Arial 30 bold"), bg='#3c3f44', fg='yellow')
        self.currenttask.pack(side=tk.TOP, padx=70, anchor='w')

        # Dynamically create and place 6 labels for task text in rows
        self.task_frames = []
        for i in range(2):  # Create 2 rows, each can hold 3 labels
            self.frame = tk.Frame(self.frame_area, bg='#3c3f44')
            # self.frame.pack(side=tk.BOTTOM,expand=True)
            self.frame.pack()
            self.task_frames.append(self.frame)
            # add to the list 
        for i in range(6):
            if i % 3 == 0:
                self.current_frame = self.task_frames[i // 3]
            self.label = tk.Label(self.current_frame, text=f"Task{i+1}: {self.tasks[i]}", bg='#3c3f44', fg='pink',font=("Arial", 40,"bold"))
            self.label.pack(side=tk.LEFT,anchor='w', padx=30, pady=10)
            # tk.left : pack the widget to the left side of container
            # anchor = 'w': refer the point of label to the west side in the pack (parent) 
            # self.label.pack(anchor='w', padx=30, pady=10)
        
        # Button Start
        self.button_start = tk.Button(self.root, text="Start", command=self.toggle_button_start, bg="green", font=('Arial 30 bold'), fg='white')
        self.button_start.grid(row=6, column=0, padx=30, pady=10, sticky="nsew")
        # Button retry 
        self.button_retry = tk.Button(self.root, text='Retry', command=self.toggle_button_retry, font=('Arial 30 bold'))
        self.button_retry.grid(row=6, column=1, padx=100, pady=10, sticky="nsew")
        self.button_retry.configure(bg='red')
        # configure use to change the properties form blue to red in widget 

    def run(self):
        self.root.mainloop()

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

        self.subscription_num = self.create_subscription(
            Int32MultiArray,
            '/array_number',
            self.number_callback,
            10
        )

        self.subscription_pose = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

    def number_callback(self, msg):
        number = msg.data
        start_value = number[0]
        retry_value = number[1]
        color_value = number[2]
        task_value= number[3]

        if start_value == 1:
            self.gui.button_start.config(text='Started', fg='white', bg='green')
        else:
            self.gui.button_start.config(text='Start', fg='white', bg='red')

        if retry_value == 1:
            self.gui.button_retry.config(text='Retried', fg='white', bg='green')
        else:
            self.gui.button_retry.config(text='Retry', fg='white', bg='red')

        if color_value == 1:
            self.gui.button_blue.config(text='Blue', fg='white', bg='blue')
        else:
            self.gui.button_blue.config(text='Red', fg='white', bg='red')

        # if task_value == 1:
        #     self.gui.config(text='Pick up seeding', fg='white')
        # if task_value == 2:
        #     self.gui.config(text='Planting seeding', fg='white')
        # if task_value == 3:
        #     self.gui.config(text='Collect empty grain', fg='white')
        # else:
        #     self.gui.config(text='collect padding rice', fg='white')
    


    def pose_callback(self, msg):
        self.gui.lbl_x_val.config(text=f"x: {msg.x:.1f} ")
        self.gui.lbl_y_val.config(text=f"y: {msg.y:.1f} ")
        self.gui.lbl_yaw_val.config(text=f"yaw: {msg.y:.1f} ")
        self.gui.lbl_finder_X.config(text=f"Range Finder X =  {msg.x:.1f} ")
        self.gui.lbl_finder_Y.config(text=f"Range Finder Y =  {msg.y:.1f} ")
        self.gui.lbl_IMU_Z.config(text=f"IMU Z =  {msg.y:.1f} ")
        self.gui.lbl_proximity.config(text=f"Range Finder X =  {msg.y:.1f} ")



       
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