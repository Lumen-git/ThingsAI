import os
import json


def main():
    #By defult, /Thigns is where all the images are stored
    path = "./Things"
    files = os.listdir(path)
    #Create dictionary giving each item an ID
    all_things = {}
    i = 0
    for item in files:
        all_things[i] = "/Things/" + item
        i += 1
    #save all_things to a json file
    with open('things.json', 'w') as fp:
        json.dump(all_things, fp, indent=4)
    

if __name__ == "__main__":
   main()
