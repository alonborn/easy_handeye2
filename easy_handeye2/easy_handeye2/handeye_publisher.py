#!/usr/bin/env python

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import ParameterType, ParameterDescriptor
import tf2_ros
import geometry_msgs.msg
from easy_handeye2.handeye_calibration import load_calibration
from std_srvs.srv import Trigger

class HandeyePublisher(rclpy.node.Node):
    def __init__(self):
        super().__init__('handeye_publisher')

        self.declare_parameter('name', descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_STRING))
        self.name = self.get_parameter('name').get_parameter_value().string_value

        self.broadcaster = tf2_ros.StaticTransformBroadcaster(self)
        self.static_transformStamped = geometry_msgs.msg.TransformStamped()

        # Service to refresh the transform
        self.srv = self.create_service(Trigger, 'refresh_handeye_transform', self.handle_refresh)

        # Initial broadcast
        self.refresh_transform()

    def refresh_transform(self):
        self.get_logger().info(f'Reloading calibration from {self.name}')
        self.calibration = load_calibration(self.name)
        parameters = self.calibration.parameters

        if parameters.calibration_type == 'eye_in_hand':
            orig = parameters.robot_effector_frame
        else:
            orig = parameters.robot_base_frame
        dest = parameters.tracking_base_frame

        self.static_transformStamped.header.stamp = self.get_clock().now().to_msg()
        self.static_transformStamped.header.frame_id = orig
        self.static_transformStamped.child_frame_id = dest
        self.static_transformStamped.transform = self.calibration.transform

        self.broadcaster.sendTransform(self.static_transformStamped)
        self.get_logger().info('Transform re-broadcasted.')

    def handle_refresh(self, request, response):
        self.get_logger().info('Received request to refresh transform.')
        try:
            self.refresh_transform()
            response.success = True
            response.message = "Transform successfully refreshed."
        except Exception as e:
            response.success = False
            response.message = str(e)
        return response
