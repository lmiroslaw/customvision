import os
import time 

#Prerequsitives
#pip install matplotlib, pillow
#pip install azure-cognitiveservices-vision-customvision

import matplotlib.pyplot as plt
import matplotlib.image as im
import numpy as np
from azure.cognitiveservices.vision.customvision.training import training_api
from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models

def create_project(trainer, name):
    # Create a new project
    print ("Creating project...")
    return trainer.create_project(name)
    
def create_tag(trainer, project, description):
    # Make two tags in the new project
    new_tag = trainer.create_tag(project.id, description)
    return new_tag

def show_image(path_to_dir, imgname):
    imgpath = os.path.join(path_to_dir,imgname)
    print(imgpath)
    img = im.imread(imgpath)    
    imgplot = plt.imshow(img)
    
def upload_images(trainer, project, path_to_images, tag):    
    for image in os.listdir(os.fsencode(path_to_images)):
        image_path=os.path.join(path_to_images,os.fsdecode(image))
        with open(image_path, mode="rb") as img_data: 
            trainer.create_images_from_data(project.id, img_data, [ tag.id ])
            print("Added: "+ image_path)

def run_training(trainer,project):
    print ("Training...")
    iteration = trainer.train_project(project.id)
    while (iteration.status != "Completed"):
        iteration = trainer.get_iteration(project.id, iteration.id)
        print ("Training status: " + iteration.status)
        time.sleep(1)
    trainer.update_iteration(project.id, iteration.id, is_default=True)
    print ("Done!")



# Loop through each subdirectory
def print_all(images_dir):
    for folder in sorted(os.listdir(images_dir)):
        # Get the subdirectory path and print it
        folderPath = os.path.join(images_dir,folder)
        print(folderPath, ':')
        # Loop through the files in the subdirectory, printing them
        for file in sorted(os.listdir(folderPath)):
            print('\t', file)

def do_stuff_on_import():
    pass

def main():
    #show_image(clean_dir,filename)
    clean_dir = 
    crack_dir = 
    

    training_key = 
    prediction_key = 

    trainer = training_api.TrainingApi(training_key)
    
    project = create_project(trainer, "Cracks Recognition")
    
    clean_tag = create_tag(trainer, project, "clean")
    crack_tag = create_tag(trainer, project, "cracked")
    
    upload_images(trainer,project, clean_dir,clean_tag)
    upload_images(trainer,project, crack_dir,crack_tag)
    
    run_training(trainer,project)


if __name__ == '__main__':
    main()
else:
    do_stuff_on_import()
