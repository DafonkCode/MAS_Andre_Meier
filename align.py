####################################################################
####################################################################
# Imports                                                      
####################################################################
####################################################################
import BR_config
import pandas as pd
import sys
import cv2
import cv2.aruco as aruco
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import pypdfium2 as pdfium
import pickle
from tqdm import tqdm
from skimage.metrics import *
import tensorflow as tf
from tensorflow import keras
import seaborn as sns

####################################################################
####################################################################
# Paths / Settings                                                           
####################################################################
####################################################################

auftragsnummer = BR_config.auftragsnummer
sortmethod = BR_config.sortmethod
delete_folders = BR_config.delete_folders
importreference = BR_config.importreference
importalign = BR_config.importalign
savereference = BR_config.savereference
featureplot = BR_config.featureplot
alignplot = BR_config.alignplot
mainfunction = BR_config.mainfunction
sim_check = BR_config.sim_check
stats = BR_config.stats
save_align = BR_config.save_align
sim_plot = BR_config.sim_plot

#-------------------------------------------------------------------
# Paths                                            
#-------------------------------------------------------------------

input_REF_path = r'input_REF\Batch_Record_Lorem_Ipsum.pdf'
input_ALIGN_path = r'./input_ALIGN/'+str(BR_config.br_name)
output_REF_path = r"./output_REF/"
output_ALIGN_path = r"./output_ALIGN/"
REF_Features = r"./REF_Features/ref_pickle.txt"
model_path = r"./models/model.h5"
aligned_images_path = r"./aligned_images_sorted/"
reference_images_path = r"./reference_images_sorted/"
exportplotpath = r"./EXPORT/Plots/"
exportpath = r"./EXPORT/"
exportresultpath = r"./EXPORT/Results/"
exportlogpath = r"./EXPORT/Results/"
zippath = r"./ZIP/"
#-------------------------------------------------------------------
# Settings                                            
#-------------------------------------------------------------------

####################################################################
####################################################################
# Sorting                                                           
####################################################################
####################################################################
#Der Code definiert eine Funktion namens "sort_pages", die dann folgende Schritte ausführt:
# Erstellt eine neue Datei mit dem Namen "Log_Alignment_"+auftragsnummer+".txt", in der dann später Log-Informationen geschrieben werden.
# Setzt die Standardausgabe auf diese Datei, sodass alle print-Anweisungen von nun an in diese Datei geschrieben werden.
# Schreibt einige log-Informationen in die Datei, unter anderem, ob bestimmte Funktionen aktiviert oder deaktiviert sind.
# Startet eine Zeitmessung mit "time.time()".
# Falls delete_folders "True" ist, wird die Funktion "delete_ordner()" aufgerufen.
# In Abhängigkeit von sortmethod wird entweder "Sortmethod = Aruco" oder "Sortmethod = Neural Network" in die Log-Datei geschrieben.
# Falls importreference "True" ist, wird die Funktion "pdf_REF_import()" aufgerufen.
# Analog dazu werden die Funktionen "pdf_ALIGN_import()", "savefeatures()" und "main()" aufgerufen, falls die entsprechenden Variablen "True" sind.
# Falls featureplot oder alignplot "True" sind, wird "Reference Plotfunction active" bzw. "Alignment Plotfunction active" in die Log-Datei geschrieben.
# Falls sim_check "True" ist, wird die Funktion "similarity()" aufgerufen.
# Falls stats "True" ist, wird die Funktion "alignment_stats()" aufgerufen.
# Die Funktion "runtime_measure_main()" wird aufgerufen und die in Schritt 4 gestartete Zeitmessung wird beendet.
# Schließlich wird die Log-Datei geschlossen und die Standardausgabe wieder auf den Ursprung zurückgesetzt.

def sort_pages(customOutput):
    s = open("EXPORT/Logs/Log_Alignment_"+str(auftragsnummer)+".txt", 'w')
    customOutput.registerOutputFunction(s.write)
    sys.stdout = customOutput
    print("*******************************************************")
    print("Setting")
    print("-------------------------------------------------------")
    Start_Time_main = time.time() 
    if delete_folders == True:
        print("Delete Folders active")
        delete_ordner()
    else:
        print("Delete Folders deactivated")
    if sortmethod == "Aruco":
        print("Sortmethod = Aruco")
    else:
        print("Sortmethod = Neural Network")

    if importreference ==True:
        print("Reference import active")
        pdf_REF_import()
    else:
        print("Reference import deactivated")

    if importalign == True:
        print("Alignment scan import active")
        pdf_ALIGN_import()
    else:
        print("Alignment scan import deactivated")

    if savereference == True:
        print("Saving of features active")
        savefeatures()
    else:
        print("Saving of features deactivated")
        

    if featureplot == True:
        print("Reference Plotfunction active")
    else:
        print("Reference Plotfunction deactivated")

    if alignplot == True:
        print("Alignment Plotfunction active")
    else:
        print("Alignment Plotfunction deactivated")

    if mainfunction == True:
        print("Alignment procedure active")
        main()
    else:
        print("Alignment procedure deactivated")

    if sim_check == True:
        print("Similarity check active")
        similarity()
    else:
        print("Similarity Check deactivated")

    if stats == True:
        print("Statistics of alignment active")
        alignment_stats()
    else:
        print("Statistics of alignment deactivated")
    
    runtime_measure_main(Start_Time_main)
    print("----------------------DONE-----------------------------")
    customOutput.unregisterOutputFunction(s.write)
    s.close()
####################################################################
####################################################################
# PDF IMPORT ALIGN                                                   
####################################################################
####################################################################
# Die Funktion "pdf_ALIGN_import()" liest PDF-Dateien aus dem angegebenen Pfad "input_ALIGN_path" ein und wandelt sie in Bilder um. 
# Die Bilder werden dann im Pfad "output_ALIGN_path" gespeichert und benennen sich "ALIGN_out_001.jpg", "ALIGN_out_002.jpg", etc. 
# Die Funktion misst außerdem die benötigte Zeit für den Import-Vorgang.
def pdf_ALIGN_import():
    print("*******************************************************")
    print("Alignment PDF Import")
    print("-------------------------------------------------------")
    Start_Time = time.time() 

    for dirname, _, filenames in os.walk(input_ALIGN_path):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    pdf = pdfium.PdfDocument(input_ALIGN_path)
    version = pdf.get_version()  # PDF Standard Version
    n_pages = len(pdf)  # Seitenzahl herausfinden

    page_indices = [i for i in range(n_pages)]  # Alle Seiten
    renderer = pdf.render_to(
        pdfium.BitmapConv.pil_image,
        page_indices = page_indices,
        scale = 300/72,  # 300dpi Auflösung
    )
    for i, image in zip(page_indices, renderer):
        image.save(output_ALIGN_path + "/ALIGN_out_%0*d.jpg" % (3, 1+i))
    runtime_measure(Start_Time)
    
    print("----------------------DONE-----------------------------")

####################################################################
####################################################################
# PDF IMPORT REF                                                 
####################################################################
####################################################################
# Die Funktion "pdf_REF_import()" liest PDF-Dateien aus dem angegebenen Pfad "input_REF_path" ein und wandelt sie in Bilder um. 
# Die Bilder werden dann im Pfad "output_REF_path" und "reference_images_path" gespeichert und benennen sich 
# "REF_out_001.jpg", "REF_out_002.jpg", etc. Die Funktion misst außerdem die benötigte Zeit für den Import-Vorgang.
def pdf_REF_import():
    print("*******************************************************")
    print("Reference PDF Import")
    print("-------------------------------------------------------")
    Start_Time = time.time()

    for dirname, _, filenames in os.walk(input_REF_path):
        for filename in filenames:
            print(os.path.join(dirname, filename))
    pdf = pdfium.PdfDocument(input_REF_path)
    version = pdf.get_version()  # PDF Standard Version
    n_pages = len(pdf)  # Seitenzahl herausfinden
    page_indices = [i for i in range(n_pages)]  # Alle Seiten
    renderer = pdf.render_to(
        pdfium.BitmapConv.pil_image,
        page_indices = page_indices,
        scale = 300/72,  # 300dpi Auflösung
    )
    for i, image in zip(page_indices, renderer):
        image.save(output_REF_path + "REF_out_%0*d.jpg" % (3, 1+i))
        image.save(reference_images_path + "%0*d.jpg" % (1, 1+i))
    runtime_measure(Start_Time)
    print("----------------------DONE-----------------------------")

####################################################################
####################################################################
# Modell importieren                                               
####################################################################
####################################################################
# Die Funktion "load_model_back()" lädt ein zuvor gespeichertes Keras-Modell aus dem Pfad 
# "model_path" und übersetzt es zur späteren Verwendung. Das Modell wird dann zurückgegeben.
def load_model_back():
    print("*******************************************************")
    print("Load Model Back in enviroment")
    print("-------------------------------------------------------")
    model = keras.models.load_model(model_path)
    model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    print("Model loaded successfully")
    print("----------------------DONE-----------------------------")
    return model
    

####################################################################
####################################################################
# Modell testem                                       
####################################################################
####################################################################
# Die Funktion "model_test(model)" testet das übergebene Modell anhand von Bildern, die im Pfad "output_REF_path" gespeichert sind. Für jedes Bild wird folgendes gemacht:
# Das Bild wird geladen und auf die Größe (200, 200) verkleinert.
# Das Bild wird in ein NumPy-Array umgewandelt.
# Das Array wird um eine Achse erweitert (um das Modell damit nutzen zu können).
# Das Modell wird auf das Array angewendet und es wird ein Ergebnis vorhergesagt.
# Die Position des höchsten Werts im Ergebnis-Array wird bestimmt und ausgegeben.
def model_test(model):
    print("*******************************************************")
    print("Test Model")
    print("-------------------------------------------------------")
    for dirname, _, filenames in os.walk(output_REF_path):
        for filename in tqdm(filenames, total = len(filenames), leave= False):
            full_REF_path = os.path.join(dirname, filename)
            print(full_REF_path)
            test_image = tf.keras.utils.load_img(full_REF_path, target_size = (200, 200)) 
            test_image = tf.keras.utils.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis = 0)
            # Vorhersage
            result = model.predict(test_image)
            position = np.argmax(result)
            print(result)
            print(position)
            #return result
    print("----------------------DONE-----------------------------")


####################################################################
####################################################################
# Modell sort loop                                       
####################################################################
####################################################################
# Die Funktion "model_sort_loop(model, full_ALIGN_path)" nimmt ein Modell und den Pfad eines Bildes als Eingaben und 
# sortiert das Bild entsprechend der Vorhersage des Modells. Folgende Schritte werden dafür ausgeführt:
# Das Bild wird geladen und auf die Größe (200, 200) verkleinert.
# Das Bild wird in ein NumPy-Array umgewandelt.
# Das Array wird um eine Achse erweitert (um das Modell damit nutzen zu können).
# Das Modell wird auf das Array angewendet und es wird ein Ergebnis vorhergesagt.
# Die Position des höchsten Werts im Ergebnis-Array wird bestimmt und als Ergebnis zurückgegeben.
def model_sort_loop(model, full_ALIGN_path):
    print("*******************************************************")
    print("Sort Pages with Neural Network")
    print("-------------------------------------------------------")
    print("Check File: " + full_ALIGN_path)
    test_image = tf.keras.utils.load_img(full_ALIGN_path, target_size = (200, 200)) 
    test_image = tf.keras.utils.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    #predict the result
    result = model.predict(test_image)
    position = np.argmax(result)
    print("Assigned Page: " +str(position+ 1))
    print("----------------------DONE-----------------------------")
    return position

####################################################################
####################################################################
# Aruco Sort                                       
####################################################################
####################################################################
# Die Funktion sortiert ein Bild mit Hilfe von Aruco-Codes. Sie nimmt das Bild (ALIGN_img), den Pfad des Bildes (full_ALIGN_path) 
# und optional die Größe der Marker (marker_size), die Anzahl der Marker (total_markers) und ob die Marker im Bild 
# gezeichnet werden sollen (draw) als Eingaben. Folgende Schritte werden durchgeführt:
# Das Bild wird in Graustufen umgewandelt.
# Ein Aruco-Dictionary mit der angegebenen Größe und Anzahl der Marker wird erstellt.
# Die Marker werden im Bild gesucht.
# Der erste gefundene Marker wird ausgegeben und als Ergebnis zurückgegeben.

def aruco_sort(ALIGN_img, full_ALIGN_path, marker_size = 4, total_markers = 250, draw = True):
    print("*******************************************************")
    print("Sort Pages with Aruco Code")
    print("-------------------------------------------------------")
    gray = cv2.cvtColor(ALIGN_img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{marker_size}X{marker_size}_{total_markers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bbox, ids,_ = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    print("Check File: " + full_ALIGN_path)
    print("Assigned Page: " + str(ids[0][0]+1))
    position = ids[0][0]
    print("----------------------DONE-----------------------------")
    return position


####################################################################
####################################################################
# Save features from REF                                  
####################################################################
####################################################################
# Die Funktion "savefeatures()" extrahiert Merkmale (Features) von Bildern im Pfad "output_REF_path" und speichert 
# sie in einem Dictionary (featurearray). Die Bilder werden zunächst aufbereitet und dann mit dem SIFT-Algorithmus 
# (Scale Invariant Feature Transform) analysiert. Die gefundenen Merkmale werden im Dictionary abgespeichert und das
# Dictionary wird dann als Pickle-Datei gespeichert. Optional werden die Bilder angezeigt und gespeichert.
def savefeatures():
    print("*******************************************************")
    print("Save Features from Reference")
    print("-------------------------------------------------------")
    Start_Time = time.time()
    featurearray = {}
    featureindex = 0

    for dirname, _, filenames in os.walk(output_REF_path):
        for filename in tqdm(filenames, total = len(filenames), leave= False):
            full_REF_path = os.path.join(dirname, filename)
            global img_Ref_path
            img_Ref_path = full_REF_path
            #print(os.path.join(dirname, filename))
            print("Check File: ", full_REF_path)
            
            img1 = cv2.imread(full_REF_path, cv2.IMREAD_COLOR)
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            if featureplot == True:
                fig= plt.figure(figsize=(10, 7))
                ax1 = fig.add_subplot(1, 2, 1)
                ax1.axis("off")
                ax1.imshow(img1); plt.title("REF Original "+ filename)
            image_preprocessing_REF()
            sift = cv2.SIFT_create()
            keypoints1, descriptors1 = sift.detectAndCompute(img_REF_processed, None)
            img1_display = cv2.drawKeypoints(img_REF_processed, keypoints1, outImage=np.array([]), color =(255, 0, 0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  
            if featureplot == True:
                ax2 = fig.add_subplot(1, 2, 2)
                ax2.axis("off")
                ax2.imshow(img1_display); plt.title("REF preprocessed: "+ filename)
                plt.show()
                plt.savefig("EXPORT/Plots/Reference_"+str(auftragsnummer)+"_"+str(filename)+".png")
            else:
                print("Reference Plots turned OFF")
            height, width, channels = img_REF_processed.shape
            featurearray[featureindex] = {}
            featurearray[featureindex]["keypoints"] = [{"pt":k.pt, "angle" : k.angle, "response":k.response, "class_id":k.class_id, "octave": k.octave, "pt": k.pt, "size":k.size} for k in keypoints1]
            featurearray[featureindex]["descriptor"] = descriptors1
            featurearray[featureindex]["channels"] =  channels
            featurearray[featureindex]["height"] =  height
            featurearray[featureindex]["width"] =  width
            featureindex += 1

    pickle.dump(featurearray,open(REF_Features, "wb"))
    runtime_measure(Start_Time)
    print("----------------------DONE-----------------------------")


####################################################################
####################################################################
# Image Preprocessing REF                                     
####################################################################
####################################################################
# Diese Funktion führt eine Vorverarbeitung von Bildern durch, die als Referenzen genutzt werden sollen. 
# Dabei wird das Bild zunächst in Graustufen umgewandelt, anschließend werden einige Filter angewendet, 
# um den Kontrast zu erhöhen. Außerdem wird eine Harris-Eckenerkennung durchgeführt und das Bild wird wieder 
# in Farbe umgewandelt. Am Ende wird das verarbeitete Bild in einer globalen Variable gespeichert.
def image_preprocessing_REF():
    print("*******************************************************")
    print("Run Image preprocessing Reference")
    print("-------------------------------------------------------")
    img_pre = cv2.imread(img_Ref_path, cv2.IMREAD_COLOR)
    img_pre = cv2.cvtColor(img_pre, cv2.COLOR_BGR2GRAY)
    height1, width1= img_pre.shape
    #img_pre[0:300, :] = (255)
    #img_pre[height1-200:height1, :] = (255)
    kernel_3x3 = np.ones((3, 3), np.float32) / 9      

    # kernel_size = 3
    # ret,thresh = cv2.threshold(img_pre,200,255,cv2.THRESH_BINARY)  
    # #finding contours 
    # cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # img_pre =cv2.cvtColor(img_pre,cv2.COLOR_GRAY2RGB)
    # img_pre = cv2.cvtColor(img_pre, cv2.COLOR_BGR2RGB)
    # #drawing Contours
    # radius =1
    # color = (0,255,120)
    # img_pre= cv2.drawContours(img_pre, cnts, -1,color , radius)

    img_pre = cv2.filter2D(img_pre, -1, kernel_3x3)
    img_pre = cv2.adaptiveThreshold(img_pre, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    img_pre = cv2.dilate(img_pre, kernel, iterations=1)    
    img_pre = cv2.bitwise_not(img_pre)
    img_pre =cv2.cvtColor(img_pre,cv2.COLOR_GRAY2RGB)
    img_pre = cv2.cvtColor(img_pre, cv2.COLOR_BGR2RGB)
    gray= cv2.cvtColor(img_pre, cv2.COLOR_BGR2GRAY)
    gray= np.float32(gray)
    harris_corners= cv2.cornerHarris(gray, 3, 3, 0.05)
    kernel= np.ones((3,3), np.uint8)
    harris_corners= cv2.dilate(harris_corners, kernel, iterations= 1)
    img_pre[harris_corners > 0.025 * harris_corners.max()]= [255,127,127]
    global img_REF_processed
    img_REF_processed = img_pre
    print("----------------------DONE-----------------------------")


####################################################################
####################################################################
# Image Preprocessing ALIGN                                   
####################################################################
####################################################################
def image_preprocessing_ALIGN():
    print("*******************************************************")
    print("Run Image preprocessing Align")
    print("-------------------------------------------------------")
    img_pre_a = cv2.imread(img_ALIGN_path, cv2.IMREAD_COLOR)
    img_pre_a = cv2.cvtColor(img_pre_a, cv2.COLOR_BGR2GRAY)
    height1, width1= img_pre_a.shape
    #img_pre_a[0:300, :] = (255)
    #img_pre_a[height1-200:height1, :] = (255)
    kernel_3x3 = np.ones((3, 3), np.float32) / 9

    # kernel_size = 3
    # ret,thresh = cv2.threshold(img_pre_a,200,255,cv2.THRESH_BINARY)  
    # #finding contours 
    # cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # img_pre_a =cv2.cvtColor(img_pre_a,cv2.COLOR_GRAY2RGB)
    # img_pre_a = cv2.cvtColor(img_pre_a, cv2.COLOR_BGR2RGB)
    # #drawing Contours
    # radius =1
    # color = (0,255,120)
    # img_pre_a= cv2.drawContours(img_pre_a, cnts, -1,color , radius)

    img_pre_a = cv2.filter2D(img_pre_a, -1, kernel_3x3)
    img_pre_a = cv2.adaptiveThreshold(img_pre_a, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    img_pre_a = cv2.dilate(img_pre_a, kernel, iterations=1)    
    img_pre_a = cv2.bitwise_not(img_pre_a)
    img_pre_a =cv2.cvtColor(img_pre_a,cv2.COLOR_GRAY2RGB)
    img_pre_a = cv2.cvtColor(img_pre_a, cv2.COLOR_BGR2RGB)
    gray= cv2.cvtColor(img_pre_a, cv2.COLOR_BGR2GRAY)
    gray= np.float32(gray)
    harris_corners= cv2.cornerHarris(gray, 3, 3, 0.05)
    kernel= np.ones((3,3), np.uint8)
    harris_corners= cv2.dilate(harris_corners, kernel, iterations= 1)
    img_pre_a[harris_corners > 0.025 * harris_corners.max()]= [255,127,127]
    global img_ALIGN_processed
    img_ALIGN_processed = img_pre_a
    print("----------------------DONE-----------------------------")

####################################################################
####################################################################
# Main Function                                                    
####################################################################
####################################################################
def main():
    Start_Time = time.time()  
    featurearray = pickle.load(open(REF_Features, "rb"))
    balance = filebalance()
    if balance == False:
        print("*******************************************************")
        print("*******************************************************")
        print("*******************************************************")
        print("------------!!! File unbalance detected !!!------------")
        print("-----------------Check the Settings--------------------")
        print("*******************************************************")
        print("*******************************************************")
        print("*******************************************************")
        sys.exit()
    else:
        print("Files balanced")
        print("----------------------DONE-----------------------------")
        print("*******************************************************")
        print("Run MAIN procedure")
        print("-------------------------------------------------------")
        print("Sortmethod: "+sortmethod)
        for key in featurearray:
            featurearray[key]["keypoints"] = [cv2.KeyPoint(k["pt"][0], k["pt"][1], k["size"], k["angle"], k["response"], k["octave"], k["class_id"])for k in featurearray[key]["keypoints"]]
        for dirname, _, filenames in os.walk(output_ALIGN_path):
            for filename in filenames:
                full_ALIGN_path = os.path.join(dirname, filename)
                global img_ALIGN_path
                img_ALIGN_path = full_ALIGN_path
                if sortmethod == "Neural":
                    model = load_model_back()
                    position = model_sort_loop(model, full_ALIGN_path)
                    ALIGN_img = cv2.imread(full_ALIGN_path, cv2.IMREAD_COLOR)
                    ALIGN_img = cv2.cvtColor(ALIGN_img, cv2.COLOR_BGR2RGB)
                else:
                    ALIGN_img = cv2.imread(full_ALIGN_path, cv2.IMREAD_COLOR)
                    ALIGN_img = cv2.cvtColor(ALIGN_img, cv2.COLOR_BGR2RGB)
                    position = aruco_sort(ALIGN_img, full_ALIGN_path)
                image_preprocessing_ALIGN()
                if alignplot == True:
                    fig= plt.figure(figsize=(15, 7))
                    ax1 = fig.add_subplot(1, 3, 1)
                    ax1.axis("off")
                    ax1.imshow(ALIGN_img); plt.title("ALIGN Image:" + filename)
                sift = cv2.SIFT_create()
                keypoints2, descriptors2 = sift.detectAndCompute(img_ALIGN_processed, None)
                ALIGN_img_display = cv2.drawKeypoints(img_ALIGN_processed, keypoints2, outImage=np.array([]), color =(255, 0, 0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                if alignplot == True:
                    ax2 = fig.add_subplot(1, 3, 2)
                    ax2.axis("off")
                    ax2.imshow(ALIGN_img_display); plt.title("ALIGN preprocessed: " +filename )
    #-------------------------------------------------------------------
    # Keypoints und Matcher                                            
    #-------------------------------------------------------------------
                FLANN_INDEX_KDTREE = 1
                index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 3)
                search_params = dict(checks=30)   # or pass empty dictionar
                matcher = cv2.FlannBasedMatcher(index_params,search_params)
                matches = list(matcher.knnMatch(featurearray[position]["descriptor"], descriptors2, k =2))
                right_page = []
                for i,(m,n) in enumerate(matches):
                    if m.distance < 0.4*n.distance:
                        right_page.append(m)
                points1 = np.zeros((len(right_page), 2), dtype =np.float32)
                points2 = np.zeros((len(right_page), 2), dtype =np.float32)

                for i, match in enumerate(right_page):
                    points1[i, :] = featurearray[position]["keypoints"][match.queryIdx].pt
                    points2[i, :] = keypoints2[match.trainIdx].pt

    #-------------------------------------------------------------------
    # Homography                                        
    #-------------------------------------------------------------------
                h, mask = cv2.findHomography(points2, points1, cv2.RANSAC)
                ALIGN_img_reg = cv2.warpPerspective(ALIGN_img, h, (featurearray[position]["width"], featurearray[position]["height"]), borderMode = cv2.BORDER_CONSTANT, borderValue=(255,255,255))
                if alignplot == True:
                    ax3 = fig.add_subplot(1, 3, 3)
                    ax3.axis("off")
                    ax3.imshow(ALIGN_img_reg); plt.title("Scan alignment DONE " +filename)
                    plt.show()
                    plt.savefig("EXPORT/Plots/Align_"+str(auftragsnummer)+str(filename)+".png")
                else:
                    print("Alignment Plots turned OFF")
                if save_align == True:
                    ALIGN_img_reg = cv2.cvtColor(ALIGN_img_reg, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(str(aligned_images_path)+str(position + 1)+".jpg", ALIGN_img_reg)
                    print("Aligned Image saved to folder")
        runtime_measure(Start_Time)
        print("----------------------DONE-----------------------------")


####################################################################
####################################################################
# Runtime Measure                                           
####################################################################
####################################################################

def runtime_measure(Start_Time):    
    End_Time = time.time()
    Zeit = End_Time - Start_Time
    print("Runtime = " + str(round(Zeit,2)) + " Seconds")

def runtime_measure_main(Start_Time_main):    
    End_Time_main = time.time()
    Zeit = End_Time_main - Start_Time_main
    print("Runtime main Process = " + str(round(Zeit,2)) + " Seconds")

####################################################################
####################################################################
# Delete Folders                                               
####################################################################
####################################################################
def delete_ordner():
    print("*******************************************************")
    print("Delete Folders")
    print("-------------------------------------------------------")
    dir = output_REF_path
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    dir = output_ALIGN_path
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    dir = aligned_images_path
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    dir = reference_images_path
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    dir = exportplotpath
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    dir = exportresultpath
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    dir = exportlogpath
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    dir = zippath
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    print("----------------------DONE-----------------------------")

####################################################################
####################################################################
# Alignment Stats                                               
####################################################################
####################################################################
def alignment_stats():
    print("*******************************************************")
    print("Summary of alignment")
    print("-------------------------------------------------------")
    df_stats = pd.read_csv(str(exportresultpath)+"Alignscores.csv", sep = ",")
    df_stats.count()
    df_sorted = df_stats.sort_values(by=['Score'])
    print("Number of checked Pages: " +str(df_stats["Filename"].count()))
    print("Best alignment score: " +str(round(df_stats["Score"].max(),5)))
    print("Minimum alignment score: " +str(round(df_stats["Score"].min(),5)))
    print("Mean alignment score: " +str(round(df_stats["Score"].mean(),5)))
    fig, ax = plt.subplots(1, 2, figsize=(15, 7))
    sns.histplot(ax = ax[0], data = df_stats, x = "Score", color = "steelblue", bins = 10, kde=True, label="Score")
    ax[0].set_title("Histogram Similarity of Alignment")
    ax[0].set(xlabel='Similarity-Score', ylabel='count')
    ax[1].set_title("Scatterplot Similarity of Alignment")
    ax[1].set(xlabel='Filename', ylabel='Score')
    ax[1].tick_params(axis='x', rotation=45)
    sns.scatterplot(ax=ax[1],data=df_stats, x="Filename", y = "Score", color = "purple", size="Score", hue= "Score")

    print("----------------------DONE-----------------------------")


####################################################################
####################################################################
# Check balance                          
####################################################################
####################################################################

def filebalance():
    print("*******************************************************")
    print("Check filebalance")
    print("-------------------------------------------------------")
    x = 0
    i = 0
    for dirname, _, filenames in os.walk(output_REF_path):
        for filename in filenames:
            n_ref = i
            i += 1
        print("Reference Files: "+str(n_ref))

    for dirname, _, filenames in os.walk(output_ALIGN_path):
        for filename in filenames:
            n_align = x
            x += 1
        print("Align Files: " +str(n_align))
    
    if n_ref == n_align:
        page_balance = True
        print("Files balanced")
    else: 
        page_balance = False
        print("Files unbalanced")
    return page_balance

    

####################################################################
####################################################################
# Check similarity Original Image                                     
####################################################################
####################################################################
def similarity():
    print("*******************************************************")
    print("Check similarity")
    print("-------------------------------------------------------")
    df_simscore = pd.DataFrame(columns = ["Filename", "Score", "Perc"])
    for dirname, _, filenames in os.walk(reference_images_path):
        for filename in filenames:
            REF_sim_path = os.path.join(dirname, filename) 
            before = cv2.imread(REF_sim_path)
            before = cv2.cvtColor(before, cv2.COLOR_BGR2RGB)
            before_gray = cv2.imread(REF_sim_path, cv2.IMREAD_GRAYSCALE)
            height = before_gray.shape[1]
            width = before_gray.shape[0]
            dim = height, width
            ALIGN_sim_path = os.path.join(aligned_images_path, filename)
            df_filename = filename
            after = cv2.imread(ALIGN_sim_path)
            after = cv2.cvtColor(after, cv2.COLOR_BGR2RGB)
            after_gray = cv2.imread(ALIGN_sim_path, cv2.IMREAD_GRAYSCALE)
            after_gray = cv2.resize(after_gray, dim, interpolation = cv2.INTER_AREA)
            after = cv2.resize(after, dim, interpolation = cv2.INTER_AREA)

            (score, diff) = structural_similarity(before_gray, after_gray, full = True)
            df_score = score
            perc = score * 100
            df_perc = perc
            
            diff = (diff * 255).astype("uint8")

            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]

            mask = np.zeros(before.shape, dtype='uint8')
            filled_after = after.copy()
            print("-------------------------------------------------------")
            print("Filename: "+ str(filename))
            print("-------------------------------------------------------")
            print("Similarity in %: " + str(round(perc,3)) + "%")
            print("Similarity Score: " +str(df_score))
            df_simscore = df_simscore.append({"Filename" : df_filename, "Score":df_score, "Perc":df_perc}, ignore_index = True)

            for c in contours:
                area = cv2.contourArea(c)
                if area > 10:
                    x,y,w,h = cv2.boundingRect(c)
                    cv2.rectangle(before, (x, y), (x + w, y + h), (255,0,255), 2)
                    cv2.rectangle(after, (x, y), (x + w, y + h), (0,255,12), 2)
                    cv2.drawContours(mask, [c], 0, (0,255,0), -1)
                    cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)
                    

            if sim_plot == True:
                fig= plt.figure(figsize=(20, 10))
                ax1 = fig.add_subplot(1, 3, 1)
                ax1.axis("off")
                ax1.imshow(before); plt.title("before")
                ax2 = fig.add_subplot(1, 3, 2)
                ax2.axis("off")
                ax2.imshow(after); plt.title("after")
                ax3 = fig.add_subplot(1, 3, 3)
                ax3.axis("off")
                ax3.imshow(diff, cmap = "gray"); plt.title("difference")
                # ax4 = fig.add_subplot(1, 5, 4)
                # ax4.axis("off")
                # ax4.imshow(mask); plt.title("mask")
                # ax5 = fig.add_subplot(1, 5, 5)
                # ax5.axis("off")
                # ax5.imshow(filled_after); plt.title("filled after")
                plt.show()
                plt.savefig("EXPORT/Plots/SIM_"+str(auftragsnummer)+"_"+str(filename)+".png")
            else:
                print("Similarity Plots turned OFF")
                print("-------------------------------------------------------")
    df_simscore.to_csv(str(exportresultpath)+"Alignscores.csv", index=False)
    print("----------------------DONE-----------------------------")

