class thing:
    """class with ID, scale, x_position, y_position, y_size, x_size, and filePath"""
    def __init__(self, scale, x_position, y_position, y_size, x_size, filePath, ID=0):
        self.ID = ID
        self.scale = scale
        self.y_size = y_size
        self.x_size = x_size
        self.filePath = filePath
        x_offset = int(x_size/2)
        y_offset = int(y_size/2)
        self.x_position = x_position - x_offset
        self.y_position = y_position - y_offset

    def getPath(self):
        return self.filePath

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

    def __str__(self):
        return "ID: " + str(self.ID) + " scale: " + str(self.scale) + " x_position: " + str(self.x_position) + " y_position: " + str(self.y_position) + " y_size: " + str(self.y_size) + " x_size: " + str(self.x_size) + " filePath: " + str(self.filePath)
    
    def __repr__(self):
        return "ID: " + str(self.ID) + " scale: " + str(self.scale) + " x_position: " + str(self.x_position) + " y_position: " + str(self.y_position) + " y_size: " + str(self.y_size) + " x_size: " + str(self.x_size) + " filePath: " + str(self.filePath)
