import math
from matrix import *

class RenderTool:
    def __init__(self):
        self.projMatrix = [[1., 0., 0.],
                           [0., 1., 0.]]
    
    def deg2Rad(self, deg):
        # Converts degrees into radians
        return (deg * math.pi) / 180.

    def rad2Deg(self, rad):
        # Converts radians into degrees
        return (rad * 180.) / math.pi
    
    def dist2D(self, p1, p2):
        # calculates the euclidean distance between two 2D points
        dX = (p2[0]-p1[0])
        dY = (p2[1]-p1[1])

        return math.sqrt(dX*dX + dY*dY)
    
    def dist3D(self, p1, p2):
        # calculates the euclidean distance between two 2D points
        dX = (p2[0]-p1[0])
        dY = (p2[1]-p1[1])
        dZ = (p2[2]-p1[2])

        return math.sqrt(dX*dX + dY*dY + dZ*dZ)

    def rotate3DPoints(self, points3D, xDeg, yDeg, zDeg):
        # points3D: list of 3D points to be projected into 2D image
        # xAngle, yAngle, zAngle are in degrees

        xRad = self.deg2Rad(xDeg)
        yRad = self.deg2Rad(yDeg)
        zRad = self.deg2Rad(zDeg)

        rotX = [[1., 0., 0.],
                [0., math.cos(xRad), -math.sin(xRad)],
                [0., math.sin(xRad), math.cos(xRad)]]

        rotY = [[math.cos(yRad), 0., math.sin(yRad)],
                [0., 1., 0.],
                [-math.sin(yRad), 0., math.cos(yRad)]]

        rotZ = [[math.cos(zRad), -math.sin(zRad), 0.],
                [math.sin(zRad), math.cos(zRad), 0.],
                [0., 0., 1.]]

        rotated = matMul(rotZ, transpose(points3D))
        rotated = matMul(rotY, rotated)
        rotated = matMul(rotX, rotated)

        return transpose(rotated)
    
    def project3Dto2D(self, points3D, scale=1.):
        points2D = transpose(matMul(self.projMatrix, transpose(points3D)))
        return [[x*scale, y*scale] for x, y in points2D]
    
    def trans2D(self, points, u, v):
        return [[x+u, y+v] for x, y in points]

    def trans3D(self, points, u, v, w):
        return [[x+u, y+v, z+w] for x, y, z in points]

    def scale2D(self, points, scale):
        return [[x*scale, y*scale] for x, y in points]

    def scale3D(self, points, scale):
        return [[x*scale, y*scale, z*scale] for x, y, z in points]
