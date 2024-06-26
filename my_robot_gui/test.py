import tkinter as tk
from tkinter import *
import threading
from turtlesim.msg import Pose
from std_msgs.msg import Int32MultiArray
import rclpy
from rclpy.node import Node
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
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)

        # Create buttons
        self.button_connected = tk.Button(self.root, text="Connected", command=self.toggle_button1, bg="blue", font=('Arial 15'), fg='white')
        self.button_connected.grid(row=0, column=0, padx=30, pady=10, sticky="nsew")
        self.button_blue = tk.Button(self.root, text="Blue Team", command=self.toggle_button2, bg="blue", font=('Arial 15'), fg='white')
        self.button_blue.grid(row=0, column=5, padx=30, pady=10, sticky="nsew")

        # Create frames and labels
        self.frame_location = tk.Frame(self.root, bg='#3c3f44')
        self.frame_location.grid(row=1, column=0, columnspan=3, padx=30, pady=10, sticky="nsew")
        self.label_location = tk.Label(self.frame_location, text="Location", bg='#3c3f44', font=('Arial 20'), fg='yellow')
        self.label_location.pack(pady=10)
        self.lbl_x_val = tk.Label(self.frame_location, text="X = 0.00", font=("Arial 16"), bg='#3c3f44', fg='lightgreen')
        self.lbl_x_val.pack()
        self.lbl_y_val = tk.Label(self.frame_location, text="Y = 0.00", font=("Arial 16"), bg='#3c3f44', fg='lightgreen')
        self.lbl_y_val.pack()

        self.frame_sensor = tk.Frame(self.root, bg='#3c3f44')
        self.frame_sensor.grid(row=1, column=3, columnspan=3, padx=30, pady=10, sticky="nsew")
        self.label_sensor = tk.Label(self.frame_sensor, text="Sensor Camera:", bg='#3c3f44', font=('Arial 20'), fg='yellow')
        self.label_sensor.pack(pady=10)

        self.frame_area = tk.Frame(self.root, bg='#3c3f44')
        self.frame_area.grid(row=2, column=0, columnspan=6, padx=30, pady=10, sticky="nsew")
        self.label_area = tk.Label(self.frame_area, text="Area1", bg='#3c3f44', font=('Arial 20'), fg='yellow')
        self.label_area.pack(pady=10)
        self.currenttask = tk.Label(self.frame_area, text="Current Task:", font=("Arial 11"), bg='#3c3f44', fg='red')
        self.currenttask.pack()

        # Dynamically create and place 6 labels for task text in rows
        self.task_frames = []
        for i in range(2):  # Create 2 rows, each can hold 3 labels
            frame = tk.Frame(self.frame_area, bg='#3c3f44')
            frame.pack()
            self.task_frames.append(frame)

        for i in range(6):
            if i % 3 == 0:
                current_frame = self.task_frames[i // 3]
            label = tk.Label(current_frame, text=f"Task{i+1}: {self.tasks[i]}", bg='#3c3f44', fg='pink')
            label.pack(side=tk.LEFT, padx=10, pady=5)


        self.button_start = tk.Button(self.root, text="Start", command=self.toggle_button_start, bg="green", font=('Arial 15'), fg='black')
        self.button_start.grid(row=6, column=0, padx=30, pady=10, sticky="nsew")
        self.button_retry = tk.Button(self.root, text='Retry', command=self.toggle_button_retry, font=('Arial 15'))
        self.button_retry.grid(row=6, column=1, padx=30, pady=10, sticky="nsew")
        self.button_retry.configure(bg='red')

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

        if start_value == 1:
            self.gui.button_start.config(text='Started', fg='white', bg='green')
        else:
            self.gui.button_start.config(text='Start', fg='black', bg='red')

        if retry_value == 1:
            self.gui.button_retry.config(text='Retried', fg='white', bg='green')
        else:
            self.gui.button_retry.config(text='Retry', fg='black', bg='red')

        if color_value == 1:
            self.gui.button_blue.config(text='Blue', fg='white', bg='blue')
        else:
            self.gui.button_blue.config(text='Red', fg='black', bg='red')

    def pose_callback(self, msg):
        self.gui.lbl_x_val.config(text=f"x: {msg.x:.1f} mm")
        self.gui.lbl_y_val.config(text=f"y: {msg.y:.1f} mm")

def start_ros_node(gui):
    rclpy.init(args=None)
    node1 = ROSNode(gui)

    executor = MultiThreadedExecutor()
    executor.add_node(node1)

    executor.spin()
    node1.destroy_node()
    rclpy.shutdown()

def main():
    gui = MyGUI()
    gui_thread = threading.Thread(target=start_ros_node, args=(gui,))
    gui_thread.start()
    gui.run()

if __name__ == "__main__":
    main()
