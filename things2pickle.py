import os
import pickle


def canThings():
    #By defult, /Thigns is where all the images are stored
    path = "./Things"
    files = os.listdir(path)
    #Create dictionary giving each item an ID
    allThings = {}
    i = 1
    for item in files:
        allThings[i] = "/Things/" + item
        i += 1
    #save all_things to a json file
    print(allThings)
    input()
    with open('things.pickle', 'wb') as jar:
        pickle.dump(allThings, jar)


def main():
    canThings()


if __name__ == "__main__":
   main()
