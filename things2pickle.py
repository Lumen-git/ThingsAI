import os
import pickle


def canThings():
    #By defult, /Thigns is where all the images are stored
    path = "./Things"
    files = os.listdir(path)
    #Create dictionary giving each item an ID
    all_things = {}
    i = 1
    for item in files:
        all_things[i] = "Things/" + item
        i += 1
    #save all_things to a pickle file
    #print(all_things)
    #input()
    with open('things.pickle', 'wb') as jar:
        pickle.dump(all_things, jar)


def main():
    canThings()


if __name__ == "__main__":
   main()
