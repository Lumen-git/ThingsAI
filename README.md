# ThingsAI
### Create dynamic mosaics using evolution

### Requirements
Most of the requirements come with python or will already be installed in most conda environments, however, all non-standard ones are listed below.
```
pillow
scipy
numpy
```

### Usage
1. Create a folder called "Things" and fill it with the images you want to use to create the target image
2. Run things2pickle.py to create an index of all the images. This can be run again to update the index at any time
3. Put the target image in the folder and give it the name "target.png"
4. Run thingsAI.py
### How to use config.json

### How it works

## To-Do

- [ ] Speed up image processing (right now 500x500 seems to be the effective limit)
- [ ] Color average mode: Select random spot and size, only select image from population with similar cover average. Possible new mutation point
    ^^ Would require color information to be preprocessed by image2pickle and stored in Thing object
- [ ] Menu system to change settings, launch program, index images...
