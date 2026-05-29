class Point3D:
    def __init__(self, x, y, z, data=None):
        self.x = x
        self.y = y
        self.z = z
        self.data = data

class BoundingBox:
    """Defines the 3D cube boundaries using a center point (cx, cy, cz) and half-dimension (size)."""
    def __init__(self, cx, cy, cz, size):
        self.cx = cx  # Center X
        self.cy = cy  # Center Y
        self.cz = cz  # Center Z
        self.size = size  # Half-width, half-height, half-depth

    def contains(self, point):
        """Checks if a Point3D is within the boundaries of this cube."""
        return (self.cx - self.size <= point.x <= self.cx + self.size and
                self.cy - self.size <= point.y <= self.cy + self.size and
                self.cz - self.size <= point.z <= self.cz + self.size)


class OctreeNode:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary    # A BoundingBox object
        self.capacity = capacity    # Maximum points a leaf node can hold before splitting
        self.points = []            # List to store Point3D objects in this node
        self.children = None        # List of 8 OctreeNode children once subdivided
        self.is_divided = False

    def subdivide(self):
        """Subdivides the current node into 8 smaller octant children."""
        new_size = self.boundary.size / 2
        cx, cy, cz = self.boundary.cx, self.boundary.cy, self.boundary.cz

        # Generate the 8 sub-cubes by combining the signs (+ / -) across the 3 axes
        self.children = [
            OctreeNode(BoundingBox(cx - new_size, cy - new_size, cz - new_size, new_size), self.capacity), # Bottom-Left-Front
            OctreeNode(BoundingBox(cx + new_size, cy - new_size, cz - new_size, new_size), self.capacity), # Bottom-Right-Front
            OctreeNode(BoundingBox(cx - new_size, cy + new_size, cz - new_size, new_size), self.capacity), # Top-Left-Front
            OctreeNode(BoundingBox(cx + new_size, cy + new_size, cz - new_size, new_size), self.capacity), # Top-Right-Front
            OctreeNode(BoundingBox(cx - new_size, cy - new_size, cz + new_size, new_size), self.capacity), # Bottom-Left-Back
            OctreeNode(BoundingBox(cx + new_size, cy - new_size, cz + new_size, new_size), self.capacity), # Bottom-Right-Back
            OctreeNode(BoundingBox(cx - new_size, cy + new_size, cz + new_size, new_size), self.capacity), # Top-Left-Back
            OctreeNode(BoundingBox(cx + new_size, cy + new_size, cz + new_size, new_size), self.capacity)  # Top-Right-Back
        ]
        self.is_divided = True

        # Redistribute the points from the parent node into the new children
        for p in self.points:
            for child in self.children:
                if child.insert(p):
                    break
        self.points = [] # Clear the parent point list as they are now held by children

    def insert(self, point):
        """Recursively inserts a point into the Octree."""
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity and not self.is_divided:
            self.points.append(point)
            return True

        if not self.is_divided:
            self.subdivide()

        # Try to insert the point into one of the 8 children
        for child in self.children:
            if child.insert(point):
                return True
        return False

    def search(self, point):
        """Searches for exact matching 3D coordinates. Returns True if found, False otherwise."""
        if not self.boundary.contains(point):
            return False

        if not self.is_divided:
            for p in self.points:
                if p.x == point.x and p.y == point.y and p.z == point.z:
                    return True
            return False

        # If divided, forward the search query recursively to the children nodes
        for child in self.children:
            if child.search(point):
                return True
        return False

    def delete(self, point):
        """Removes an exact matching point from the Octree and cleans up empty leaf nodes."""
        if not self.boundary.contains(point):
            return False

        if not self.is_divided:
            for i, p in enumerate(self.points):
                if p.x == point.x and p.y == point.y and p.z == point.z:
                    self.points.pop(i)
                    return True
            return False

        # Search and delete the target point within the children nodes
        deleted = False
        for child in self.children:
            if child.delete(point):
                deleted = True
                break

        # Optimization: Collapse children back into parent if total point count drops below capacity
        if deleted:
            total_points = 0
            all