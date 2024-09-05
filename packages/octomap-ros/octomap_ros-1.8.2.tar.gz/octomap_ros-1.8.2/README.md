<h1 align="center">octomap_ros</h1>
<h4 align="center">Python binding of <a href="https://github.com/OctoMap/octomap">the OctoMap library</a> for ROS (Robot Operating System).</h4>
<div align="center">
  <a href="https://pypi.python.org/pypi/octomap_ros"><img src="https://img.shields.io/pypi/v/octomap_ros.svg"></a>
  <a href="https://pypi.org/project/octomap_ros"><img src="https://img.shields.io/pypi/pyversions/octomap_ros.svg"></a>
</div>

## Installation

### ROS Humble Integration

To use OctoMap with ROS Humble, install the following ROS packages:

```bash
sudo apt-get install ros-humble-octomap ros-humble-octomap-mapping ros-humble-octomap-server
```

These packages provide the necessary ROS integration for OctoMap:

- `ros-humble-octomap`: Core OctoMap library for ROS
- `ros-humble-octomap-mapping`: Provides mapping capabilities using OctoMap
- `ros-humble-octomap-server`: Offers a ROS server for OctoMap, allowing you to save, load, and publish OctoMaps

### Python Package

Install `octomap_ros` directly from PyPI:

```bash
pip install octomap-ros
```

**Prerequisites:**

* Python development headers: `sudo apt-get install python3-dev`
* C++ compiler: `sudo apt-get install build-essential`
* CMake: `sudo apt-get install cmake`

## ROS Humble Usage

Here's a basic example of how to use OctoMap with ROS Humble:

```python
import rclpy
from rclpy.node import Node
from octomap_msgs.msg import Octomap
import octomap

class OctomapProcessor(Node):
    def __init__(self):
        super().__init__('octomap_processor')
        self.subscription = self.create_subscription(
            Octomap,
            '/octomap_binary',
            self.octomap_callback,
            10)
        self.octree = octomap.OcTree(0.1)  # 0.1 is the resolution

    def octomap_callback(self, msg):
        # Convert ROS message to OcTree
        tree = octomap.OcTree.from_msg(msg)
    
        # Process the OcTree
        for node in tree.iterator():
            if tree.isNodeOccupied(node):
                # Process occupied nodes
                coord = node.getCoordinate()
                print(f"Occupied node at {coord.x()}, {coord.y()}, {coord.z()}")

        # You can also update your own OcTree
        self.octree.insertPointCloud(tree.getPointCloud(), octomap.point3d(0, 0, 0))

def main(args=None):
    rclpy.init(args=args)
    octomap_processor = OctomapProcessor()
    rclpy.spin(octomap_processor)
    octomap_processor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This example demonstrates how to:

1. Subscribe to the `/octomap_binary` topic
2. Process incoming OctoMap messages
3. Convert ROS messages to OcTree objects
4. Iterate through occupied nodes in the OcTree
5. Update a local OcTree with new data

To run the OctoMap server and visualize the data:

```bash
# Run the octomap server
ros2 run octomap_server octomap_server_node

# In another terminal, run your OctoMap processor
python3 your_octomap_processor.py

# View the OctoMap in RViz
ros2 run rviz2 rviz2
```

Configure RViz to display the OctoMap by adding an OccupancyGrid or MarkerArray display and setting the appropriate topic (usually `/octomap_binary` or `/octomap_full`).

## Acknowledgement

This package is based on [wkentaro/octomap-python](https://github.com/wkentaro/octomap-python) and [neka-nat/python-octomap](https://github.com/neka-nat/python-octomap), adapted for ROS integration.

## License

`octomap_ros` is licensed under the BSD License. See the [LICENSE](LICENSE) file for details.
