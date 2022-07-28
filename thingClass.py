from PIL import Image

#I know this file name/class name doesn't fit standard naming conventions, but when you're
#basing a project on the work "things", file names and variables get real messy real fast
class thing:
    """class with ID, scale, x_position, y_position, y_size, x_size, rotation, and file_path"""
    def __init__(self, scale, x_position, y_position, file_path, rotation, ID=0):
        self.ID = ID
        self.scale = scale
        self.y_size = Image.open(file_path).size[1]
        self.x_size = Image.open(file_path).size[0]
        self.file_path = file_path
        x_offset = int(self.x_size/2)
        y_offset = int(self.y_size/2)
        self.x_position = x_position - x_offset
        self.y_position = y_position - y_offset
        score = 0
        self.rotation = rotation

    def getPath(self):
        return self.file_path

    def getScale(self):
        return self.scale

    def getXPosition(self):
        return self.x_position 

    def getYPosition(self): 
        return self.y_position

    def getYOffset(self):
        return self.y_offset

    def getXOffset(self):
        return self.x_offset

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

    def getXPosition(self):
        return self.x_position
    
    def getYPosition(self):
        return self.y_position

    def getRotation(self):
        return self.rotation

    def __str__(self):
        return "ID: " + str(self.ID) + " scale: " + str(self.scale) + " x_position: " + str(self.x_position) + " y_position: " + str(self.y_position) + " y_size: " + str(self.y_size) + " x_size: " + str(self.x_size) + " file_path: " + str(self.file_path)
    
    def __repr__(self):
        return "ID: " + str(self.ID) + " scale: " + str(self.scale) + " x_position: " + str(self.x_position) + " y_position: " + str(self.y_position) + " y_size: " + str(self.y_size) + " x_size: " + str(self.x_size) + " file_path: " + str(self.file_path)
