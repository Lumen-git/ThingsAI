import pickle
import random
from PIL import Image
from thingClass import thing
import math
from scipy.interpolate import interp1d
import numpy
from things2pickle import canThings
from copy import deepcopy

def makePopulation(thingsDict, main_x_size, main_y_size):
    print("Making population...")
    population = []
    #Generate a population of 1000 things
    for i in range(1000):
        #Choose a random image by its ID
        chosen = random.randint(1,len(thingsDict))
        #Generate a thing from the chosen image with random scale and
        #offset to have selected position on the canvas be the center
        #of the thing
        size_test = Image.open(thingsDict[chosen])
        #Scalar prevents the images from being too small
        #Paining pixel by pixel is cheating
        #The things are now based on 1/8 the size of the full image (based on x axis), then adjusted
        #to their unique item size
        #scalar = main_x_size / 8
        #scaler = scalar / size_test.size[0]
        scale = random.uniform(.6, 1.4)
        x_position = random.randint(0,main_x_size)
        y_position = random.randint(0,main_y_size)
        rotation = random.randint(0,360)
        population.append(thing(scale, x_position, y_position, thingsDict[chosen], rotation, chosen))
        size_test.close()
    return population

def getTotalDifferenceVisual(image1,image2):
    #Get the total difference between two images using euclidean distance formula, pixel by pixel
    ##SLOW AS ALL HELL THIS NEEDS TO BE MADE BETTER
    ##JUST USE THIS TO GENERATE A VISUAL OF THE IMAGE DIFFERENCES
    #Takes 41.2 seconds to compare two identical 1098 × 1028 images
    m = interp1d([0,442],[0,255])
    x_size=image1.size[0]
    y_size=image1.size[1]
    canvasTest = Image.new("RGB", (x_size, y_size))
    total = 0
    for x in range(image1.size[0]):
        for y in range(image1.size[1]):
            difference = math.sqrt((image1.getpixel((x,y))[0] - image2.getpixel((x,y))[0])**2 + (image1.getpixel((x,y))[1] - image2.getpixel((x,y))[1])**2 + (image1.getpixel((x,y))[2] - image2.getpixel((x,y))[2])**2)
            total += difference
            red = int(m(difference))
            green = 255 - red
            canvasTest.putpixel((x,y), (red,green,0))
    canvasTest.save("difference.png")
    print(total)

def getTotalDifferenceFunctional(image1,image2):
    #Get the total difference between two images using numpy
    #This is faster than the previous method by a long shot
    #Amazing how different packages and do the same thing with such different speeds
    #Takes .2 seconds to compare two identical 1098 × 1028 images
    #Convert the images to numpy arrays
    image1 = image1.convert("RGB")
    image2 = image2.convert("RGB")
    image1 = numpy.asarray(image1)
    image2 = numpy.asarray(image2)
    #Aparrently this does the euclidian difference formula
    differences = numpy.linalg.norm(image1 - image2)
    return differences

def mutate(parent_thing):
    #Mutate a thing by changing its scale, position, and rotation by 80% to 120%
    additions = []
    i = 0
    for i in range(3):
        thing_copy = deepcopy(parent_thing)
        thing_copy.scale = int(thing_copy.scale * random.uniform(.8,1.2))
        thing_copy.x_position = int(thing_copy.x_position * random.uniform(.8,1.2))
        thing_copy.y_position = int(thing_copy.y_position * random.uniform(.8,1.2))
        #All these checks prevent the images from going out of bounds/giving and argument pillow doesn't like
        if thing_copy.scale <= .1:
            thing_copy.scale = .1
        if thing_copy.x_position == 0:
            thing_copy.x_position = 1
        if thing_copy.y_position == 0:
            thing_copy.y_position = 1
        if thing_copy.x_position < 0:
            thing_copy.x_position = 0
        if thing_copy.y_position < 0:
            thing_copy.y_position = 0
        if thing_copy.x_size == 0:
            thing_copy.x_size = thing_copy.x_size
        if thing_copy.y_size == 0:
            thing_copy.y_size = thing_copy.y_size
        thing_copy.rotation = int(thing_copy.rotation * random.uniform(.8,1.2))
        additions.insert(i, thing_copy)
        i += 1
    return additions


def evolve():
    #read things.pickle to a dictionary
    with open('things.pickle', 'rb') as jar:
        things_dict = pickle.load(jar)
    #Open target image and make a new canvas of same size
    #then copy it as new_image
    #Evolution will happen on the a copy pf canvas, and after each
    #cycle, the canvas will be saved with the best change of that generation
    target = Image.open("target.png")
    target_x = target.size[0]
    target_y = target.size[1]
    canvas = Image.new("RGB", (target_x, target_y))
    previous_canvas = Image.new("RGB", (target_x, target_y))
    population = makePopulation(things_dict, target_x, target_y)

    #Evolution time!
    #Enclosed in a while true loop to keep evolving until the user stops the program
    #Each generation will run a population 10 times, and the best one will be added
    #To new_image
    #After each of the 10 loops, the top 25% will stay alive and mutate
    #Each loop of the while loop is one generation
    generation = 0
    print("Starting evolution...")
    while True:
        for i in range(10):
            print("Generation: " + str(generation) + " Loop: " + str(i))
            for trial_thing in population:
                canvas_copy = canvas.copy()
                thing_image = Image.open(trial_thing.getPath())
                thing_image = thing_image.convert("RGBA")
                new_x = int(thing_image.size[0]*trial_thing.scale)
                new_y = int(thing_image.size[1]*trial_thing.scale)
                #All these checks prevent the images from going out of bounds/giving and argument pillow doesn't like
                if new_x <= 0:
                    new_x = 1
                if new_y <= 0:
                    new_y = 1
                thing_image = thing_image.resize((new_x, new_y))
                thing_image = thing_image.rotate(trial_thing.rotation, expand=True)
                canvas_copy.paste(thing_image, (trial_thing.x_position, trial_thing.y_position), mask=thing_image)
                #Score is calculated by comparing the canvas_copy to the target image and the last canvas
                #Lower score is better (more similar to target)
                #How close it is to the target is more important, so it has a 1.3 weight
                #The closer the trial is to the last canvas, the less it will have its score reduced
                trial_thing.setScore((getTotalDifferenceFunctional(target, canvas_copy)*1.5)-(getTotalDifferenceFunctional(previous_canvas, canvas_copy)*.4))
                thing_image.close()
            #Sort the population by score
            population.sort(key=lambda x: x.getScore())
            #Take first 250 items of the population and save them in population
            population = population[:250]
            new_population = []
            for thing in population:
                child = mutate(thing)
                new_population.extend(child)
            population.extend(new_population)
        best_thing = population[0]
        thing_image = Image.open(best_thing.file_path)
        #thing_image_mask = thing_image.convert("RGBA")
        thing_image = thing_image.convert("RGBA")
        thing_image = thing_image.resize((int(thing_image.size[0]*best_thing.scale), int(thing_image.size[1]*best_thing.scale)))
        thing_image = thing_image.rotate(best_thing.rotation, expand=True)
        canvas.paste(thing_image, (best_thing.x_position, best_thing.y_position), mask=thing_image)
        canvas.save("product.png")
        previous_canvas = canvas.copy()
        thing_image.close()
        generation += 1
        population = []
        population = makePopulation(things_dict, target_x, target_y)





if __name__ == "__main__":
    evolve()
