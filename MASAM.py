###########################################################################
###########################################################################
###### Imports
###########################################################################
###########################################################################
from align import *
from Page_OCR import *
from Logic import *
from pyzip import *
import time

###########################################################################
###########################################################################
###### Mainrun von MASAM
###########################################################################
###########################################################################
def mainrun(customOutput): 
    sys.stdout = customOutput
    MASAM_time = time.time()  
    sort_pages(customOutput)
    roi(customOutput)
    mainlogic(customOutput)
    MASAM_measure(MASAM_time)
    zipexport(customOutput)
    clear_all()

###########################################################################
###########################################################################
###### Zeit Messen
###########################################################################
###########################################################################
def MASAM_measure(MASAM_time):
    End_Time = time.time()
    Zeit = End_Time - MASAM_time
    message = "Zeit für Prüfung des Batchrecords: " + str(round(Zeit,2)) + " Sekunden"
    with open(os.path.join("./EXPORT/Results/", "Runtime.txt"), "w") as f:
        f.write(message)
    
###########################################################################
###########################################################################
###### Alles Löschen
###########################################################################
###########################################################################
def clear_all():
    #------------------------
    #Logfiles
    #------------------------ 
    dir = "./Export/Logs/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    #------------------------
    #Results
    #------------------------ 
    dir = "./Export/Results/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    #------------------------
    #Plots
    #------------------------ 
    dir = "./Export/Plots/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    #------------------------
    #Align Images sorted
    #------------------------ 
    dir = "./aligned_images_sorted/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    #------------------------
    #Exportimg
    #------------------------ 
    dir = "./exportimg/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    #------------------------
    #input Align
    #------------------------ 
    dir = "./input_ALIGN/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    #------------------------
    #Plots
    #------------------------ 
    dir = "./output_ALIGN/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    print("Alle Auftragsdaten wurden entfernt.\n")
    print("Bitte ZIP-File Downloaden. \n")
    