import pickle
import os
import random
from PIL import Image
from thing import thing

def makePopulation(thingsDict, x_size, y_size):
    population = []
    #Generate a population of 1000 things
    for i in range(1001):
        #Choose a random image by its ID
        chosen = random.randint(1,len(thingsDict))
        #Generate a thing from the chosen image with random scale and 
        #offset to have selected position on the canvas be the center
        #of the thing
        scale = random.uniform(.5,1.5)
        x_position = random.randint(0,x_size)
        y_position = random.randint(0,y_size)
        population.append(thing(scale, x_position, y_position, x_size, y_size, thingsDict[chosen], chosen))
    return population

def main():
    #read things.json to a dictionary
    with open('things.pickle', 'rb') as jar:
        thingsDict = pickle.load(jar)
    #Open target image and make a new canvas of same size
    #then copy it as new_image
    #Evolution will happen on the canvas, and after each
    #cycle, the canvas will be copied to the new_image
    #new image is the final result
    target = Image.open("target.png")
    x_size = target.size[0]
    y_size = target.size[1]
    canvas = Image.new("RGB", (x_size, y_size))
    new_image = canvas.copy()
    population = makePopulation(thingsDict, x_size, y_size)
    print(population)

if __name__ == "__main__":
   main()