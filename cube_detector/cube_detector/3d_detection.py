import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2 
from geometry_msgs.msg import Point
from cv_bridge import CvBridge 
import cv2 
 
class ImageSubscriber(Node):
  
  def __init__(self):

    super().__init__('image_subscriber')
    
    self.subscription_image = self.create_subscription(
      Image, 
      '/camera/color/image_raw', 
      self.image_callback, 
      10)
    
    self.subscription_depth = self.create_subscription(
      PointCloud2, 
      '/camera/depth/color/points', 
      self.depth_callback, 
      10)
      
    self.br = CvBridge()
   
  def image_callback(self, data):

    self.get_logger().info('Receiving video frame')
 
    current_frame = self.br.imgmsg_to_cv2(data, "bgra8")
    
    cv2.imshow("camera", current_frame)
    
    cv2.waitKey(1)

  def depth_callback(self, data):
    box_position_camera_frame = Point()
    self.pixel_to_3d_point(data, self.box_centroid_x, self.box_centroid.y, box_position_camera_frame)

  def pixel_to_3d_point(self, pCloud, u, v, point):
    arrayPosition = v*pCloud.row_step + u*pCloud.point_step
    arrayPosX = arrayPosition + pCloud.fields[0].offset
    arrayPosY = arrayPosition + pCloud.fields[1].offset
    arrayPosZ = arrayPosition + pCloud.fields[2].offset

    point.x = pCloud.data[arrayPosX]
    point.y = pCloud.data[arrayPosY]
    point.z = pCloud.data[arrayPosZ]

    return point
  
def main(args=None):
  
  rclpy.init(args=args)
  
  image_subscriber = ImageSubscriber()
  
  rclpy.spin(image_subscriber)
  
  image_subscriber.destroy_node()
  
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()