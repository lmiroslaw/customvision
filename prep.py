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

def create_predictor(prediction_key):
    return prediction_endpoint.PredictionEndpoint(prediction_key)

def predict_single_image_report(predictor, projectid, path_to_images, filename_crack, filename_clean):    
    resultList={} #empty dictionary
    with open(filename_crack, 'w') as fcr, open(filename_clean, 'w') as fcl:
        for image in os.listdir(os.fsencode(path_to_images)):
            image_path=os.path.join(path_to_images,os.fsdecode(image))
            #print("Prediction for: " + filename, file=f)
            with open(image_path, mode="rb") as img_data: 
                results = predictor.predict_image(projectid, img_data)
                for prediction in results.predictions:
                    resultList[prediction.tag_name] = prediction.probability                    

                if resultList.get("clean street")>resultList.get("cracked street"):
                    print("Prediction for: " + image_path, file=fcl)
                    print(resultList,file=fcl)
                    #print("\t" + resultList.get("clean street") + ": {0:.2f}%".format(resultList.get("clean street") * 100), file=fcl)
                    #print("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100), file=fcl)
                else:
                    print("Prediction for: " + image_path, file=fcr)
                    print(resultList,file=fcr)
                    #print("Prediction for: " + image, file=fcr)
                    #print("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100), file=fcr)

        

def predict_single_image(predictor, projectid, path_to_images):    
    for image in os.listdir(os.fsencode(path_to_images)):
        image_path=os.path.join(path_to_images,os.fsdecode(image))
        print("Prediction for: " + image_path)
        with open(image_path, mode="rb") as img_data: 
            results = predictor.predict_image(projectid, img_data)
            for prediction in results.predictions:
                print ("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))

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
    #show_image(clean_dir,"5_3312_1.jpg")
    clean_dir = 
    crack_dir = 
    test_dir = 

    training_key = YOURKEY 
    prediction_key = YOURKEY 

    #trainer = training_api.TrainingApi(training_key)
    #pr = trainer.get_project("Cracks Recognition") 
    
    # project = create_project(trainer, "Cracks Recognition")
    
    # clean_tag = create_tag(trainer, project, "clean street")
    # crack_tag = create_tag(trainer, project, "cracked street")
    
    # upload_images(trainer,project, clean_dir,clean_tag)
    # upload_images(trainer,project, crack_dir,crack_tag)
    
    # run_training(trainer,project)

    #from Portal: ProjectID: 08aee8df-801d-48fc-ae8b-3512cc2b54f7
    predictor = create_predictor(prediction_key)  
    predict_single_image_report(predictor, "08aee8df-801d-48fc-ae8b-3512cc2b54f7", test_dir,"report_cracked.txt","report_clean.txt")
    #predict_single_image(predictor, "08aee8df-801d-48fc-ae8b-3512cc2b54f7", test_dir)

     



if __name__ == '__main__':
    main()
else:
    do_stuff_on_import()
