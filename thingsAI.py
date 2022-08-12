import pickle
import random
from PIL import Image, ImageSequence
from thingClass import thing
import math
from scipy.interpolate import interp1d
import numpy
from things2pickle import canThings
from copy import deepcopy
import json

def makePopulation(thingsDict, main_x_size, main_y_size, settings_bundle):
    print("Making population...")
    population = []
    #Generate a population of 1000 things
    for i in range(int(settings_bundle[2])):
        #Choose a random image by its ID
        chosen = random.randint(1,len(thingsDict))
        #Generate a thing from the chosen image with random scale and
        #offset to have selected position on the canvas be the center
        #of the thing
        if settings_bundle[0]:
            trial_image = Image.open(thingsDict[chosen])
            trial_x = trial_image.size[0]
            trial_y = trial_image.size[1]
            trial_image.close()
            smallest_scale = max(main_x_size*float(settings_bundle[1])/trial_x, main_y_size*float(settings_bundle[1])/trial_y)
            scale = random.uniform(smallest_scale, smallest_scale + 1.2)
        else:
            smallest_scale = .0005
            scale = random.uniform(.4,1.6)
        x_position = random.randint(0,main_x_size)
        y_position = random.randint(0,main_y_size)
        rotation = random.randint(0,360)
        population.append(thing(scale, x_position, y_position, thingsDict[chosen], rotation, smallest_scale, chosen))
    return population

def getTotalDifferenceVisual(image1,image2):
    #Get the total difference between two images using euclidean distance formula, pixel by pixel
    ##SLOW AS ALL HELL THIS NEEDS TO BE MADE BETTER
    ##JUST USE THIS TO GENERATE A VISUAL OF THE IMAGE DIFFERENCES
    ##206 times slower than getTotalDifferenceFunctional
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
    #Convert the images to numpy arrays
    #206 times faster than getTotalDifferenceVisual
    image1 = image1.convert("RGB")
    image2 = image2.convert("RGB")
    image1 = numpy.asarray(image1)
    image2 = numpy.asarray(image2)
    #Apparently this does the euclidean difference formula
    differences = numpy.linalg.norm(image1 - image2)
    return differences

def mutate(parent_thing, settings_bundle, rate):
    #Mutate a thing by changing its scale, position, and rotation by 80% to 120%
    thing_copy = deepcopy(parent_thing)
    #Mutations
    if random.uniform(0,1) <= rate: 
        thing_copy.scale = int(thing_copy.scale * random.uniform(.6,1.4))
    if random.uniform(0,1) <= rate:
        thing_copy.x_position = int(thing_copy.x_position * random.uniform(.8,1.2))
    if random.uniform(0,1) <= rate:
        thing_copy.y_position = int(thing_copy.y_position * random.uniform(.8,1.2))
    if random.uniform(0,1) <= rate:
        thing_copy.rotation = int(thing_copy.rotation * random.uniform(.8,1.2))
    #All these checks prevent the images from going out of bounds/giving and argument pillow doesn't like
    if thing_copy.x_position == 0:
        thing_copy.x_position = 1
    if thing_copy.y_position == 0:
        thing_copy.y_position = 1
    if thing_copy.x_position < 0:
        thing_copy.x_position = 0
    if thing_copy.y_position < 0:
        thing_copy.y_position = 0
    #If minimum scale is enabled, make sure the scale is at least the minimum scale
    if settings_bundle[0]:
        smallest_scale = thing_copy.smallest_scale
        if thing_copy.scale < smallest_scale:
            thing_copy.scale = smallest_scale
    #Make sure the scale doesn't make the image 0
    #This isn't a great solution, but it'll do for now
    if thing_copy.x_size*thing_copy.scale <= 0:
        thing_copy.scale = 1
    if thing_copy.y_size*thing_copy.scale <= 0:
        thing_copy.scale = 1
    return thing_copy


def evolve():
    #Load in settings
    with open('config.json') as configFile:
        settings = json.load(configFile)
    configFile.close()

    #read things.pickle to a dictionary
    with open('things.pickle', 'rb') as jar:
        things_dict = pickle.load(jar)
    
    #Save the settings in a way easy to reference
    population_settings = (settings["MinSizeMode"], settings["MinSize"], settings["PopulationSize"])
    mutation_settings = settings["MutationRate"]
    GIF_settings = settings["GIF"]

    #Open target image and make a new canvas of same size
    #then copy it as new_image
    #Evolution will happen on the a copy pf canvas, and after each
    #cycle, the canvas will be saved with the best change of that generation
    target = Image.open("target.png")
    target_x = target.size[0]
    target_y = target.size[1]
    canvas = Image.new("RGB", (target_x, target_y))
    population = makePopulation(things_dict, target_x, target_y, population_settings)
    high_score = getTotalDifferenceFunctional(target, canvas)

    if GIF_settings:
        gif = canvas.copy()
        gif.save("product.gif", save_all=True, duration=100, loop=0)
        gif.close()

    #Evolution time!
    #Enclosed in a while true loop to keep evolving until the user stops the program
    #Each generation will run a population 10 times, and the best one will be added
    #To new_image
    #After each of the 10 loops, the top 25% will stay alive and mutate
    #Each loop of the while loop is one generation
    generation = 0
    print("Starting evolution...")
    while True:
        for i in range(int(settings["GenerationCycles"])):
            print("Generation: " + str(generation) + " Cycle: " + str(i))
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
                trial_thing.setScore(getTotalDifferenceFunctional(target, canvas_copy))
                thing_image.close()
            #Sort the population by score
            population.sort(key=lambda x: x.getScore())
            #Take first percentage items of the population based on SurvivalRate and save them in population
            population = population[:int(len(population)*float(settings["SurvivalRate"]))]
            new_population = []
            for thing in population:
                #Certain values of SurvivalRate can cause the population to decrease in size
                #Its best to use a percentage where 1/SurvivalRate is a whole number
                for i in range(int(1/float(settings["SurvivalRate"]))-1):
                    child = mutate(thing, population_settings, mutation_settings)
                    new_population.append(child)
            population.extend(new_population)
        best_thing = population[0]
        #Only add image if it increased the overall score of the canvas
        #Somewhat breaks evolution, but prevents program
        #from constantly undoing progress
        #Using < because a lower score is better
        #Using -2000 to give the AI a little room to undo some progress
        #In order to make more overall
        if best_thing.getScore() - 2000 < high_score:
            high_score = best_thing.getScore()
            thing_image = Image.open(best_thing.file_path)
            #thing_image_mask = thing_image.convert("RGBA")
            thing_image = thing_image.convert("RGBA")
            paste_x_size = int(thing_image.size[0]*best_thing.scale)
            paste_y_size = int(thing_image.size[1]*best_thing.scale)
            #A bit of a quick fix to prevent pasting/resizing an image less than 0 size, but it'll work for now
            if paste_x_size > 0 and paste_y_size > 0:
                thing_image = thing_image.resize((paste_x_size, paste_y_size))
                thing_image = thing_image.rotate(best_thing.rotation, expand=True)
                canvas.paste(thing_image, (best_thing.x_position, best_thing.y_position), mask=thing_image)
                canvas.save("product.png")
                if GIF_settings:
                    gif = Image.open("product.gif")
                    frames = []
                    for frame in ImageSequence.Iterator(gif):
                        frames.append(frame)
                    frames.append(canvas)
                    gif.close()
                    frames[0].save('product.gif', save_all=True, append_images=frames[1:])
            thing_image.close()
            generation += 1
        else:
            generation += 1
        population = []
        population = makePopulation(things_dict, target_x, target_y, population_settings)

if __name__ == "__main__":
    evolve()
