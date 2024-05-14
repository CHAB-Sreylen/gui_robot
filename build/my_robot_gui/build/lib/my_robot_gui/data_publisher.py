#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray

class DataPublisher(Node):
    def __init__(self, gui=None):
        super().__init__("data_publisher")
        self.gui = gui
        # self.publisher_ = self.create_publisher(Int32, '/number_topic', 10)
        #Array publish
        self.publish_arr = self.create_publisher(Int32MultiArray, '/array_number', 10)
        self.timer_array = self.create_timer(1.0, self.publish_array)
        # self.timer_ = self.create_timer(1.0, self.publish_number)
        # self.counter = 0
        self.start_value = 0
        self.retry_value = 0
        self.color_value = 1
    
    def publish_array(self):
        msg = Int32MultiArray()
        
        # array of msg.data[0] for start , msg.data[1] for retrying, msg.data[2] for color 
        msg.data = [self.start_value, self.retry_value, self.color_value]
        # print("Publish Number: ", msg.data)
        # self.counter += 1
        
        if self.gui is not None:
            if self.gui.start_value:
                self.start_value = 1
            else:
                self.start_value = 0
            
            if self.gui.retry_value:
                self.retry_value = 1
            else:
                self.retry_value = 0
                
            if self.gui.color_value:
                self.color_value = 1
            else:
                self.color_value = 0
        
        self.publish_arr.publish(msg)
                     
def main(args=None):
    rclpy.init(args=args)
    node = DataPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
    
# if __name__ == "__main__":
#     main()