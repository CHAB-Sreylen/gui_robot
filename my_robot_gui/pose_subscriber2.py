import tkinter as tk
from tkinter import *
import threading
from turtlesim.msg import Pose
from std_msgs.msg import String
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from PIL import Image, ImageTk
from std_msgs.msg import Int32
from .data_publisher import DataPublisher
from .draw_circle import DrawCircleNode
from rclpy.executors import MultiThreadedExecutor
import os
from PIL import Image, ImageTk, ImageFilter
from ament_index_python.packages import get_package_share_directory
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

        # Create a label to display the image

        # Set the window size
        window_width, window_height = 1366, 768
        self.root.geometry(f'{window_width}x{window_height}')
        self.root.configure(bg='#D9D9D9')

        # Configure grid
        for i in range(6):
            self.root.grid_columnconfigure(i, weight=1) # weight refer to the extra space of column when the window resize 
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)

        package_share_directory = get_package_share_directory('my_robot_gui')

        # Construct the path to the image file
        image_path = os.path.join(package_share_directory, 'assets', 'itc_logo.png')
        print(image_path)
       
        image = Image.open(image_path)
        desired_width = 100
        desired_height = 100
        image = image.resize((desired_width, desired_height))
        # image = self.remove_background(image)
        self.photo = ImageTk.PhotoImage(image)
        # image = self.remove_background(image)
        # self.photo = self.remove_background(image)

 
        # Create a label to display the image
        self.image_label = tk.Label(self.root,image=self.photo)
        # self.image_label.pack()
        self.image_label.grid(row=0, column=1)
        # self.image_label.pack(row=0,column=0, side=tk.TOP)

        

        self.button_connected = tk.Button(self.root, text="Connected", command=self.toggle_button1, bg="blue", font=('Arial 30 bold'), fg='white') 
        self.button_connected.grid(row=0, column=0, padx=30, pady=20, sticky="nsew")

        self.button_blue = tk.Button(self.root, text="Blue Team", command=self.toggle_button2, bg="blue", font=('Arial 30 bold'), fg='white')
        self.button_blue.grid(row=0, column=5, padx=30, pady=20, sticky="nsew")

        # Create frames and labels
        self.frame_location = tk.Frame(self.root, bg='#3c3f44')
        self.frame_location.grid(row=1, column=0, columnspan=2, padx=30, sticky="nsew")
        self.label_location = tk.Label(self.frame_location, text="Location", bg='#3c3f44', font=('Arial 30 bold'), fg='yellow')
        self.label_location.pack(pady=10)

        # frame of variable x 
        self.frame_x = tk.Frame(self.frame_location,bg='#3c3f44')
        self.frame_x.pack(side=tk.TOP, anchor="nw",padx=30)
        self.lbl_x = tk.Label(self.frame_x, text="X:", font=("Arial 40 bold"), bg='#3c3f44', fg='#38E54D')
        self.lbl_x.pack(side=tk.LEFT)
        self.lbl_x_val = tk.Label(self.frame_x, text="",  bg='#3c3f44', fg='#38E54D')
        self.lbl_x_val.pack(side=tk.LEFT, padx=10)

        # frame of variable y 

        self.frame_yaw = tk.Frame(self.frame_location,bg='#3c3f44')
        self.frame_yaw.pack(side=tk.RIGHT,pady=20)
        self.lbl_yaw = tk.Label(self.frame_yaw, text="Yaw:", font=("Arial 40 bold"), bg='#3c3f44', fg='#5AB2FF')
        self.lbl_yaw.pack(anchor='n')
        self.lbl_yaw_val = tk.Label(self.frame_yaw, text="",  bg='#3c3f44', fg='#5AB2FF')
        self.lbl_yaw_val.pack(anchor='s', padx=10)


        # self.lbl_y_val = tk.Label(self.frame_location, text="", font=("Arial 50 bold"), bg='#3c3f44', fg='lightgreen')
        # self.lbl_y_val.pack()

        #frame of variable yaw
        self.frame_y = tk.Frame(self.frame_location,bg='#3c3f44')
        self.frame_y.pack(side=tk.BOTTOM,anchor="nw",padx=30)
        self.lbl_y= tk.Label(self.frame_y, text="y:", font=("Arial 40 bold"), bg='#3c3f44', fg='#FFA62F')
        self.lbl_y.pack(side=tk.LEFT)
        self.lbl_y_val = tk.Label(self.frame_y, text="", bg='#3c3f44', fg='#FFA62F')
        self.lbl_y_val.pack(side=tk.LEFT, pady=30,padx=10)

        # self.lbl_yaw_val = tk.Label(self.frame_location, text="", font=("Arial 50 bold"), bg='#3c3f44', fg='lightgreen')
        # self.lbl_yaw_val.pack()
        self.lbl_number_val = tk.Label(self.frame_location, text="", font=("Arial 50 bold"), bg='#3c3f44', fg='lightgreen')
        self.lbl_number_val.pack()

        self.frame_sensor = tk.Frame(self.root, bg='#3c3f44')
        self.frame_sensor.grid(row=1, column=2, columnspan=4, padx=30,  sticky="nsew")
        self.label_sensor = tk.Label(self.frame_sensor, text="Sensor of R1:", bg='#3c3f44', font=('Arial 30 bold bold'), fg='yellow')
        
        self.frame_lidar = tk.Label(self.frame_sensor,bg='#3c3f44')
        self.frame_lidar.pack(side=tk.TOP,anchor="nw",padx=30,pady=10)

        self.lbl_lidar= tk.Label(self.frame_lidar,text="Lidar: ",font=("Arial 50 bold"),bg='#3c3f44', fg='lightgreen')
        self.lbl_lidar.pack(side=tk.LEFT,pady=10)
        self.lbl_finder_X = tk.Label(self.frame_lidar,text="",font=("Arial 50 bold"),bg='#3c3f44', fg='lightgreen')
        self.lbl_finder_X.pack(side=tk.LEFT,pady=10)
        self.lbl_finder_Y = tk.Label(self.frame_lidar,text="",font=("Arial 50 bold"),bg='#3c3f44', fg='lightgreen')
        self.lbl_finder_Y.pack(side=tk.LEFT,pady=10)

        self.lbl_odemetery_X = tk.Label(self.frame_sensor, text="", font=("Arial 50 bold"), bg='#3c3f44', fg='lightgreen', anchor='w')
        self.lbl_odemetery_X.pack(side='top', fill='x', pady=10,padx=30)

        self.lbl_odemetery_Y = tk.Label(self.frame_sensor, text="", font=("Arial 50 bold"), bg='#3c3f44', fg='lightgreen', anchor='w')
        self.lbl_odemetery_Y.pack(side='top', fill='x', pady=10,padx=30)

        self.lbl_IMU_Z = tk.Label(self.frame_sensor, text="", font=("Arial 50 bold"), bg='#3c3f44', fg='lightgreen', anchor='w')
        self.lbl_IMU_Z.pack(side='top', fill='x', pady=10, padx=30)

        self.frame_area = tk.Frame(self.root, bg='#3c3f44')
        self.frame_area.grid(row=2,rowspan=3, column=0, columnspan=6, padx=30, pady=10, sticky="nsew")
        self.label_area = tk.Label(self.frame_area, text="R2", bg='#3c3f44', font=('Arial 30 bold'), fg='yellow')
        self.label_area.pack(pady=10)
        self.currenttask = tk.Label(self.frame_area, text="Current Task:", font=("Arial 15 bold"), bg='#3c3f44', fg='yellow')
        self.currenttask.pack(side=tk.TOP, padx=70, anchor='w')

        self.label_task=tk.Label(self.frame_area,text=" ",font=("Arial 50 bold"), bg='#3c3f44', fg='yellow')
        self.label_task.pack()

        
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

    # def remove_background(self, image):
    #     # Example of simple background removal using ImageFilter
    #     # You may need more sophisticated techniques depending on your images
    #     return image.filter(ImageFilter.)
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

        self.sensor1 = "X"
        self.sensor2 = "Y"
        self.sensor3 = "Odometery X "
        self.sensor4 = "Odometery Y"
        self.sensor5 = "IMU Z"
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
        self.subscription_number = self.create_subscription(
            Int32,
            '/number_topic',
            self.number_data,
            10
        )

    def number_callback(self, msg):
        number = msg.data
        start_value = number[0]
        retry_value = number[1]
        color_value = number[2]
        

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

        
    
    def number_data(self, msg):
        number = msg.data
        
        if number == 1:
            self.gui.label_task.config(text='Pick up seeding', fg='white')
        elif number == 2:
            self.gui.label_task.config(text='Planting seeding', fg='white')
        elif number == 3:
            self.gui.label_task.config(text='Collect empty grain', fg='white')
        else:
            self.gui.label_task.config(text='collect padding rice', fg='white')


    def pose_callback(self, msg):
        self.gui.lbl_x_val.config(text=f"{msg.x:.1f} ", font=("Arial", 110, "bold",),)
        self.gui.lbl_y_val.config(text=f"{msg.y:.1f} ", font=("Arial", 110, "bold",))
        self.gui.lbl_yaw_val.config(text=f"{msg.y:.1f} ", font=("Arial", 110, "bold",))
        self.gui.lbl_finder_X.config(text=f"{self.sensor1} =  {msg.x:.1f} ")
        self.gui.lbl_finder_Y.config(text=f"{self.sensor2} =  {msg.y:.1f} ")
        self.gui.lbl_odemetery_X.config(text=f"{self.sensor3} =  {msg.y:.1f} ")
        self.gui.lbl_odemetery_Y.config(text=f"{self.sensor4} =  {msg.y:.1f} ")
        self.gui.lbl_IMU_Z.config(text=f"{self.sensor5} =  {msg.y:.1f} ")



       
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