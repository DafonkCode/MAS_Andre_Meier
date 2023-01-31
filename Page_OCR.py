###########################################################################
###########################################################################
###### Imports
###########################################################################
###########################################################################
import cv2
import pytesseract
import numpy as np
import sys
import torch
import os
import ast
from datetime import datetime
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import csv
import time
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from PIL import Image
import natsort
import BR_config

#pytesseract path
#C:\Users\Andre\anaconda3\envs\OpenCV\Scripts
#https://cs.nyu.edu/~roweis/data.html

###########################################################################
###########################################################################
###### Settings und Variablen
###########################################################################
###########################################################################
#Settings sind in BR_config.py ersichtlich
#Zurücklesen und transformieren der globalen Variablen
datebegin = BR_config.datebegin
dateend = BR_config.dateend
starttime = BR_config.starttime
endtime = BR_config.endtime
auftragsnummer = BR_config.auftragsnummer
batchnummer = BR_config.batchnummer
faildate = BR_config.faildate
failtime = BR_config.failtime
checkfilepath = BR_config.checkfilepath
plots = BR_config.plots
dilatesize = BR_config.dilatesize
inputsize = BR_config.inputsize
startdate = datetime.strptime(datebegin, "%d.%m.%y")
enddate = datetime.strptime(dateend, "%d.%m.%y")
starttime = datetime.strptime(starttime, '%H:%M:%S').time()
endtime = datetime.strptime(endtime, '%H:%M:%S').time()
reslist = [["restype", "resname", "resvalue"]]
model = keras.models.load_model("./model/FullDataset55px.h5")
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
yolo = torch.hub.load("yolov5", "custom", path = "yolov5/runs/train/exp19/weights/best.pt", source= 'local',  force_reload = True)
yolo.conf = 0.40  # Confidence threshold (0-1)
yolo.iou = 0.40  # NMS IoU threshold (0-1)  
exportpath = r"./EXPORT/"
exportresultpath = r"./EXPORT/Results/"
exportlogpath = r"./EXPORT/Logs/"
korrlst = []

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###### Hauptfunktion
###########################################################################
###########################################################################
###########################################################################
###########################################################################
# Dieser Code liest Bilder von einem Pfad ein, sucht bestimmte Regionen innerhalb der Bilder (ROIs) und führt verschiedene Prüfungen auf diesen ROIs durch. 
# Dabei werden die Ergebnisse der Prüfungen in eine Textdatei geschrieben und eventuell auch Plots angezeigt. 
# Die Prüfungen umfassen das Überprüfen auf bestimmte Daten (Datum, Zahl), das Ausfüllen von leeren ROIs mit einem Standardwert und das Maskieren von ROIs. 
# Die ROIs werden aus einer Mapping-Datei gelesen und es wird nach Daten innerhalb eines vorgegebenen Zeitraums gesucht. 
# Am Ende werden die verarbeiteten Bilder in einen anderen Ordner verschoben.
def roi(customOutput):
    Start_Time_main = time.time() 
    delete_ordner()
    checklog = open(str(exportlogpath)+"Checklog_"+str(auftragsnummer)+".txt", 'w')
    customOutput.registerOutputFunction(checklog.write)
    sys.stdout = customOutput
    print("###################################################")
    print("#Auftragsdaten")
    print("###################################################")
    print("Startdatum: " +str(datebegin))
    print("Enddatum: " +str(dateend))
    print("Auftragsnummer: " +str(auftragsnummer))
    print("Batchnummer: " +str(batchnummer))
    print("Timestamp: "+str(datetime.now()))
    for dirname, _, filenames in os.walk(checkfilepath):
        filenames = natsort.natsorted(filenames,reverse=False)    
        for filename in filenames:
            Start_Time = time.time()
            checkfile = os.path.join(dirname, filename)
            parts = filename.split(".")
            #---------------------------------------------------------
            #Mapping zuweisen
            #---------------------------------------------------------
            number = parts[0].strip()
            print("*******************************************************")
            print("Check Page No. " + str(number))
            print("-------------------------------------------------------")
            with open("./Mapping/P" + number + ".txt", 'r') as f:
                res = ast.literal_eval(f.read())
            roi = res
            imgScan = cv2.imread(checkfile)
            imgScan = cv2.cvtColor(imgScan, cv2.COLOR_BGR2RGB)
            imgShow = imgScan.copy()
            imgMask = np.zeros_like(imgShow)
            i = 0
            for i in range(len(roi)):
                print("*******************************************************")
                print("Check: " + str(roi[i][3]))
                print("-------------------------------------------------------")
                #---------------------------------------------------------
                #Prüfe auf Typ Datum            
                #---------------------------------------------------------
                if roi[i][2] == "datum":
                    New = cv2.addWeighted(imgShow, 0.90, imgMask, 0.1, 0)
                    imgCrop = imgScan[roi[i][0][1]:roi[i][1][1], roi[i][0][0]:roi[i][1][0]]
                    date_result = dateempty(imgCrop)
                    if date_result == 0:
                        cv2.rectangle(imgCrop, ((roi[i][0][0]), roi[i][0][1]),((roi[i][1][0]), roi[i][1][1]), (255,0,0), cv2.FILLED)
                        dt = datetime(1970, 1, 1)
                        date =dt.date()
                        date = dt.strftime('%d.%m.%y')
                        restype = roi[i][2]
                        resname = roi[i][3]
                        resvalue = date
                        print("Datecheck cancelled")
                        print("----------------------DONE-----------------------------")   
                    else:
                        cv2.rectangle(imgCrop, ((roi[i][0][0]), roi[i][0][1]),((roi[i][1][0]), roi[i][1][1]), (255,0,0), cv2.FILLED)
                        char, date = digitpre(imgCrop, model, startdate, enddate)
                        if plots == True and char is not None :
                            plt.imshow(char, cmap= "gray")
                            plt.show()
                        else:
                            print("Plots turned OFF")
                        print("----------------------DONE-----------------------------")
                    #---------------------------------------------------------
                    #Maskierung anzeigen
                    #---------------------------------------------------------
                    # plt.figure(dpi = 200)
                    # plt.imshow(New)
                    # plt.axis("off")
                    # plt.show()
                        restype = roi[i][2]
                        resname = roi[i][3]
                        resvalue = str(date)
                #---------------------------------------------------------
                #Prüfe auf Typ Time
                #--------------------------------------------------------- 
                if roi[i][2] == "time":
                    New = cv2.addWeighted(imgShow, 0.90, imgMask, 0.1, 0)
                    imgCrop = imgScan[roi[i][0][1]:roi[i][1][1], roi[i][0][0]:roi[i][1][0]]
                    result_time = timeempty(imgCrop)
                    if result_time == 0:
                        result_time = datetime.strptime('0000', '%H%M').time()
                        restype = roi[i][2]
                        resname = roi[i][3]
                        resvalue = result_time
                        print("Timecheck cancelled")
                        print("----------------------DONE-----------------------------")   
                    else:
                        char, zeit = timepre(imgCrop, model)
                        if plots == True and char is not None :
                            plt.imshow(char, cmap= "gray")
                            plt.show()
                        else:
                            print("Plots turned OFF")
                        print("----------------------DONE-----------------------------")
                    #---------------------------------------------------------
                    #Maskierung anzeigen
                    #---------------------------------------------------------
                    # plt.figure(dpi = 200)
                    # plt.imshow(New)
                    # plt.axis("off")
                    # plt.show()
                        restype = roi[i][2]
                        resname = roi[i][3]
                        resvalue = str(zeit)
                #---------------------------------------------------------        
                #Prüfe auf Typ Value
                #---------------------------------------------------------
                if roi[i][2] == "value":
                    cv2.rectangle(imgMask, ((roi[i][0][0]), roi[i][0][1]),((roi[i][1][0]), roi[i][1][1]), (0,255,0), cv2.FILLED)
                    New = cv2.addWeighted(imgShow, 0.90, imgMask, 0.1, 0)
                    imgCrop = imgScan[roi[i][0][1]:roi[i][1][1], roi[i][0][0]:roi[i][1][0]]
                    value_result = valueempty(imgCrop)
                    if value_result == 0:
                        restype = roi[i][2]
                        resname = roi[i][3]
                        resvalue = value_result
                        print("Value check cancelled")
                        print("----------------------DONE-----------------------------")   
                    else:
                        varchar, val = valuepre(imgCrop, model)
                        if plots == True and varchar is not None :
                            plt.imshow(varchar, cmap= "gray")
                            plt.show()
                        else:
                            print(roi[i][2])
                            print(roi[i][3])
                            print("Plots turned OFF")
                        print("----------------------DONE-----------------------------")
                    # plt.figure(dpi = 200)
                    # plt.imshow(New)
                    # plt.axis("off")
                    # plt.show()
                        restype = roi[i][2]
                        resname = roi[i][3]
                        resvalue = str(val)
                #---------------------------------------------------------        
                #Prüfe auf Typ Visum                    
                #---------------------------------------------------------
                elif roi[i][2] == "visum":
                    cv2.rectangle(imgMask, ((roi[i][0][0]), roi[i][0][1]),((roi[i][1][0]), roi[i][1][1]), (0,255,0), cv2.FILLED)
                    New = cv2.addWeighted(imgShow, 0.90, imgMask, 0.1, 0)
                    imgCrop = imgScan[roi[i][0][1]:roi[i][1][1], roi[i][0][0]:roi[i][1][0]]
                    visum, visumchar = visumpre(imgCrop)
                    restype = roi[i][2]
                    resname = roi[i][3]
                    resvalue = visum
                    print("----------------------DONE-----------------------------")
                #---------------------------------------------------------
                #Prüfe auf Typ Tesserract                
                #---------------------------------------------------------
                elif roi[i][2] == "tess":
                    cv2.rectangle(imgMask, ((roi[i][0][0]), roi[i][0][1]),((roi[i][1][0]), roi[i][1][1]), (0,255,0), cv2.FILLED)
                    New = cv2.addWeighted(imgShow, 0.90, imgMask, 0.1, 0)
                    imgCrop = imgScan[roi[i][0][1]:roi[i][1][1], roi[i][0][0]:roi[i][1][0]]
                    tess, tesschar = tesspre(imgCrop)
                    
                    if roi[i][3] == "p" + str(number)+"_tess_auftragsnummer":
                        if tess == auftragsnummer:
                            print("Auftragsnummer OK")
                        else:
                            print("Auftragnummer NOT OK")
                    if roi[i][3] == "p" + str(number)+"_tess_batchnummer":
                        if tess == batchnummer:
                            print("Batchnummer OK")
                        else:
                            print("Batchnummer NOT OK")
                    restype = roi[i][2]
                    resname = roi[i][3]
                    resvalue = tess                   
                    print("----------------------DONE-----------------------------")
                #---------------------------------------------------------      
                #Prüfe auf Typ Checkbox
                #---------------------------------------------------------
                elif roi[i][2] == "checkbox":
                    New = cv2.addWeighted(imgShow, 0.90, imgMask, 0.1, 0)
                    imgCrop = imgScan[roi[i][0][1]:roi[i][1][1], roi[i][0][0]:roi[i][1][0]]
                    checkbox, checkboxchar = checkpre(imgCrop)
                    restype = roi[i][2]
                    resname = roi[i][3]
                    resvalue = checkbox
                    print("----------------------DONE-----------------------------")
                #---------------------------------------------------------
                #Prüfe auf Typ Unbekannt
                #---------------------------------------------------------
                else:
                    print(roi[i][2])
                    print(roi[i][3])
                    print()
                    print("Nothing Found")
                    print("----------------------DONE-----------------------------")   
                i +=1
                if [restype, resname, resvalue] not in reslist:
                    reslist.append([restype, resname, resvalue])
            korrcheck(imgScan, number)

            runtime_measure(Start_Time)
        csv_write()
        savepdf()
    runtime_measure(Start_Time_main)
    customOutput.unregisterOutputFunction(checklog.write)
    checklog.close()
    


###########################################################################
###########################################################################
###### Datum
###########################################################################
###########################################################################
# Dieser Code enthält Funktionen zur Vorverarbeitung und Prüfung von Bildern auf Daten. Die Funktion dateempty überprüft, ob in einem gegebenen Bild ein Datum vorliegt, 
# indem sie prüft, ob genügend dunkle Pixel vorhanden sind. Die Funktion digitpre macht aus einem Bild eine Schwarz-Weiß-Version, 
# extrahiert daraus die Konturen und zeichnet Rechtecke um die Konturen. Die innerhalb dieser Rechtecke befindlichen Bilder werden dann an ein neuronales Netzwerk übergeben, 
# um sie zu interpretieren und in Zeichen umzuwandeln. Die Funktion check_date nimmt das Ergebnis der Zeicheninterpretation und versucht, daraus ein gültiges Datum im Format dd.mm.yy zu parsen. 
# Ist dies erfolgreich, wird das Datum mit Hilfe von startdate und enddate auf Gültigkeit überprüft.
#---------------------------------------------------------
#Check if empty
#---------------------------------------------------------
def dateempty(img):
    pixelThreshold = 900
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgGray, 170, 255, cv2.THRESH_BINARY_INV)[1]
    #plt.imshow(img, cmap = "gray")
    #plt.show()
    
    totalPixels = cv2.countNonZero(imgThresh)
    #print(totalPixels)
    if totalPixels>pixelThreshold:
        totalPixels = 1
    else:
        totalPixels = 0

    if totalPixels == 1:
        print("Date detected")
    else: 
        print("No Date detected")
    dateresult = totalPixels
    
    return dateresult 
#---------------------------------------------------------
#Preprocessing
#---------------------------------------------------------

def digitpre(img, model, startdate, enddate):
    resultlst = []
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    img_before = img
    img_after = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(img_after, 50, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh2 = thresh
    thresh = cv2.dilate(thresh, kernel, iterations=dilatesize)
    plt.imshow(thresh)
    plt.show()
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    bbxlst = []
    i = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 150:
            x,y,w,h = cv2.boundingRect(c)
            if h >= 15:
                if w >= 100:
                    # Wenn checkbox grösser als variable w, teile / 2
                    w = w // 2
                    # Beide Boxen der Liste hinzufügen
                    bbxlst.append([x,y,w,h])
                    bbxlst.append([x+w,y,w,h])
                else:
                    # Bounding box so lassen wie sie ist
                    bbxlst.append([x,y,w,h])

    bbxlst.sort(key = lambda el: el[0])
    crop = None
    char = None
    for e in bbxlst:
        x,y,w,h = e
        crop = img[y:y+h, x:x+w]
        result = predict_digit(crop, model)
        resultlst.append(result)
        char = cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)
    if len(resultlst) != 0:
        resultlst = str(''.join([str(i) for i in resultlst]))

    a = str(resultlst)
    date = check_date(resultlst, startdate, enddate)
    return char, date

def check_date(resultlst, startdate, enddate):
    a = str(resultlst)
    print("Detected String: " + str(a))
    if len(resultlst) == 6:
        try:
            dt = datetime.strptime(a, '%d%m%y')
            print("Date format Valid")
        except ValueError:
            dt = datetime(1970, 1, 1)
            dtstr = datetime(1970, 1, 1).strftime('%d.%m.%y')
            print("Invalid date format. Set default value: " + dtstr)
    else: 
        dt = datetime(1970, 1, 1)
        dtstr = datetime(1970, 1, 1).strftime('%d.%m.%y')
        print("Invalid date format. Set default value: " + dtstr)

    # Überprüfe, ob das Datum im gültigen Bereich liegt
    if startdate <= dt <= enddate:
        print("Date Range OK")
    else:
        print("Date Range NOT OK")
    date =dt.date()
    date = dt.strftime('%d.%m.%y')
    print(date)

    return date

#---------------------------------------------------------
#Predict Digits
#---------------------------------------------------------
def predict_digit(crop, model):

    height = inputsize
    width = inputsize
    dim = width , height

    #Für VGG16 Auskommentieren
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^
    charcheck = image_resize_keep_aspect(crop, inputsize, border=2, interpolation = cv2.INTER_LINEAR)
    charcheck = tf.keras.utils.img_to_array(charcheck)
    charcheck = np.expand_dims(charcheck, axis = 0)
    
    y_pred = model.predict(charcheck, verbose = 0)
    y_pred = (y_pred > 0.5)

    res = [i for i, val in enumerate(y_pred[0]) if val]
    pred = res[0]
    print("Digit identified as: " +str(pred))
    return pred



###########################################################################
###########################################################################
###### Resize der Bilder mit Beibehaltung der Proportion
###########################################################################
###########################################################################
# Der unten gezeigte Code ist eine Funktion, die ein Bild auf die gewünschte Größe skaliert, 
# wobei der Aspekt des Bildes beibehalten wird. Die Funktion nimmt vier Argumente entgegen: image, size, border und interpolation. 
# Image ist das Bild, das skaliert werden soll. Size ist die Größe, auf die das Bild skaliert werden soll. 
# Border ist der Rand, der um das Bild hinzugefügt werden soll, wenn es skaliert wird. Interpolation ist die Art der Interpolation, die verwendet werden soll, um das Bild zu skalieren. 
# Die Funktion gibt das skalierte Bild zurück. 
# Mit overdrive kann die stärke des Effekts verändert werden.

def image_resize_keep_aspect(image, size, border = 0, interpolation = cv2.INTER_AREA):

    #Stärke des Effekts
    overdrive = 1.5

    #Dimensions platzhalter
    dim = None
    (h, w) = image.shape[:2]
    image = cv2.fastNlMeansDenoising(image, None, 20,7,21 )

    #min max Bildwerte
    darkest = np.amin(image)
    brightest = np.amax(image)
    
    #Steigung Grautonfunktion von originalbild
    slope = brightest - darkest
    if slope == 0:
        slope = 1
    multiplier = 255/float(slope)
    lower = int((255*overdrive-255)/2)

    #Platzerhalter in Grösse des Bildes in schwarz, int16 wegen Überlauf
    buffer = np.full((len(image),len(image[0])), 255, np.int16)
    
    #Kurve steiler machen und zentrieren
    for i in range(len(image)-1):
        for j in range(len(image[i])-1):
            value = int((image[i][j]-darkest)*multiplier*overdrive)-lower
            buffer[i][j] = value

    
    #handeln von Wertüberläufen
    for i in range(len(image)-1):
        for j in range(len(image[i])-1):
            if buffer[i][j] < 0:
                image[i][j] = 0
            elif buffer[i][j] > 255:
                image[i][j] = 255
            else:
                image[i][j] = buffer[i][j]


    #entscheidung ob bild in höhe oder breite resized wird
    if h > w:
        m = float(size-2*border)/float(h)
        dim = int(m*w),size-2*border
    else:
        m = float(size-2*border)/float(w)
        dim = size-2*border,int(m*h)
    #Resize von bild
    resized = cv2.resize(image, dim, interpolation = interpolation)
    #Leeres bild erstellen
    blank_image = np.full((size,size),255,  np.uint8)
    
    #Zentriertes einfügen des resized image
    if h > w:
        offset = int((size-2*border-dim[0]) / 2)
        (h,w) = resized.shape[:2]
        blank_image[border:h+border,offset+border:offset+border+w] = resized
    else:
        offset = int((size-2*border-dim[1]) / 2)
        (h,w) = resized.shape[:2]
        blank_image[offset+border:offset+h+border,border:w+border] = resized

    # return vom resized image
    return blank_image

###########################################################################
###########################################################################
###### Zeit
###########################################################################
###########################################################################
# Dieser Codeblock enthält Funktionen zur Vorverarbeitung und Prüfung von Bildern auf Zeitangaben. Die Funktion timeempty überprüft, ob in einem gegebenen Bild eine Zeitangabe vorliegt, 
# indem sie prüft, ob genügend dunkle Pixel vorhanden sind. Die Funktion timepre macht aus einem Bild eine Schwarz-Weiß-Version, extrahiert daraus die Konturen und zeichnet 
# Rechtecke um die Konturen. Die innerhalb dieser Rechtecke befindlichen Bilder werden dann an ein neuronales Netzwerk übergeben, um sie zu interpretieren und in Zeichen umzuwandeln. 
# Die Funktion check_time nimmt das Ergebnis der Zeicheninterpretation und versucht, daraus eine gültige Zeit im Format hhmm zu parsen. Ist dies erfolgreich, wird die Zeit mit Hilfe von 
# starttime und endtime auf Gültigkeit überprüft.
#---------------------------------------------------------
#Check if empty
#---------------------------------------------------------
def timeempty(img):
    pixelThreshold = 900
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgGray, 170, 255, cv2.THRESH_BINARY_INV)[1]
    #plt.imshow(img, cmap = "gray")
    #plt.show()
    
    totalPixels = cv2.countNonZero(imgThresh)
    #print(totalPixels)
    if totalPixels>pixelThreshold:
        totalPixels = 1
    else:
        totalPixels = 0

    if totalPixels == 1:
        print("Time detected")
    else: 
        print("No Time detected")
    timeresult = totalPixels
    
    return timeresult 
#---------------------------------------------------------
#Preprocessing
#---------------------------------------------------------
def timepre(img, model):
    resultlst = []
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    img_before = img
    img_after = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(img_after, 50, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh2 = thresh
    thresh = cv2.dilate(thresh, kernel, iterations=dilatesize)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    bbxlst = []
    i = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 100:
            x,y,w,h = cv2.boundingRect(c)
            if h >= 15:
                if w >= 80:
                    # Wenn Boundingbox grösser als variable w dann w / 2
                    w = w // 2
                    # Beide Boxen der Liste hinzufügen
                    bbxlst.append([x,y,w,h])
                    bbxlst.append([x+w,y,w,h])
                else:
                    # Boundingbox so lassen wie sie ist
                    bbxlst.append([x,y,w,h])

    
    bbxlst.sort(key = lambda el: el[0])
    
    crop = None
    char = None
    for e in bbxlst:
        x,y,w,h = e
        crop = img[y:y+h, x:x+w]
        result = predict_digit(crop, model)
        resultlst.append(result)
        char = cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)
    if len(resultlst) != 0:
        resultlst = str(''.join([str(i) for i in resultlst]))

    a = str(resultlst)
    time = check_time(resultlst, starttime, endtime)
    return char, time

def check_time(resultlst, starttime, endtime):
    resultlst_str = str(resultlst)
    
    print("Detected Time String: " + str(resultlst_str))
    if len(resultlst_str) == 4:
        try:
            result_time = datetime.strptime(resultlst_str, '%H%M').time()
            print("Time format Valid")
        except ValueError:
            result_time = datetime.strptime('0000', '%H%M').time()
            print("Invalid time format. Set default value: " + str(result_time))
    else:
        result_time = datetime.strptime('0000', '%H%M').time()
        print(result_time)
        print("Invalid time format. Set default value: " + str(result_time))
    if starttime <= result_time <= endtime:
        print("Time Range OK")
    else:
        print("Time Range NOT OK")
    print(result_time)
    return result_time

###########################################################################
###########################################################################
###### Visum
###########################################################################
###########################################################################
#Der Codeblock überprüft, ob sich auf einem Bild ein Visum befindet. Dazu werden zunächst die Konturen auf dem Bild ermittelt und für jede Kontur, 
# die eine Fläche von mehr als X Pixeln hat, wird ein Rechteck um sie gezeichnet. Danach wird die Anzahl an schwarzen Pixeln auf dem Bild gezählt 
# und anhand eines Schwellenwertes entschieden, ob sich auf dem Bild ein Visum befindet oder nicht. Der Schwellenwert hängt von der Höhe des Bildes 
# ab und wird entsprechend angepasst. Am Ende wird das Ergebnis ausgegeben und zusammen mit der Anzahl an schwarzen Pixeln zurückgegeben.
def visumpre(img, plots=True):
    visumchar = None
    imgh = img.shape[0]
    imgw = img.shape[1]
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgGray, 170, 255, cv2.THRESH_BINARY_INV)[1]
    contours = cv2.findContours(imgThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    total_pixels_in_bounding_boxes = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 200:
            x,y,w,h = cv2.boundingRect(c)
            visumchar = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) 
            total_pixels_in_bounding_boxes += w*h

    if imgh <= 40:
        pixelThreshold = 500
        print("pixelThreshold set to: "+str(pixelThreshold))
    else:
        pixelThreshold = 650
        print("pixelThreshold set to: "+str(pixelThreshold))


    if plots == True and visumchar is not None:
        plt.imshow(img, cmap = "gray")
        plt.show()
    else:
        print("Plots turned OFF")

    totalPixels = cv2.countNonZero(imgThresh)
    total_pixels_in_bounding_boxes = cv2.countNonZero(imgThresh)

    if plots and visumchar is not None:
            plt.imshow(img, cmap = "gray")
            plt.show()
    else:
        print("Plots turned OFF")

    if total_pixels_in_bounding_boxes>pixelThreshold:
        print("Total Pixel: " +str(total_pixels_in_bounding_boxes))
        totalPixels = 1
    else:
        print("Total Pixel: " +str(total_pixels_in_bounding_boxes))
        totalPixels = 0

    if totalPixels == 1:
        print("Visum OK")
    else: 
        print("Visum NOT OK")
    visum = totalPixels
    return visum, totalPixels

###########################################################################
###########################################################################
###### Tesserract
###########################################################################
###########################################################################
# Der Code definiert eine Funktion namens "tesspre", die ein Bild als Eingabe annimmt. Das Bild wird zunächst in Graustufen umgewandelt 
# und es werden die Konturen des Bildes gefunden. Dann werden die Konturen durchlaufen und für jede Kontur wird deren Fläche berechnet. 
# Wenn die Fläche größer als X ist, wird ein Rechteck um die Kontur gezeichnet. Danach wird der Text im Bild mithilfe von Tesseract 
# erkannt und ausgegeben. Am Ende wird der erkannte Text zurückgegeben, zusammen mit dem Bild, auf dem die Rechtecke gezeichnet sind.
def tesspre(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours = cv2.findContours(imgGray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    i = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 150:
            x,y,w,h = cv2.boundingRect(c)
            tesschar = cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)  
    if plots == True:
        plt.imshow(img, cmap = "gray")
        plt.show()
    else:
        print("Plots turned OFF")

    text = pytesseract.image_to_string(imgGray)
    print("Detected String: " + str(text))
    tess = text
    tess = tess.strip()
    return tess, tesschar 

###########################################################################
###########################################################################
###### Check Value
###########################################################################
###########################################################################
# Dieser Code definiert zwei Funktionen: "valueempty" und "valuepre". 
# Die Funktion "valueempty" nimmt ein Bild als Eingabe und funktioniert genauso wie in meiner vorherigen Erklärung: 
# Das Bild wird in Graustufen umgewandelt, binarisiert und die Anzahl nicht-Null-Pixel wird gezählt. Wenn diese Anzahl größer als ein festgelegter Schwellenwert ist, 
# wird "Value detected" ausgegeben und der Wert 1 zurückgegeben, andernfalls wird "No Value detected" ausgegeben und der Wert 0 zurückgegeben.

# Die Funktion "valuepre" nimmt ebenfalls ein Bild als Eingabe und zusätzlich ein Modell. Das Bild wird zunächst in Graustufen umgewandelt und es wird ein Schwellenwert festgelegt. 
# Das Bild wird dann binarisiert und es werden die Konturen des Bildes gefunden. Dann werden die Konturen durchlaufen und für jede Kontur wird deren Fläche berechnet. 
# Wenn die Fläche größer als X ist, wird ein Rechteck um die Kontur gezeichnet. Wenn das Rechteck eine Höhe von mindestens X Pixeln hat und eine Breite von mindestens X Pixeln hat, 
# wird das Rechteck in zwei Hälften geteilt und beide Hälften der Liste "bbxlst" hinzugefügt. Wenn das Rechteck weniger als X Pixel breit ist, wird es unverändert der Liste "bbxlst" hinzugefügt. 
# Die Liste "bbxlst" wird sortiert und für jedes Element in der Liste wird ein Ausschnitt aus dem Bild genommen und das Modell wird verwendet, um die Ziffer in diesem Ausschnitt vorherzusagen. 
# Die Vorhersage wird der Liste "resvallst" hinzugefügt und das ursprüngliche Bild wird gezeichnet. Am Ende wird das Bild mit gezeichneten Rechtecken und die Liste "resvallst" zurückgegeben.
#---------------------------------------------------------
#Check if empty
#---------------------------------------------------------
def valueempty(img):

    pixelThreshold = 100
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgGray, 170, 255, cv2.THRESH_BINARY_INV)[1]
   
    totalPixels = cv2.countNonZero(imgThresh)

    if totalPixels>pixelThreshold:
        totalPixels = 1
    else:
        totalPixels = 0

    if totalPixels == 1:
        print("Value detected")
    else: 
        print("No Value detected")
    valueresult = totalPixels
    
    return valueresult 

#---------------------------------------------------------
#Preprocessing
#---------------------------------------------------------    
def valuepre(img, model):
    resvallst = []

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    img_before = img
    img_after = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(img_after, 50, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh2 = thresh
    thresh = cv2.dilate(thresh, kernel, iterations=dilatesize)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    bbxlst = []
    i = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 120:
            x,y,w,h = cv2.boundingRect(c)
            if h >= 15:
                if w >= 100:
                    # Wenn w grösser als variable w, dann w / 2
                    w = w // 2
                    # Beide Boxen der Liste hinzufügen
                    bbxlst.append([x,y,w,h])
                    bbxlst.append([x+w,y,w,h])
                else:
                    # Box so lassen wie sie ist
                    bbxlst.append([x,y,w,h])
    
    bbxlst.sort(key = lambda el: el[0])
    crop = None
    varchar = None
    for e in bbxlst:
        x,y,w,h = e
        crop = img[y:y+h, x:x+w]
        val = predict_digit(crop, model)
        resvallst.append(val)
        varchar = cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)
    if len(resvallst) != 0:
        resvallst = int(''.join([str(i) for i in resvallst]))
    return varchar, resvallst

###########################################################################
###########################################################################
###### Checkbox
###########################################################################
###########################################################################
# Dieser Code definiert eine Funktion namens "checkpre", die ein Bild als Eingabe annimmt. Das Bild wird zunächst in Graustufen umgewandelt und es wird ein Schwellenwert von X festgelegt. 
# Das Bild wird dann mithilfe dieses Schwellenwerts binarisiert. Danach werden die Konturen des Bildes gefunden und für jede Kontur wird deren Fläche berechnet. Wenn die Fläche größer als X ist, 
# wird ein Rechteck um die Kontur gezeichnet. Wenn die Variable "plots" True ist, wird das Bild mit den gezeichneten Rechtecken angezeigt,
# ansonsten wird "Plots turned OFF" ausgegeben. Danach wird gezählt, wie viele Pixel im binarisierten Bild nicht den Wert 0 haben. Wenn diese Anzahl größer als ein festgelegter Schwellenwert von X Pixel ist, 
# wird "Checkbox ticked" ausgegeben und der Wert 1 zurückgegeben, andernfalls wird "Checkbox empty" ausgegeben und der Wert 0 zurückgegeben.
def checkpre(img):
    checkboxchar = None
    pixelThreshold = 550
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgGray, 170, 255, cv2.THRESH_BINARY_INV)[1]
    contours = cv2.findContours(imgThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    i = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 150:
            x,y,w,h = cv2.boundingRect(c)
            checkboxchar = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) 
    if plots == True and checkboxchar is not None:
        plt.imshow(img, cmap = "gray")
        plt.show()
    else:
        print("Plots turned OFF")
    totalPixels = cv2.countNonZero(imgThresh)
    print("Total Pixel: " +str(totalPixels))
    if totalPixels>pixelThreshold:
        totalPixels = 1
    else:
        totalPixels = 0

    if totalPixels == 1 :
        print("Checkbox ticked")
    else:
        print("Checkbox empty")
    checkbox = totalPixels 
    return checkbox, checkboxchar

####################################################################
####################################################################
# Runtime Measure                                           
####################################################################
####################################################################
# Dieser Code definiert zwei Funktionen: "runtime_measure" und "runtime_measure_main".
# Die Funktion "runtime_measure" nimmt eine Startzeit als Eingabe und berechnet die Dauer, die seitdem vergangen ist. 
# Dazu wird die aktuelle Zeit ermittelt und die Differenz zur Startzeit berechnet. Die Dauer wird in Sekunden ausgegeben.
# Die Funktion "runtime_measure_main" funktioniert genauso wie "runtime_measure", nur dass sie stattdessen die Dauer des Hauptprozesses ausgibt.
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
# export to csv                                        
####################################################################
####################################################################
# Dieser Code definiert eine Funktion namens "csv_write", die eine CSV-Datei schreibt. 
# Zunächst wird eine neue CSV-Datei erstellt und ein "csv.writer" wird initialisiert. 
# Danach werden die Zeilen in der Liste "reslist" mit "writer.writerows" in die CSV-Datei geschrieben und die Datei wird geschlossen.
def csv_write():
    with open("./csv/Batch_"+str(auftragsnummer) +'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(reslist)

####################################################################
####################################################################
#Check for corrections                  
####################################################################
####################################################################
# Dieser Code definiert eine Funktion namens "korrcheck", die ein Bild und eine Nummer als Eingabe annimmt. 
# Die Funktion verwendet das Bild, um mit einem YOLO-Modell die Anzahl der Korrekturen auf dem Bild zu zählen. 
# Das Ergebnis wird angezeigt und das Bild wird in eine Datei gespeichert. Die Anzahl der Korrekturen wird auch in eine Liste namens "korrlst" 
# geschrieben und diese Liste wird in eine CSV-Datei exportiert. Am Ende wird das Ergebnis des YOLO-Modells zurückgegeben.
def korrcheck(korrimg, number):
    yoloresults = yolo(korrimg)
    plt.imshow(np.squeeze(yoloresults.render()))
    imgyolo = yoloresults.pandas().xyxy[0].value_counts('name')

    rendered_image = yoloresults.render()
    
    image = np.squeeze(rendered_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    
    if plots == False:
        print("Plots turned OFF")
        cv2.imwrite("./exportimg/"+number+".jpg", image)
    else:
        yoloresults.show()
        cv2.imwrite("./exportimg/"+number+".jpg", image)
    
    re = yoloresults.pandas().xyxy
    total = np.shape(re)[0]    # Total nummer der geprüften Bilder
    print('Page =', number)
    unf = np.array([])
    sl = np.array([]) 
    c = 1
    while c <= total:
        
        for i in re:
                
            n = np.shape(i)[0]   # Nummer der detektierten Korrekturen
            
            if n > 0:
                if n not in unf:
                    
                    unf = np.append(unf,n)
                    sl = np.append(sl,c)
                
            c += 1 
    print("*******************************************************")
    print("Number of corrections: " + str(n))
    print("-------------------------------------------------------")                                        

    korrlst.append(("Page: "+str(number), "Korrekturen: " +str(n)))
    with open(str(exportresultpath)+"Batch_"+str(auftragsnummer) +'_Korrekturen_.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(korrlst)
    return imgyolo

####################################################################
####################################################################
#PDF sichern         
####################################################################
####################################################################
# Dieser Code definiert eine Funktion namens "savepdf", die alle Bilder in einem bestimmten Ordner öffnet, 
# in ein PDF-Dokument einfügt und das PDF speichert. Zunächst werden die Dateinamen im Ordner aufgelistet und sortiert. 
# Danach wird ein neues PDF-Dokument erstellt. Dann werden alle Dateien im Ordner durchlaufen und überprüft, ob sie auf ".jpg" enden. 
# Wenn dies der Fall ist, wird das Bild geöffnet, skaliert und dem PDF hinzugefügt. Am Ende wird das PDF gespeichert.
def savepdf():
    folder = './exportimg/'
    filenames = os.listdir(folder)
    filenames = natsort.natsorted(filenames,reverse=False)
    pdf_file = str(exportresultpath) + str(auftragsnummer)+"_Results.pdf"
    c = Canvas(pdf_file, pagesize=A4)
    for file in filenames:
        
        if file.endswith('.jpg'):
            image = Image.open(os.path.join(folder, file))

            width, height = image.size
            max_width, max_height = A4
            scale = min(max_width / width, max_height / height)
            image = image.resize((int(width * scale), int(height * scale)), Image.ANTIALIAS)

            # Füge das Bild dem PDF hinzu
            c.drawInlineImage(image, 0, 0)
            c.showPage()

    # Speichere das PDF
    c.save()

####################################################################
####################################################################
#Ordner Löschen         
####################################################################
####################################################################
# Dieser Code definiert eine Funktion namens "delete_ordner", die alle Dateien in einem bestimmten Ordner löscht. 
# Zunächst wird der Pfad zum Ordner festgelegt. Danach werden alle Dateien im Ordner durchlaufen und mit "os.remove" gelöscht. 
# Am Ende wird "DONE" ausgegeben.
def delete_ordner():
    print("*******************************************************")
    print("Delete Folders")
    print("-------------------------------------------------------")
    dir = "./exportimg/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    print("----------------------DONE-----------------------------")

