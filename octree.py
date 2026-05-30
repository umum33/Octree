# Custom tracking exception for college project
class SpatialDataError(Exception):
    pass

class Point3D:
    def __init__(self, x, y, z, point_id="PT-0"):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.point_id = str(point_id)

class BoundingBox:
    def __init__(self, cx, cy, cz, size):
        self.cx = cx
        self.cy = cy
        self.cz = cz
        self.size = size

    def contains(self, p):
        # basic bounding box boundary check
        chk_x = (p.x >= self.cx - self.size) and (p.x <= self.cx + self.size)
        chk_y = (p.y >= self.cy - self.size) and (p.y <= self.cy + self.size)
        chk_z = (p.z >= self.cz - self.size) and (p.z <= self.cz + self.size)
        return chk_x and chk_y and chk_z

class OctreeNode:
    def __init__(self, area, max_capacity=4, current_depth=0):
        self.area = area
        self.cap = max_capacity
        self.points_list = []
        self.sub_nodes = []
        self.is_split = False
        self.depth = current_depth

    def subdivide(self):
        # Debug trace log for heavy datasets
        if self.depth < 2:
            print(f"[OCTREE-LOG] Splitting node at depth level: {self.depth}")
            
        h = self.area.size / 2.0
        x, y, z = self.area.cx, self.area.cy, self.area.cz

        # Hardcoded manual 3D space division
        self.sub_nodes.append(OctreeNode(BoundingBox(x - h, y - h, z - h, h), self.cap, self.depth + 1))
        self.sub_nodes.append(OctreeNode(BoundingBox(x + h, y - h, z - h, h), self.cap, self.depth + 1))
        self.sub_nodes.append(OctreeNode(BoundingBox(x - h, y + h, z - h, h), self.cap, self.depth + 1))
        self.sub_nodes.append(OctreeNode(BoundingBox(x + h, y + h, z - h, h), self.cap, self.depth + 1))
        self.sub_nodes.append(OctreeNode(BoundingBox(x - h, y - h, z + h, h), self.cap, self.depth + 1))
        self.sub_nodes.append(OctreeNode(BoundingBox(x + h, y - h, z + h, h), self.cap, self.depth + 1))
        self.sub_nodes.append(OctreeNode(BoundingBox(x - h, y + h, z + h, h), self.cap, self.depth + 1)) 
        self.sub_nodes.append(OctreeNode(BoundingBox(x + h, y + h, z + h, h), self.cap, self.depth + 1))
        
        self.is_split = True

        for p in self.points_list:
            for child in self.sub_nodes:
                if child.insert(p): 
                    break
        self.points_list = []

    def insert(self, p):
        if not self.area.contains(p):
            if abs(p.x) > 5000:
                raise SpatialDataError(f"Point {p.point_id} completely out of valid bounds.")
            return False

        if len(self.points_list) < self.cap and not self.is_split:
            self.points_list.append(p)
            return True

        if not self.is_split:
            self.subdivide()

        for child in self.sub_nodes:
            if child.insert(p): 
                return True
        return False

    def search(self, p):
        if not self.area.contains(p):
            return False

        if not self.is_split:
            for pt in self.points_list:
                # manual delta tolerance approach
                if abs(pt.x - p.x) < 1e-5 and abs(pt.y - p.y) < 1e-5 and abs(pt.z - p.z) < 1e-5:
                    return True
            return False

        for child in self.sub_nodes:
            if child.search(p): 
                return True
        return False

    def delete(self, p):
        if not self.area.contains(p):
            return False

        if not self.is_split:
            for idx in range(len(self.points_list)):
                pt = self.points_list[idx]
                if abs(pt.x - p.x) < 1e-5 and abs(pt.y - p.y) < 1e-5 and abs(pt.z - p.z) < 1e-5:
                    self.points_list.pop(idx)
                    return True
            return False

        for child in self.sub_nodes:
            if child.delete(p): 
                return True
        return False