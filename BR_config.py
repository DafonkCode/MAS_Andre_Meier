####################################################################
####################################################################
# Imports                                                      
####################################################################
####################################################################
from datetime import datetime, timedelta
import csv


####################################################################
####################################################################
# Auslesen der config CSV-Datei aus der GUI                                                  
####################################################################
####################################################################
# Öffnen Sie die CSV-Datei mit dem csv-Modul
with open('./csv/config.csv', 'r') as file:
  # Verwenden Sie den csv-Reader, um das CSV-Dateiobjekt zu iterieren
  reader = csv.reader(file)
  # Initialisieren Sie die Variablen, die die Werte der Zeilen speichern
  global batchnummer
  batchnummer = None
  global auftragsnummer
  auftragsnummer = None
  global datebegin
  datebegin = None
  global dateend
  dateend = None
  global br_name
  br_name = None
  # Iterieren Sie über jede Zeile im CSV-Reader
  for i, row in enumerate(reader):
    if i == 0:

      batchnummer = row[0]
    elif i == 1:
      auftragsnummer = row[0]
    elif i == 2:
      datebegin = row[0]
    elif i == 3:
      dateend = row[0]
    elif i == 4:
      br_name = row[0]

####################################################################
####################################################################
# Definiere Globale Variablen für Scripts                                            
####################################################################
####################################################################
#------------------------
#Alignment
#------------------------
#ImageFile.LOAD_TRUNCATED_IMAGES = True
global delete_folders
delete_folders = True          #delete all folders (True, False)
global importreference
importreference = True         #import Reference PDF to JPG (True, False)
global importalign
importalign = True             #import Alignscans PDF to JPG (True, False)
global savereference
savereference = True           #Save Reference Features (True, False)
global featureplot
featureplot = True             #Acticate Reference Plots (True, False)
global alignplot
alignplot = True               #Activate Align Plots (True, False)
global sortmethod
sortmethod = "Aruco"           #Choose the Sortmethod ("Neural", "Aruco")
global mainfunction
mainfunction = True            #Activate Mainfunction (True, False)
global save_align
save_align = True              #Save the aligned Picture (True, False)
global sim_check
sim_check = True               #Check similiarity of Reference and Aligned Pictures (True, False)
global sim_plot
sim_plot = True                #Activate Similarity Plots (True, False)
global stats
stats = True                   #Show stats of Alignment Procedure

#------------------------
#Page_OCR
#------------------------
global checkfilepath
checkfilepath = "aligned_images_sorted/"
global plots
plots = False
global inputsize
inputsize = 55
global dilatesize
dilatesize = 1

#------------------------
#Logic
#------------------------
global faildate
faildate = "01.01.70"
global starttime
starttime = "05:00:00"
global endtime
endtime = "19:00:00"
global failtime
failtime = "00:00:00"
global total_length
total_length = 60
global comparelist
comparelist = []
