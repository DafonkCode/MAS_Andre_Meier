**************************************************************************
**************************************************************************
  _____           _           _     __  __           _____         __  __ 
  |  __ \         (_)         | |   |  \/  |   /\    / ____|  /\   |  \/  |
  | |__) | __ ___  _  ___  ___| |_  | \  / |  /  \  | (___   /  \  | \  / |
  |  ___/ '__/ _ \| |/ _ \/ __| __| | |\/| | / /\ \  \___ \ / /\ \ | |\/| |
  | |   | | | (_) | |  __/ (__| |_  | |  | |/ ____ \ ____) / ____ \| |  | |
  |_|   |_|  \___/| |\___|\___|\__| |_|  |_/_/    \_\_____/_/    \_\_|  |_|
                _/ |                                                      
                |__/                                                       
**************************************************************************
**************************************************************************
© André Meier 2023, CSL Vifor
andre.meier@viforpharma.com

Diese Software ist im Rahmen der Masterarbeit für den Titel "Master of Advances Studies in Data Science"
entstanden. Weitergabe an Dritte ohne Einverständnis des Urhebers ist grundsätzlich untersagt.

**************************************************************************
Anleitung
**************************************************************************
1. Installieren von Tesseract https://tesseract-ocr.github.io/tessdoc/Installation.html
2. Installieren der erforderlichen Packages entwecker mittels dem Jupyter Notebook "Assets/install.ipynb"
   oder per import der MASAM_conda_enviroment.yaml in Conda Navigator
3. starten des scripts gui.py -> die GUI öffnet sich
4. Auftragsdaten eingeben
    - Auftragsnummer = 123456
    - Batchnummer = AM2023
    - Datumsbereich wählen
4. Mit "PDF hochladen" den Demo Batch Record im Hauptverzeichnis auswählen
5. Auf Start Klicken -> Warten bis Software zu Ende ist
6. ZIP File mit Resultaten herunterladen
7. Resultate auswerten
    - Logs = Alles was während dem Auswerten in die Konsole geschrieben wurde
    - Plots = Alle Plots die während dem Auswerten erstellt wurden
    - Results = CSV dateien, Laufzeitinformationen, PDF mit Resultaten, Final Results

**************************************************************************
WICHTIG
**************************************************************************
Die Ordnerstruktur muss so belassen werden. Durch leichte Unterschiede in Position des DEMO Batch Records
gegenüber dem Originalen kann es sein, dass Positionen von Lesefenstern nicht immer den ganzen Sollbereich auslesen. Diese Demo
dient einzig und allein dem Beweis zur Lauffähigkeit. 

**************************************************************************
Scriptübersicht
**************************************************************************
align.py		=	Script für Umwandlung der Bilder und Bildregistrierung
BR_conig.py		=	Script für Variablen handling und Einstellungen
gui.py 		=	Erstellen der GUI. Startscript der Software
Logic.py		=	Plausibilitätsprüfung des Batch Records
MASAM.py		=	Script um alle Codes miteinander zu verbinden
Page_OCR.py		=	Extrahieren und auswerten der Lesefenster
pyzip.py		=	Verpacken der Resultate
ROI.py		=	Hilfescript für dynamisches Mapping der Lesefenster

