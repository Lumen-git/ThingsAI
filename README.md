# ThingsAI
### Create dynamic mosaics using evolution

<img src="sample.gif" alt="The Mona Lisa recreated using textures from Minecraft"/>

###### The Mona Lisa Recreated using textures from Minecraft
<br>

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
config.json is used to change some of the optional settings in ThingsAI. Each option as well as their accepted settings are explained below.

- MinSizeMode - true/false - Enables the minsize mode. If enabled, images will be no smaller than a set percentage of the target
- MinSize - 0 to 1 decimal - The minimum size of each image if minsize mode is enabled. Expressed as decimal percentage of the target image
- Mutation rate - 0 to 1 decimal - The rate at which mutations occur
- Population size - integer - The size of the population
- SurvivalRate - 0 to 1 decimal - Percentage of the top of the population that will be kept
- GenerationCycles - integer - The number of cycles in each generation
- GIF - true/false - Enables the creation of a gif of the evolution with each frame being a new addition to the canvas. Use with caution as the process can be slowed down.

### How it works
Each generation begins by creating a population (defined in config,default 1000) and assigning them each a random position, rotation, and scale. At the start of the first cycle, each image is placed into a temporary canvas, then scored based on how much closer it gets the canvas to the target image. At the end of each cycle, the population is sorted based on score and the top percentage (defined in config) of the population is kept. This surviving population then generates mutated offspring. By default the top 25% survives and each then produces 3 offspring to generate the next 1000 item population. This repeats for a number of cycles (defined in config, default 10). At the end of the final cycle, the best image is permanently added to the canvas and the current canvas is saved as product.png. At any point product.png can be viewed and the process can be terminated. If GIF mode is enabled, each canvas will also be added to the end of the product.gif to generate an animation of the evolution process.

### To-Do

- [ ] Speed up image processing (right now 500x500 seems to be the effective limit)
- [ ] Color average mode: Select random spot and size, only select image from population with similar cover average. Possible new mutation point
    ^^ Would require color information to be preprocessed by image2pickle and stored in Thing object
- [ ] Menu system to change settings, launch program, index images...
