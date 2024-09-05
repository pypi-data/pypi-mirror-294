import unittest

import numpy as np

import octomap


class MocktomapMsg:
    def __init__(self):
        self.header = None
        self.binary = True
        self.id = 'OcTree'
        self.resolution = 0.1
        self.data = self.create_mock_data()
        
    def create_mock_data(self):
        # Create a simple 3x3x3 grid with some occupied cells
        grid = np.zeros((3, 3, 3), dtype=np.uint8)
        grid[1, 1, 1] = 1  # Center voxel occupied
        grid[0, 0, 0] = 1  # Corner voxel occupied
        return grid.tobytes()


class OctreeTestCase(unittest.TestCase):
    def setUp(self):
        self.tree = octomap.OcTree(0.1)

    def tearDown(self):
        pass

    def test_readBinary(self):
        self.assertTrue(self.tree.readBinary(b"test.bt"))
        self.assertFalse(self.tree.readBinary(b"test0.bt"))

    def test_writeBinary(self):
        self.assertTrue(self.tree.writeBinary(b"test1.bt"))

    def test_checkTree(self):
        self.tree.readBinary(b"test.bt")
        data = self.tree.write()
        tree2 = octomap.OcTree.read(data)
        self.assertEqual(tree2.write(), data)

    def test_checkBinary(self):
        self.tree.readBinary(b"test.bt")
        data = self.tree.writeBinary()
        tree2 = octomap.OcTree(0.1)
        tree2.readBinary(data)
        self.assertEqual(tree2.writeBinary(), data)

    def test_BBXMax(self):
        a = np.array((1.0, 2.0, 3.0))
        self.tree.setBBXMax(a)
        self.assertTrue(np.allclose(self.tree.getBBXMax(), a))

    def test_BBXMin(self):
        a = np.array((1.0, 2.0, 3.0))
        self.tree.setBBXMin(a)
        self.assertTrue(np.allclose(self.tree.getBBXMin(), a))

    def test_Resolution(self):
        r = 1.0
        self.tree.setResolution(r)
        self.assertAlmostEqual(self.tree.getResolution(), r)

    def test_Node(self):
        self.tree.insertPointCloud(
            np.array([[1.0, 0.0, 0.0]]), np.array([0.0, 0.0, 0.0])
        )
        node = self.tree.getRoot()
        self.assertAlmostEqual(node.getValue(), 0.847298, places=5)
        self.assertEqual(node.childExists(0), False)
        self.assertEqual(node.childExists(1), False)
        self.assertEqual(node.childExists(2), False)
        self.assertEqual(node.childExists(3), False)
        self.assertEqual(node.childExists(4), False)
        self.assertEqual(node.childExists(5), False)
        self.assertEqual(node.childExists(6), False)
        self.assertEqual(node.childExists(7), True)
        self.assertAlmostEqual(
            self.tree.getNodeChild(node, 7).getValue(), 0.847298, places=5
        )

    def test_Update(self):
        test_point1 = np.array([1.0, 2.0, 3.0])
        test_point2 = np.array([0.0, 0.0, 0.0])
        test_point3 = np.array([5.0, 5.0, 5.0])
        self.tree.insertPointCloud(
            np.array([test_point1]), np.array([0.0, 0.0, 0.0])
        )
        node1 = self.tree.search(test_point1)
        node2 = self.tree.search(test_point2)
        node3 = self.tree.search(test_point3)
        self.assertTrue(self.tree.isNodeOccupied(node1))
        self.assertFalse(self.tree.isNodeOccupied(node2))
        self.assertRaises(
            octomap.NullPointerException,
            lambda: self.tree.isNodeOccupied(node3),
        )

        self.tree.updateNode(test_point2, True)
        self.tree.updateInnerOccupancy()
        self.assertTrue(self.tree.isNodeOccupied(node2))

    def test_Iterator(self):
        self.tree.insertPointCloud(
            np.array(
                [
                    [1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0],
                    [-1.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0],
                ]
            ),
            np.array([0.0, 1.0, 0.0]),
        )
        nodes = [i for i in self.tree.begin_tree() if i.isLeaf()]
        leafs = [i for i in self.tree.begin_leafs()]
        leafs_bbx = [
            i
            for i in self.tree.begin_leafs_bbx(
                np.array([0.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0])
            )
        ]
        self.assertEqual(len(nodes), len(leafs))
        self.assertEqual(len(leafs_bbx), 2)

    def test_castRay(self):
        origin = np.array([0.0, 0.0, 0.0])
        direction = np.array([1.0, 0.0, 0.0])
        end = np.array([0.0, 0.0, 0.0])

        # miss
        hit = self.tree.castRay(
            origin=origin,
            direction=direction,
            end=end,
            ignoreUnknownCells=True,
        )
        self.assertFalse(hit)
        self.assertTrue(np.all(end == 0.0))

        self.tree.insertPointCloud(
            np.array(
                [
                    [1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0],
                    [-1.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0],
                ]
            ),
            np.array([0.0, 0.0, 0.0]),
        )

        # hit
        hit = self.tree.castRay(
            origin=origin,
            direction=direction,
            end=end,
            ignoreUnknownCells=True,
        )
        self.assertTrue(hit)
        self.assertTrue(np.allclose(end, [1.05, 0.05, 0.05]))

    def test_updateNodes(self):
        # test points
        test_point1 = np.array([1.0, 2.0, 3.0])
        test_point2 = np.array([0.0, 0.0, 0.0])
        test_point3 = np.array([5.0, 5.0, 5.0])

        # *not* present
        node1 = self.tree.search(test_point1)
        node2 = self.tree.search(test_point2)
        node3 = self.tree.search(test_point3)
        self.assertRaises(
            octomap.NullPointerException,
            lambda: self.tree.isNodeOccupied(node1),
        )
        self.assertRaises(
            octomap.NullPointerException,
            lambda: self.tree.isNodeOccupied(node2),
        )
        self.assertRaises(
            octomap.NullPointerException,
            lambda: self.tree.isNodeOccupied(node3),
        )

        # batch update w/ test points
        self.tree.updateNodes([test_point1, test_point2, test_point3], True)

        # occupied
        node1 = self.tree.search(test_point1)
        node2 = self.tree.search(test_point2)
        node3 = self.tree.search(test_point3)
        self.assertTrue(self.tree.isNodeOccupied(node1))
        self.assertTrue(self.tree.isNodeOccupied(node2))
        self.assertTrue(self.tree.isNodeOccupied(node3))

    def test_insertDiscretizedPointCloud(self):
        test_point1 = np.array([1.0, 2.0, 3.0])
        test_point2 = np.array([0.0, 0.0, 0.0])
        test_point3 = np.array([5.0, 5.0, 5.0])

        self.tree.insertPointCloud(
            np.array([test_point1]), np.array([0.0, 0.0, 0.0]), discretize=True
        )

        node1 = self.tree.search(test_point1)
        node2 = self.tree.search(test_point2)
        node3 = self.tree.search(test_point3)

        self.assertTrue(self.tree.isNodeOccupied(node1))
        self.assertFalse(self.tree.isNodeOccupied(node2))
        self.assertRaises(
            octomap.NullPointerException,
            lambda: self.tree.isNodeOccupied(node3),
        )
        
    def test_from_msg(self):
        mock_msg = MocktomapMsg()
        
        try:
            octree = octomap.OcTree.binaryMsgToMap(mock_msg.resolution, 
                                                mock_msg.id.encode('utf-8'), 
                                                mock_msg.binary, 
                                                mock_msg.data)
            self.assertIsNotNone(octree)
            self.assertEqual(octree.getResolution(), 0.1)
            
            # # Test occupied voxels
            # center_node = octree.search([0.1, 0.1, 0.1])
            # corner_node = octree.search([0.0, 0.0, 0.0])
            # empty_node = octree.search([0.2, 0.2, 0.2])

            # self.assertTrue(octree.isNodeOccupied(center_node))
            # self.assertTrue(octree.isNodeOccupied(corner_node))
            # self.assertFalse(octree.isNodeOccupied(empty_node))

            # Additional checks
            self.assertGreater(octree.getNumLeafNodes(), 0)
            self.assertGreater(octree.getTreeDepth(), 0)
            self.assertGreater(octree.size(), 0)

        except Exception as e:
            self.fail(f"Error creating OcTree from mock message: {e}")


if __name__ == "__main__":
    unittest.main()