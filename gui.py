###########################################################################
###########################################################################
###### Imports
###########################################################################
###########################################################################
import os
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkcalendar
import shutil
import csv
import sys
import datetime
import tkinter.simpledialog as simpledialog
import time

###########################################################################
###########################################################################
###### Klassendefinierung
###########################################################################
###########################################################################
# In diesem Codeblock werden zwei Klassen definiert, "CustomOutput" und "MyDialog". Die Klasse "CustomOutput" hat Methoden, 
# um Ausgabefunktionen zu registrieren und zu entfernen, um Ausgaben zu schreiben und um Ausgaben zu leeren. Die Klasse "MyDialog" 
# erweitert die Klasse "simpledialog.Dialog" und hat Methoden, um den Dialoginhalt und das Ergebnis des Dialogs zu definieren. 
# Die "init"-Methode der Klasse "CustomOutput" initialisiert das Objekt und speichert den aktuellen Wert von "sys.stdout" in einer Variablen, 
# damit später darauf zugegriffen werden kann. Die "init"-Methode der Klasse "MyDialog" ruft die "init"-Methode der Basisklasse auf und speichert 
# das Argument "prompt" in einer Variablen, die später im Dialogkörper verwendet wird.
# In der "init"-Methode wird zunächst die "init"-Methode der Basisklasse aufgerufen und anschließend die Methode "create_widgets" aufgerufen. 
# Danach wird das "Project MASAM"  in das Eingabefeld "console_output" eingefügt. Anschließend werden in verschiedenen Verzeichnissen alle Dateien gelöscht, 
# indem in Schleifen über die Dateien in den Verzeichnissen iteriert wird und jede Datei mit der "os.remove"-Methode entfernt wird.

class CustomOutput():
    def __init__(self):
        self.old_stdout=sys.stdout
        self.outputFunctions = []
        self.registerOutputFunction(self.old_stdout.write)

    def registerOutputFunction(self, newOutputFunction):
        self.outputFunctions.append(newOutputFunction)

    def unregisterOutputFunction(self, removeOutputFunction):
        self.outputFunctions.remove(removeOutputFunction)

    def write(self, text):
        text = text.rstrip()
        for outputFunction in self.outputFunctions:
            outputFunction(text+"\n")
        
    def flush(self):
        self.old_stdout.write("Cache cleared...")


class MyDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt):
        self.prompt = prompt
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=self.prompt).pack()
        self.e1 = tk.Entry(master)
        self.e1.pack()
        return self.e1

    def apply(self):
        self.result = self.e1.get()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        
        self.console_output.insert(tk.END, "**************************************************************************\n")
        self.console_output.insert(tk.END, "**************************************************************************\n")
        self.console_output.insert(tk.END, "  _____           _           _     __  __           _____         __  __ \n")
        self.console_output.insert(tk.END, " |  __ \         (_)         | |   |  \/  |   /\    / ____|  /\   |  \/  |\n")
        self.console_output.insert(tk.END, " | |__) | __ ___  _  ___  ___| |_  | \  / |  /  \  | (___   /  \  | \  / |\n")
        self.console_output.insert(tk.END, " |  ___/ '__/ _ \| |/ _ \/ __| __| | |\/| | / /\ \  \___ \ / /\ \ | |\/| |\n")
        self.console_output.insert(tk.END, " | |   | | | (_) | |  __/ (__| |_  | |  | |/ ____ \ ____) / ____ \| |  | |\n")
        self.console_output.insert(tk.END, " |_|   |_|  \___/| |\___|\___|\__| |_|  |_/_/    \_\_____/_/    \_\_|  |_|\n")
        self.console_output.insert(tk.END, "                _/ |                                                      \n")
        self.console_output.insert(tk.END, "               |__/                                                       \n")
        self.console_output.insert(tk.END, "**************************************************************************\n")
        self.console_output.insert(tk.END, "**************************************************************************\n")
        
        
        dir = "./Export/Logs/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        
        dir = "./input_ALIGN/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        
        dir = "./Export/Results/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        
        dir = "./Export/Plots/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        
        dir = "./output_ALIGN/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        
        dir = "./exportimg/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        
        dir = "./aligned_images_sorted/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))


        self.console_output.insert(tk.END, "Alle vorherigen Auftragsdaten wurden gelöscht!\n")
        self.console_output.insert(tk.END, "Bitte Auftragsdaten eingeben...\n")

###########################################################################
###########################################################################
###### Create Widgets
###########################################################################
###########################################################################
# In diesem Codeblock werden einige Widgets für ein grafisches Benutzerinterface erstellt und miteinander verbunden. 
# Die Widgets umfassen Labels, Eingabefelder, Buttons und Textfelder. 
    def create_widgets(self):

        self.title_label = tk.Label(self, text="Project MASAM", font=("Arial", 18))
        self.title_label.pack(side='top', fill='x', pady=10)

        self.auftragsnummer_label = tk.Label(self, text="Auftragsnummer:", font=("Arial", 12))
        self.auftragsnummer_label.pack(side='top', fill='none', anchor = "center")

        self.auftragsnummer_entry = tk.Entry(self, font=("Arial", 12))
        self.auftragsnummer_entry.pack(side='top', pady=10, fill='none', anchor="center")
        self.auftragsnummer_entry.bind("<Button-1>", self.show_auftragsnummer_dialog)

        self.batchnummer_label = tk.Label(self, text="Batchnummer:", font=("Arial", 12))
        self.batchnummer_label.pack(side='top', fill='none', anchor = "center")

        self.batchnummer_entry = tk.Entry(self, font=("Arial", 12))
        self.batchnummer_entry.pack(side='top', pady=10, fill='none', anchor="center")
        self.batchnummer_entry.bind("<Button-1>", self.show_batchnummer_dialog)



        self.von_label = tk.Label(self, text="Von:", font=("Arial", 12))
        self.von_label.pack(side='top', fill='none', anchor = "center")

        self.von_entry = tk.Text(self, state='normal', height=1, width=20, font=("Arial", 12))
        self.von_entry.pack(side='top', fill='none', anchor = "center")
        self.von_entry.bind("<Key>", lambda e: "break")
        self.von_entry.bind("<Button-1>", self.show_von_datepicker)

        self.bis_label = tk.Label(self, text="Bis:", font=("Arial", 12))
        self.bis_label.pack(side='top', fill='none', anchor = "center")

        self.bis_entry = tk.Text(self, state='normal', height=1, width=20, font=("Arial", 12))
        self.bis_entry.pack(side='top', fill='none', anchor = "center")
        self.bis_entry.bind("<Key>", lambda e: "break")
        self.bis_entry.bind("<Button-1>", self.show_bis_datepicker)


        self.upload_button = tk.Button(self, text="PDF hochladen", command=self.upload_pdf, height=2, width=20, font=("Arial", 12))
        self.upload_button.pack(side='top', padx=10, fill='none', anchor = "center", pady=10)

        self.start_button = tk.Button(self, text="Start", command=self.start, height=2, width=20, bg='lightgreen', font=("Arial", 12))
        self.start_button.pack(side='top', padx=10, fill='none', anchor = "center")


        self.download_button = tk.Button(self, text="ZIP herunterladen", command=self.download_pdf, height=2, width=20, font=("Arial", 12))
        self.download_button.pack(side='top', padx=10, fill='none', anchor = "center",pady=10)


        frame = tk.Frame(root)
        self.console_output = tk.Text(frame, width=80, height=20)
        self.scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.console_output.yview)

        self.console_output.configure(yscrollcommand=self.scrollbar.set)
        self.console_output.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        frame.pack(side='top', padx=10, fill='both', expand=True, anchor = "center", pady =10)

###########################################################################
###########################################################################
###### Dialogfelder für Batchnummer und Auftragsnummer
###########################################################################
########################################################################### 
# In diesem Codeblock werden per klick auf die entsprechenden Eingabefelder die Dialogfenster zur Eingabe
# der Batch oder Auftragsnummer geöffnet. Der eingegebene Wert wird anschliessend übertragen.
# Anschliessend wird die Eingabe in der Konsole ausgegeben.

    def show_batchnummer_dialog(self, event):
        dialog = MyDialog(self, "Batchnummer eingeben", "Bitte geben Sie die Batchnummer ein:")
        if dialog.result is not None:
            self.batchnummer_entry.delete(0, tk.END)
            self.batchnummer_entry.insert(0, dialog.result)
            self.console_output.insert(tk.END, f"Batchnummer wurde eingegeben: {dialog.result}\n")


    def show_auftragsnummer_dialog(self, event):
        dialog = MyDialog(self, "Auftragsnummer eingeben", "Bitte geben Sie die Auftragsnummer ein:")
        if dialog.result is not None:
            self.auftragsnummer_entry.delete(0, tk.END)
            self.auftragsnummer_entry.insert(0, dialog.result)
            self.console_output.insert(tk.END, f"Auftragsnummer wurde eingegeben: {dialog.result}\n")

###########################################################################
###########################################################################
###### Datepicker für Datumsfelder
###########################################################################
########################################################################### 
# Beim Klicken in die jeweilgen Felder wird ein Datepicker geöffnet welche das Datum im Format dd.mm.yy in das jeweilige
# Datumsfeld zurückschreibt. Anschliessend wird die Eingabe in der Konsole ausgegeben.

    def show_von_datepicker(self, event):
        def on_date_selected(event):
            # Date String in Datumsformat konvertieren
            selected_date = event.widget.selection_get()
            formatted_date = selected_date.strftime('%d.%m.%y') 
            # Formatiertes Datum in das Feld eintragen
            self.von_entry.delete(1.0, tk.END)  # Löschen des aktuellen Inhalts des Eingabefelds
            self.von_entry.insert(1.0, formatted_date)  # Eintragen des ausgewählten Datums
            self.console_output.insert(tk.END, f"Startdatum wurde eingegeben: {formatted_date}\n")
            calendar_window.destroy()

        calendar_window = tk.Tk()
        calendar = tkcalendar.Calendar(calendar_window, selectmode='day', state='normal')
        # Verwenden von Inhalt von self.bis_entry als formatted_date
        calendar.pack()
        calendar.bind("<<CalendarSelected>>", on_date_selected)


    def show_bis_datepicker(self, event):
        def on_date_selected(event):
            # Date String in Datumsformat konvertieren
            selected_date = event.widget.selection_get()
            formatted_date = selected_date.strftime('%d.%m.%y') 
            # Formatiertes Datum in das Feld eintragen
            self.bis_entry.delete(1.0, tk.END)  # Löschen des aktuellen Inhalts des Eingabefelds
            self.bis_entry.insert(1.0, formatted_date)  # Eintragen des ausgewählten Datums
            self.console_output.insert(tk.END, f"Enddatum wurde eingegeben: {formatted_date}\n")
            calendar_window.destroy()

        calendar_window = tk.Tk()
        calendar = tkcalendar.Calendar(calendar_window, selectmode='day', state='normal')
        # Verwenden vom Inhalt von self.bis_entry als formatted_date
        calendar.pack()
        calendar.bind("<<CalendarSelected>>", on_date_selected)

###########################################################################
###########################################################################
###### Upload und Download
###########################################################################
########################################################################### 
# Mit dem Upload Button kann ein PDF in den import Align Ordner geladen werden. Nach beendigung der Prüfung des 
# Batchrecords wird das gezippte File zum Download bereitgestellt und kann mit dem Download button heruntergeladen werden.

    def download_pdf(self):
        # Verwenden Sie den initialfile-Parameter, um den Namen der Datei anzugeben, die standardmäßig angezeigt werden soll
        filepath = filedialog.asksaveasfilename(initialfile='Batch_'+str(self.auftragsnummer_entry.get())+".zip")
        # ZIP-File herunterladen
        source_directory = "./ZIP/"
        filename = 'Batch_'+str(self.auftragsnummer_entry.get())+".zip"
        shutil.copy(os.path.join(source_directory, filename), filepath)
        self.console_output.insert(tk.END, f"ZIP-File wurde gespeichert: {filepath}\n")

    def upload_pdf(self):
        filepath = filedialog.askopenfilename()
        # PDF Hochladen
        target_directory = './input_ALIGN/'
        # Überprüfen, ob das Zielverzeichnis existiert
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        # Den Dateinamen aus dem Pfad extrahieren und in das Zielverzeichnis kopieren
        filename = os.path.basename(filepath)
        shutil.copy(filepath, os.path.join(target_directory, filename))
        self.console_output.insert(tk.END, f"PDF wurde hochgeladen: {filepath}\n")

        # Dateinamen in Variable Speichern
        self.uploaded_filename = filename

###########################################################################
###########################################################################
###### Start
###########################################################################
########################################################################### 
# Mit dem Startbutton wird die hauptfunktion aus dem Modul MASAM gestartet. 
# Die Eingabewerte der Felder werden in ein CSV geschrieben und später von den einzelnen
# Scripts wieder ausgelesen.

    def start(self):

        batchnummer = self.batchnummer_entry.get()
        auftragsnummer = self.auftragsnummer_entry.get()
        von = self.von_entry.get("1.0", "end")
        bis = self.bis_entry.get("1.0", "end")


        with open('./csv/config.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            von = von.replace("\n", "")
            bis = bis.replace("\n", "")
            writer.writerow([batchnummer])
            writer.writerow([auftragsnummer])
            writer.writerow([von])
            writer.writerow([bis])
            writer.writerow([self.uploaded_filename])
        
        self.show_console_output()

###########################################################################
###########################################################################
###### Konsole
###########################################################################
########################################################################### 
# In der Konsole wird der Output aus den einzelnen Scripts aufgezeigt.

    def show_console_output(self):
        now = datetime.datetime.now()
        Logtime = now.strftime('%d.%m.%y %H:%M:%S')
        self.console_output.insert(tk.END, "Prüfung des Batchrecords wurde gestartet. Bitte warten...\n")
        root.update()
        self.console_output.insert(tk.END, "Startzeit: " + str(Logtime)+"\n")
        root.update()
        self.console_output.insert(tk.END, "Bibliotheken werden importiert...\n")
        root.update()
        customOutput = CustomOutput()
        customOutput.registerOutputFunction(self.sendToConsole)
        import MASAM
        MASAM.mainrun(customOutput)

    
    def sendToConsole(self, text):
        self.console_output.insert(tk.END, text)
        root.update()
        self.console_output.see("end")


###########################################################################
###########################################################################
###### Erstellen der GUI und starten der Applikation
###########################################################################
########################################################################### 

root = tk.Tk()
root.minsize(width=800, height=400)
root.title("Project MASAM")


if __name__ == '__main__':
    app = Application()
    app.mainloop()
