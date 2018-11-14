import os
import sys
import time 
import pickle

from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models

#filename in [] corresponds to results in {} position-wise
# returns: predictList{filename, resultList}
def get_prediction_images(predictor, projectid, path_to_images):        
    predictList={} #empty dictionary
    
    for image in os.listdir(os.fsencode(path_to_images)):
        resultList={} #empty dictionary

        image_name=os.fsdecode(image)
        image_path=os.path.join(path_to_images,image_name)
        if (os.path.isdir(image_path)):
            continue
        with open(image_path, mode="rb") as img_data: 
            results = predictor.predict_image(projectid, img_data)
            for prediction in results.predictions:
                resultList[prediction.tag_name] = prediction.probability    
        predictList[image_name]=resultList                
        print("Predition for ", image_name, " done.")
    return predictList

def get_final_predictions(myList):
    predictionList={}
    for imagename, resultList in myList.items():
        for tag,prob in resultList.items():
            maxprob=0
            winner={}
            if prob > maxprob:
                maxprob=prob
            winner[tag]=maxprob
        predictionList[imagename]=winner
    return predictionList

def save_results_report(predictor, projectid, resultList, filename_crack, filename_clean):    
    
    with open(filename_crack, 'w') as fcr, open(filename_clean, 'w') as fcl:
        for key, value in resultList.items():

                if resultList.get("clean street")>resultList.get("cracked street"):
                    #print("Prediction for: " + image_name, file=fcl)
                    print(resultList,file=fcl)
                    #print("Prediction for: " + image_name)
                    print(resultList)
                    #print("\t" + resultList.get("clean street") + ": {0:.2f}%".format(resultList.get("clean street") * 100), file=fcl)
                    #print("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100), file=fcl)
                else:
                    #print("Prediction for: " + image_name, file=fcr)
                    print(resultList,file=fcr)
                    #print("Prediction for: " + image_name)
                    print(resultList)
                    #print("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100), file=fcr)        

def predict_single_image(predictor, projectid, path_to_images):    
    for image in os.listdir(os.fsencode(path_to_images)):
        image_path=os.path.join(path_to_images,os.fsdecode(image))
        print("Prediction for: " + image_path)
        with open(image_path, mode="rb") as img_data: 
            results = predictor.predict_image(projectid, img_data)
            for prediction in results.predictions:
                print ("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))

def create_predictor(prediction_key):
    return prediction_endpoint.PredictionEndpoint(prediction_key)

def serialize(myList, dump_file_name):
    binary_file = open(dump_file_name,mode='wb')
    pickle.dumps(myList,binary_file)
    binary_file.close()

def deseliarize(dump_file_name):
    return pickle.load(dump_file_name)

def main(argv):
    prediction_key = 
    test_dir = 
    #From the customvision.ai portal
    projectid = 

    #from Portal: ProjectID: 08aee8df-801d-48fc-ae8b-3512cc2b54f7
    predictor = create_predictor(prediction_key) 
    predictList = get_prediction_images(predictor, projectid, test_dir) 
    
    #Not tested
    #serialize(predictList,'my_pickled_results.bin')
    #copy_predict_list = deseliarize('my_pickled_results.bin')

    finalList=get_final_predictions(predictList)
    save_results_report(predictor, projectid, finalList, "report_cracked.txt","report_clean.txt")
    

if __name__ == "__main__":
    main(sys.argv)
