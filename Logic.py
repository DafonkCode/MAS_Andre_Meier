###########################################################################
###########################################################################
###### Imports
###########################################################################
###########################################################################
import BR_config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta
import sys
import shutil

###########################################################################
###########################################################################
###### Settings und Variablen
###########################################################################
###########################################################################
#Settings sind in BR_config.py ersichtlich
#Zurücklesen und transformieren der globalen Variablen
#Debug Variables
# datebegin = "14.09.22"
# dateend = "15.12.22"
# starttime = "05:00:00"
# endtime = "20:00:00"
# auftragsnummer = 40098765
# batchnummer = "ABC2023"
# total_length = 60
# faildate = "01.01.70"
# failtime = "00:00:00"


datebegin = BR_config.datebegin
dateend = BR_config.dateend
starttime = BR_config.starttime
endtime = BR_config.endtime
auftragsnummer = int(BR_config.auftragsnummer)
batchnummer = BR_config.batchnummer
total_length = BR_config.total_length
faildate = BR_config.faildate
failtime = BR_config.failtime
startdate = datetime.strptime(datebegin, "%d.%m.%y")
enddate = datetime.strptime(dateend, "%d.%m.%y")
faildate = datetime.strptime(faildate, "%d.%m.%y")
starttime = datetime.strptime(starttime, '%H:%M:%S').time()
endtime = datetime.strptime(endtime, '%H:%M:%S').time()
failtime = datetime.strptime(failtime, '%H:%M:%S').time()
exportpath = r"./EXPORT/"
exportresultpath = r"./EXPORT/Results/"
exportlogpath = r"./EXPORT/Results/"
comparelist = []

###########################################################################
###########################################################################
###### Printfunction
###########################################################################
###########################################################################
# In diesem Codeblock wird eine Funktion definiert, die drei Argumente erwartet und innerhalb der Funktion 
# eine Zeichenkette erstellt, die als Trenner zwischen dem Namen und dem Erfolgswert dient. Die Länge dieser 
# Zeichenkette wird so berechnet, dass der Name, der Trenner und der Erfolgswert in die Ausgabe passen, die anschließend 
# ausgegeben wird. Zusätzlich wird das Tuple "(name, success)" der Liste "comparelist" hinzugefügt.
def print_result(name, success, total_length):
    name_length = len(name)
    separator = "." * (total_length - name_length - len(str(success)))
    comparelist.append((name, success))
    print(name + separator + str(success))

###########################################################################
###########################################################################
###### Mainlogic
###########################################################################
###########################################################################    
# In diesem Codeblock wird das csv von der auswertung entgegengenommen. Das CSV weist einem Dictionary die jeweiligen Werte den Namen der Variablen zu.
# Die Logik überprüft anschliessend ob das erhaltene Ergebnis valide ist. Wenn ja wird Success mit True markiert, wenn nein mit False. Die einzelnen Successwerte
# werden anschliessend durchgezählt und die Ergebnisse mit dem obigen Printbefehl ausgegeben. Am schluss werden alle Resultate in ein Textfile geschrieben.

def mainlogic(customOutput):
    logres = open(str(exportresultpath)+"Final_Results_"+str(auftragsnummer)+".txt", 'w')
    customOutput.registerOutputFunction(logres.write)
    sys.stdout = customOutput
    global comparelist
    comparelist = []
    print("###################################################")
    print("#Auftragsdaten")
    print("###################################################")
    print("Startdatum: " +str(datebegin))
    print("Enddatum: " +str(dateend))
    print("Auftragsnummer: " +str(auftragsnummer))
    print("Batchnummer: " +str(batchnummer))
    print("Timestamp: "+str(datetime.now()))

    with open("./csv/Batch_"+str(auftragsnummer) +'.csv', "r") as file:
        reader = csv.reader(file)
        values = []
        variables = {}
        for row in reader:
            values.append(row[2])
            variables[row[1]] = row[2]
    for key, value in variables.items():
        if value.isdigit():
            value = int(value)

        elif value == "[]":
            value = 0
        else:
            pass

        variables[key] = value

    print("###################################################")
    print("Seite 1")
    print("###################################################")
    success = False
    true_count = 0
    false_count = 0
    total_true = 0
    total_false = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 
    if variables['p1_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p1_tess_auftragsnummer', success, total_length)

    if variables['p1_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p1_tess_batchnummer', success, total_length)

    if startdate <= datetime.strptime(variables['p1_a1_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p1_a1_datum_1', success, total_length)
        
    if variables['p1_a1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p1_a1_visum_1', success, total_length)

    if startdate <= datetime.strptime(variables['p1_a2_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p1_a2_datum_1', success, total_length)

    if variables['p1_a2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p1_a2_visum_1', success, total_length)

    if startdate <= datetime.strptime(variables['p1_a3_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p1_a3_datum_1', success, total_length)

    if variables['p1_a3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p1_a3_visum_1', success, total_length)

    if variables['p1_a4_checkbox_1'] + variables['p1_a4_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p1_a4_checkbox_1', success, total_length)
    print_result('p1_a4_checkbox_2', success, total_length)

    if startdate <= datetime.strptime(variables['p1_a4_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p1_a4_datum_1', success, total_length)

    if variables['p1_a4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p1_a4_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 2")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 
    if variables['p2_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p2_tess_auftragsnummer', success, total_length)

    if variables['p2_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p2_tess_batchnummer', success, total_length)

    if variables['p2_d1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p2_d1_visum_1', success, total_length)

    number1 = variables['p2_c2_value_1']
    str_number1 = str(number1)
    part = str_number1[:-1]
    try:
        result1 = float(part +"."+ str_number1[-1])     
    except ValueError:
        result1 = 9999.9
    pass

    number2 = variables['p2_c2_value_2']
    str_number2 = str(number2)
    part = str_number2[:-1]
    try:
        result2 = float(part +"."+str_number2[-1])
    except ValueError:
        result1 = 9999.9
    pass

    


    if variables['p2_c2_checkbox_1'] + variables['p2_c2_checkbox_2']+variables['p2_c2_checkbox_3'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p2_c2_checkbox_1', success, total_length)
    print_result('p2_c2_checkbox_2', success, total_length)
    print_result('p2_c2_checkbox_3', success, total_length)


    if variables['p2_c2_checkbox_1'] == 1 and variables['p2_d2_visum_1'] == 1 and variables['p2_d2_visum_2'] == 1 and variables['p2_b4_visum_1'] == 0 and datetime.strptime(variables['p2_a3_datum_1'], "%d.%m.%y")<= faildate and variables['p2_b4_visum_2'] == 0 and variables['p2_d4_visum_1'] ==0 and variables['p2_d4_visum_2'] == 0:
        success = True
        true_count += 6
        
        print_result('p2_d2_visum_1', success, total_length)
        print_result('p2_a3_datum_1', success, total_length)
        print_result('p2_d2_visum_2', success, total_length)
        print_result('p2_b4_visum_1', success, total_length)
        print_result('p2_b4_visum_2', success, total_length)
        print_result('p2_d4_visum_1', success, total_length)
        print_result('p2_d4_visum_2', success, total_length)

    elif variables['p2_c2_checkbox_2'] == 1 and variables['p2_d2_visum_1'] == 1 and variables['p2_d2_visum_2'] == 1 and 1077.7 <= result1 <= 1093.7 and variables['p2_b4_visum_1'] ==1 and startdate <= datetime.strptime(variables['p2_a3_datum_1'], "%d.%m.%y")<= enddate and variables['p2_b4_visum_2'] == 1 and variables['p2_d4_visum_1'] == 1 and variables['p2_d4_visum_2'] == 1:
        success = True
        true_count += 6
        
        print_result('p2_d2_visum_1', success, total_length)
        print_result('p2_a3_datum_1', success, total_length)
        print_result('p2_d2_visum_2', success, total_length)
        print_result('p2_b4_visum_1', success, total_length)
        print_result('p2_b4_visum_2', success, total_length)
        print_result('p2_d4_visum_1', success, total_length)
        print_result('p2_d4_visum_2', success, total_length)


    elif variables['p2_c2_checkbox_3'] == 1 and variables['p2_d2_visum_1'] == 1 and variables['p2_d2_visum_2'] == 1 and 1077.7 <= result2 <= 1093.7 and variables['p2_b4_visum_1'] ==1 and startdate <= datetime.strptime(variables['p2_a3_datum_1'], "%d.%m.%y")<= enddate and variables['p2_b4_visum_2'] == 1 and variables['p2_d4_visum_1'] ==1 and variables['p2_d4_visum_2'] == 1:
        success = True
        true_count += 6
        
        print_result('p2_d2_visum_1', success, total_length)
        print_result('p2_a3_datum_1', success, total_length)
        print_result('p2_d2_visum_2', success, total_length)
        print_result('p2_b4_visum_1', success, total_length)
        print_result('p2_b4_visum_2', success, total_length)
        print_result('p2_d4_visum_1', success, total_length)
        print_result('p2_d4_visum_2', success, total_length)

    else:
        success = False
        false_count += 6
        print_result('p2_d2_visum_1', success, total_length)
        print_result('p2_a3_datum_1', success, total_length)
        print_result('p2_d2_visum_2', success, total_length)
        print_result('p2_b4_visum_1', success, total_length)
        print_result('p2_b4_visum_2', success, total_length)
        print_result('p2_d4_visum_1', success, total_length)
        print_result('p2_d4_visum_2', success, total_length)


    if variables['p2_d3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p2_d3_visum_1', success, total_length)

    if variables['p2_c5_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p2_c5_visum_1', success, total_length)


    if variables['p2_b5_checkbox_1'] + variables['p2_b5_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p2_b5_checkbox_1', success, total_length)
    print_result('p2_b5_checkbox_2', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 3")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 
    if variables['p3_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p3_tess_auftragsnummer', success, total_length)

    if variables['p3_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p3_tess_batchnummer', success, total_length)

    if variables['p3_c1_checkbox_1'] + variables['p3_c1_value_1'] == 2 and variables['p3_c1_checkbox_2'] + variables['p3_c1_value_2'] == 0:
        success = True
        true_count += 4
        print_result('p3_c1_checkbox_1', success, total_length)
        print_result('p3_c1_value_1', success, total_length)
        print_result('p3_c1_checkbox_2', success, total_length)
        print_result('p3_c1_value_2', success, total_length)

    elif variables['p3_c1_checkbox_2'] + variables['p3_c1_value_2'] == 2 and variables['p3_c1_checkbox_1'] + variables['p3_c1_value_1'] == 0:
        success = True
        true_count += 4
        print_result('p3_c1_checkbox_1', success, total_length)
        print_result('p3_c1_value_1', success, total_length)
        print_result('p3_c1_checkbox_2', success, total_length)
        print_result('p3_c1_value_2', success, total_length)
    else:
        success = False
        false_count += 4
        print_result('p3_c1_checkbox_1', success, total_length)
        print_result('p3_c1_value_1', success, total_length)
        print_result('p3_c1_checkbox_2', success, total_length)
        print_result('p3_c1_value_2', success, total_length)

    if variables['p3_d1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p3_d1_visum_1', success, total_length)

    if variables['p3_d2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p3_d2_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 4")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 
    if variables['p4_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p4_tess_auftragsnummer', success, total_length)

    if variables['p4_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p4_tess_batchnummer', success, total_length)

    #------------------------
    #AS 1
    #------------------------
    if startdate <= datetime.strptime(variables['p4_a1_date_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p4_a1_date_1', success, total_length)

    if variables['p4_d1_checkbox_1'] + variables['p4_d1_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p4_d1_checkbox_1', success, total_length)
    print_result('p4_d1_checkbox_2', success, total_length)

    if variables['p4_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p4_e1_visum_1', success, total_length)

    #------------------------
    #AS 2
    #------------------------

    if variables['p4_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p4_e2_visum_1', success, total_length)

    #------------------------
    #AS 3
    #------------------------
    if variables['p4_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p4_e3_visum_1', success, total_length)

    #------------------------
    #AS 4
    #------------------------

    if startdate <= datetime.strptime(variables['p4_a4_date_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p4_a4_date_1', success, total_length)

    if variables['p4_d4_checkbox_1'] + variables['p4_d4_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p4_d4_checkbox_1', success, total_length)
    print_result('p4_d4_checkbox_2', success, total_length)

    if variables['p4_e4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p4_e4_visum_1', success, total_length)

    #------------------------
    #AS 5
    #------------------------

    if variables['p4_d5_checkbox_1'] + variables['p4_d5_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p4_d5_checkbox_1', success, total_length)
    print_result('p4_d5_checkbox_2', success, total_length)

    if variables['p4_d5_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p4_d5_visum_1', success, total_length)


    #------------------------
    #AS 6
    #------------------------

    if variables['p4_d6_checkbox_1'] + variables['p4_d6_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p4_d6_checkbox_1', success, total_length)
    print_result('p4_d6_checkbox_2', success, total_length)

    if variables['p4_e6_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p4_e6_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 5")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 
    if variables['p5_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_tess_auftragsnummer', success, total_length)

    if variables['p5_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_tess_batchnummer', success, total_length)

    #------------------------
    #AS 7
    #------------------------
    if variables['p5_d1_checkbox_1'] + variables['p5_d1_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p5_d1_checkbox_1', success, total_length)
    print_result('p5_d1_checkbox_2', success, total_length)

    if variables['p5_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_e1_visum_1', success, total_length)

    #------------------------
    #AS 8
    #------------------------
    if starttime <= datetime.strptime(variables['p5_a2_time_1'], '%H:%M:%S').time()<= endtime:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_a2_time_1', success, total_length)

    try:
        valueresult = float('.'.join([str(variables['p5_d2_value_1']), str(variables['p5_d2_value_2'])]))
    except ValueError:
        valueresult = 9999.9
    pass
    
    if 6.6 <= float(valueresult) <=7.1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p5_d2_value_1', success, total_length)
    print_result('p5_d2_value_2', success, total_length)

    if variables['p5_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_e2_visum_1', success, total_length)

    #------------------------
    #AS 9
    #------------------------

    if startdate <= datetime.strptime(variables['p5_a3_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_a3_datum_1', success, total_length)


    if starttime <= datetime.strptime(variables['p5_a3_time_1'], '%H:%M:%S').time()<= endtime:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_a3_time_1', success, total_length)


    try:
        valueresult = float('.'.join([str(variables['p5_d3_value_1']), str(variables['p5_d3_value_2'])]))
    except ValueError:
        valueresult = 9999.9
    pass
    if 7.0 <= float(valueresult) <=7.5:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p5_d3_value_1', success, total_length)
    print_result('p5_d3_value_2', success, total_length)

    if variables['p5_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_e3_visum_1', success, total_length)

    if variables['p5_e4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_e4_visum_1', success, total_length)

    #------------------------
    #AS 10 + 11
    #------------------------   

    valueresult = '.'.join([str(variables['p5_d5_value_1']), str(variables['p5_d5_value_2'])])
    if variables['p5_d4_checkbox_2'] == 1 and variables['p5_d4_checkbox_1'] == 0 and variables['p5_e5_visum_1'] == 0 and  datetime.strptime(variables['p5_a5_time_1'], '%H:%M:%S').time() == failtime and variables['p5_d5_value_1'] == 0 and variables['p5_d5_value_2'] == 0:
        success = True
        true_count += 6
        print_result('p5_d4_checkbox_1', success, total_length)
        print_result('p5_d4_checkbox_2', success, total_length)
        print_result('p5_e5_visum_1', success, total_length)
        print_result('p5_a5_time_1', success, total_length)
        print_result('p5_d5_value_1', success, total_length)
        print_result('p5_d5_value_2', success, total_length)
        print("checkbox1")
        print(valueresult)
        print(variables['p5_d5_value_1'])
        print(variables['p5_d5_value_2'])
        

    elif variables['p5_d4_checkbox_1'] == 1 and variables['p5_d4_checkbox_2'] == 0 and variables['p5_e5_visum_1'] == 1 and starttime <= datetime.strptime(variables['p5_a5_time_1'], '%H:%M:%S').time()<= endtime and 7.0 <= float(valueresult) <=7.5:
        success = True
        true_count += 6
        print_result('p5_d4_checkbox_1', success, total_length)
        print_result('p5_d4_checkbox_2', success, total_length)
        print_result('p5_e5_visum_1', success, total_length)
        print_result('p5_a5_time_1', success, total_length)
        print_result('p5_d5_value_1', success, total_length)
        print_result('p5_d5_value_2', success, total_length)
        print("checkbox2")
        print(valueresult)
        print(variables['p5_d5_value_1'])
        print(variables['p5_d5_value_2'])
    else:
        success = False
        false_count += 6
        print_result('p5_d4_checkbox_1', success, total_length)
        print_result('p5_d4_checkbox_2', success, total_length) 
        print_result('p5_e5_visum_1', success, total_length)
        print_result('p5_a5_time_1', success, total_length)
        print_result('p5_d5_value_1', success, total_length)
        print_result('p5_d5_value_2', success, total_length)
        print("checkboxelse")
        print(valueresult)
        print(type(variables['p5_d5_value_1']))
        print(type(variables['p5_d5_value_2']))
 
    #------------------------
    #AS 12 + 13
    #------------------------   
    sevendays = datetime.strptime(variables['p5_a3_datum_1'], "%d.%m.%y") - timedelta(days = 7)

    if sevendays <= datetime.strptime(variables['p5_b6_datum_1'], "%d.%m.%y") <= datetime.strptime(variables['p5_a3_datum_1'], "%d.%m.%y"):
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_b6_datum_1', success, total_length)

    if variables['p5_d6_checkbox_1'] + variables['p5_d6_checkbox_2'] + variables['p5_d6_checkbox_3'] == 1:
        success = True
        true_count += 3
    else:
        success = False
        false_count += 3
    print_result('p5_d6_checkbox_1', success, total_length)
    print_result('p5_d6_checkbox_2', success, total_length)
    print_result('p5_d6_checkbox_3', success, total_length)


    if variables['p5_e6_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_e6_visum_1', success, total_length)

    if variables['p5_d6_checkbox_2'] == 1 and variables['p5_e7_visum_1'] == 1 and datetime.strptime(variables['p5_a7_datum_1'], "%d.%m.%y")==faildate and variables['p5_d7_checkbox_1'] == 0 and variables['p5_d7_checkbox_2'] == 1:
        success = True
        true_count += 4
        
        print_result('p5_e7_visum_1', success, total_length)
        print_result('p5_a7_datum_1', success, total_length)
        print_result('p5_d7_checkbox_1', success, total_length)
        print_result('p5_d7_checkbox_2', success, total_length)

    elif variables['p5_d6_checkbox_1'] == 1 and variables['p5_e7_visum_1'] == 1 and startdate <= datetime.strptime(variables['p5_a7_datum_1'], "%d.%m.%y")<= enddate and variables['p5_d7_checkbox_1'] == 1 and variables['p5_d7_checkbox_2'] == 0:
        success = True
        true_count += 4
        print_result('p5_e7_visum_1', success, total_length)
        print_result('p5_a7_datum_1', success, total_length)
        print_result('p5_d7_checkbox_1', success, total_length)
        print_result('p5_d7_checkbox_2', success, total_length)
        
    elif variables['p5_d6_checkbox_3'] == 1 and variables['p5_e7_visum_1'] == 1 and startdate <= datetime.strptime(variables['p5_a7_datum_1'], "%d.%m.%y")<= enddate and variables['p5_d7_checkbox_1'] == 1 and variables['p5_d7_checkbox_2'] == 0:
        success = True
        true_count += 4
        print_result('p5_e7_visum_1', success, total_length)
        print_result('p5_a7_datum_1', success, total_length)
        print_result('p5_d7_checkbox_1', success, total_length)
        print_result('p5_d7_checkbox_2', success, total_length)
        
    else:
        success = False
        false_count += 4   
        print_result('p5_e7_visum_1', success, total_length)
        print_result('p5_a7_datum_1', success, total_length)
        print_result('p5_d7_checkbox_1', success, total_length)
        print_result('p5_d7_checkbox_2', success, total_length)
        
    #------------------------
    #AS 14
    #------------------------   
    if startdate <= datetime.strptime(variables['p5_a8_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_a8_datum_1', success, total_length)

    if variables['p5_e8_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p5_e8_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count

    print("###################################################")
    print("Seite 6")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p6_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p6_tess_auftragsnummer', success, total_length)

    if variables['p6_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p6_tess_batchnummer', success, total_length)

    #------------------------
    #AS 15
    #------------------------ 

    if startdate <= datetime.strptime(variables['p6_a1_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p6_a1_datum_1', success, total_length)

    if variables['p6_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p6_e1_visum_1', success, total_length)

    #------------------------
    #AS 16
    #------------------------ 

    if variables['p6_d2_checkbox_1'] + variables['p6_d2_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p6_d2_checkbox_1', success, total_length)
    print_result('p6_d2_checkbox_2', success, total_length)

    if variables['p6_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p6_e2_visum_1', success, total_length)

    #------------------------
    #AS 17
    #------------------------ 
    if variables['p6_d3_value_1'] <= 30:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p6_d3_value_1', success, total_length)

    if variables['p6_d3_checkbox_1'] + variables['p6_d3_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p6_d3_checkbox_1', success, total_length)
    print_result('p6_d3_checkbox_2', success, total_length)

    if variables['p6_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p6_e3_visum_1', success, total_length)

    #------------------------
    #AS 18
    #------------------------ 
    if variables['p6_d4_checkbox_1'] + variables['p6_d4_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p6_d4_checkbox_1', success, total_length)
    print_result('p6_d4_checkbox_2', success, total_length)

    if variables['p6_e4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p6_e4_visum_1', success, total_length)

    #------------------------
    #AS 19
    #------------------------  
    if variables['p6_d5_checkbox_1'] == 1 and variables['p6_e5_visum_1'] == 1 and startdate <= datetime.strptime(variables['p6_a5_datum_1'], "%d.%m.%y")==enddate and variables['p6_d5_checkbox_2'] == 0:
        success = True
        true_count += 4
        print_result('p6_d5_checkbox_1', success, total_length)
        print_result('p6_e5_visum_1', success, total_length)
        print_result('p6_a5_datum_1', success, total_length)
        print_result('p6_d5_checkbox_2', success, total_length)

    elif variables['p6_d5_checkbox_2'] == 1 and variables['p6_e5_visum_1'] == 1 and datetime.strptime(variables['p6_a5_datum_1'], "%d.%m.%y")==faildate and variables['p6_d5_checkbox_1'] == 0:
        success = True
        true_count += 4
        print_result('p6_d5_checkbox_1', success, total_length)
        print_result('p6_e5_visum_1', success, total_length)
        print_result('p6_a5_datum_1', success, total_length)
        print_result('p6_d5_checkbox_2', success, total_length)
    
    else:
        success = False
        false_count += 4
        print_result('p6_d5_checkbox_1', success, total_length)
        print_result('p6_e5_visum_1', success, total_length)
        print_result('p6_a5_datum_1', success, total_length)
        print_result('p6_d5_checkbox_2', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 7")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p7_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p7_tess_auftragsnummer', success, total_length)

    if variables['p7_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p7_tess_batchnummer', success, total_length)

    #------------------------
    #AS 20
    #------------------------  
    if startdate <= datetime.strptime(variables['p7_a1_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p7_a1_datum_1', success, total_length)

    if variables['p7_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p7_e1_visum_1', success, total_length)

    #------------------------
    #AS 21
    #------------------------  

    if variables['p7_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p7_e2_visum_1', success, total_length)

    #------------------------
    #AS 22
    #------------------------ 
    if variables['p7_d3_checkbox_1'] + variables['p7_d3_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p7_d3_checkbox_1', success, total_length)
    print_result('p7_d3_checkbox_2', success, total_length)

    if variables['p7_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p7_e3_visum_1', success, total_length)
    
    #------------------------
    #AS 23 + 24
    #------------------------ 
    sevendays = datetime.strptime(variables['p7_a1_datum_1'], "%d.%m.%y") - timedelta(days = 7)
    if variables['p7_d4_checkbox_1'] == 1 and variables['p7_d4_checkbox_2'] + variables['p7_d4_checkbox_3'] == 0 and datetime.strptime(variables['p7_b4_datum_1'], "%d.%m.%y") <= sevendays and variables['p7_e4_visum_1'] == 1 and startdate <= datetime.strptime(variables['p7_a5_datum_1'], "%d.%m.%y") <= enddate and variables['p7_d5_checkbox_1'] == 1 and  variables['p7_d5_checkbox_2'] == 0 and variables['p7_e5_visum_1'] == 1:
        success = True
        true_count += 9
        print_result('p7_d4_checkbox_1', success, total_length)
        print_result('p7_d4_checkbox_2', success, total_length)
        print_result('p7_d4_checkbox_3', success, total_length)
        print_result('p7_b4_datum_1', success, total_length)
        print_result('p7_e4_visum_1', success, total_length)
        print_result('p7_a5_datum_1', success, total_length)
        print_result('p7_d5_checkbox_1', success, total_length)
        print_result('p7_d5_checkbox_2', success, total_length)
        print_result('p7_e5_visum_1', success, total_length)

    elif variables['p7_d4_checkbox_3'] == 1 and variables['p7_d4_checkbox_1'] + variables['p7_d4_checkbox_2'] == 0 and sevendays <= datetime.strptime(variables['p7_b4_datum_1'], "%d.%m.%y") <= datetime.strptime(variables['p7_a1_datum_1'], "%d.%m.%y") and variables['p7_e4_visum_1'] == 1 and startdate <= datetime.strptime(variables['p7_a5_datum_1'], "%d.%m.%y")<=enddate and variables['p7_d5_checkbox_1']== 1 and variables['p7_d5_checkbox_2'] == 0 and variables['p7_e5_visum_1'] == 1:
        success = True
        true_count += 9
        print_result('p7_d4_checkbox_1', success, total_length)
        print_result('p7_d4_checkbox_2', success, total_length)
        print_result('p7_d4_checkbox_3', success, total_length)
        print_result('p7_b4_datum_1', success, total_length)
        print_result('p7_e4_visum_1', success, total_length)
        print_result('p7_a5_datum_1', success, total_length)
        print_result('p7_d5_checkbox_1', success, total_length)
        print_result('p7_d5_checkbox_2', success, total_length)
        print_result('p7_e5_visum_1', success, total_length)


    elif variables['p7_d4_checkbox_2'] == 1 and variables['p7_d4_checkbox_1'] + variables['p7_d4_checkbox_3'] == 0 and sevendays <= datetime.strptime(variables['p7_b4_datum_1'], "%d.%m.%y") <= datetime.strptime(variables['p7_a1_datum_1'], "%d.%m.%y") and variables['p7_e4_visum_1'] == 1 and datetime.strptime(variables['p7_a5_datum_1'], "%d.%m.%y") == faildate and variables['p7_d5_checkbox_1']==0 and variables['p7_d5_checkbox_2'] == 1 and variables['p7_e5_visum_1'] == 1:
        success = True
        true_count += 9
        print_result('p7_d4_checkbox_1', success, total_length)
        print_result('p7_d4_checkbox_2', success, total_length)
        print_result('p7_d4_checkbox_3', success, total_length)
        print_result('p7_b4_datum_1', success, total_length)
        print_result('p7_e4_visum_1', success, total_length)
        print_result('p7_a5_datum_1', success, total_length)
        print_result('p7_d5_checkbox_1', success, total_length)
        print_result('p7_d5_checkbox_2', success, total_length)
        print_result('p7_e5_visum_1', success, total_length)

    else: 
        success = False
        false_count += 9
        print_result('p7_d4_checkbox_1', success, total_length)
        print_result('p7_d4_checkbox_2', success, total_length)
        print_result('p7_d4_checkbox_3', success, total_length)
        print_result('p7_b4_datum_1', success, total_length)
        print_result('p7_e4_visum_1', success, total_length)
        print_result('p7_a5_datum_1', success, total_length)
        print_result('p7_d5_checkbox_1', success, total_length)
        print_result('p7_d5_checkbox_2', success, total_length)
        print_result('p7_e5_visum_1', success, total_length)


    #------------------------
    #AS 25
    #------------------------ 

    if variables['p7_d6_checkbox_1'] + variables['p7_d6_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p7_d6_checkbox_1', success, total_length)
    print_result('p7_d6_checkbox_2', success, total_length)

    if variables['p7_e6_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p7_e6_visum_1', success, total_length)
    #------------------------
    #AS 26
    #------------------------ 

    if variables['p7_e7_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p7_e7_visum_1', success, total_length)

    #------------------------
    #AS 27
    #------------------------ 
    if variables['p7_e8_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p7_e8_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 8")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p8_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p8_tess_auftragsnummer', success, total_length)

    if variables['p8_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p8_tess_batchnummer', success, total_length)  

    #------------------------
    #AS 28
    #------------------------ 

    if variables['p8_d1_checkbox_1'] + variables['p8_d1_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p8_d1_checkbox_1', success, total_length)
    print_result('p8_d1_checkbox_2', success, total_length)

    if variables['p8_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p8_e1_visum_1', success, total_length)

    #------------------------
    #AS 29
    #------------------------ 

    if variables['p8_d2_checkbox_1'] + variables['p8_d2_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p8_d2_checkbox_1', success, total_length)
    print_result('p8_d2_checkbox_2', success, total_length)

    if variables['p8_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p8_e2_visum_1', success, total_length)

    #------------------------
    #AS 30
    #------------------------ 
    if variables['p8_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p8_e3_visum_1', success, total_length)


    #------------------------
    #AS 31
    #------------------------ 
    if variables['p8_e4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p8_e4_visum_1', success, total_length)

    #------------------------
    #AS 32
    #------------------------ 
    if variables['p8_d5_checkbox_1'] + variables['p8_d5_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p8_d5_checkbox_1', success, total_length)
    print_result('p8_d5_checkbox_2', success, total_length)

    if variables['p8_e5_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p8_e5_visum_1', success, total_length)

   #------------------------
    #AS 33, 34, 35
    #------------------------

    if variables['p8_e6_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p8_e6_visum_1', success, total_length)

    if variables['p8_d6_checkbox_1'] == 1 and startdate <= datetime.strptime(variables['p8_a7_datum_1'], "%d.%m.%y") <= enddate and variables['p8_d7_checkbox_1'] == 1 and variables['p8_d7_checkbox_2'] == 0 and variables['p8_e7_visum_1'] == 1:
        success = True
        true_count += 6
        print_result('p8_d6_checkbox_1', success, total_length)
        print_result('p8_a7_datum_1', success, total_length)
        print_result('p8_d7_checkbox_1', success, total_length)
        print_result('p8_d7_checkbox_2', success, total_length)
        print_result('p8_e7_visum_1', success, total_length)

    elif variables['p8_d6_checkbox_1'] == 0 and datetime.strptime(variables['p8_a7_datum_1'], "%d.%m.%y") == faildate and variables['p8_d7_checkbox_1'] == 0 and variables['p8_d7_checkbox_2'] == 1 and variables['p8_e7_visum_1'] == 1:
        success = True
        true_count += 6
        print_result('p8_d6_checkbox_1', success, total_length)
        print_result('p8_a7_datum_1', success, total_length)
        print_result('p8_d7_checkbox_1', success, total_length)
        print_result('p8_d7_checkbox_2', success, total_length)
        print_result('p8_e7_visum_1', success, total_length)
    else:
        success = False
        false_count += 6
        print_result('p8_d6_checkbox_1', success, total_length)
        print_result('p8_d6_checkbox_2', success, total_length)
        print_result('p8_a7_datum_1', success, total_length)
        print_result('p8_d7_checkbox_1', success, total_length)
        print_result('p8_d7_checkbox_2', success, total_length)
        print_result('p8_e7_visum_1', success, total_length)

    
    if variables['p8_d6_checkbox_2'] == 1 and startdate <= datetime.strptime(variables['p8_a8_datum_1'], "%d.%m.%y") <= enddate and variables['p8_d8_checkbox_1'] == 1 and variables['p8_d8_checkbox_2'] == 0 and variables['p8_e8_visum_1'] == 1:
        success = True
        true_count += 6
        
        print_result('p8_d6_checkbox_2', success, total_length)
        print_result('p8_a8_datum_1', success, total_length)
        print_result('p8_d7_checkbox_1', success, total_length)
        print_result('p8_d7_checkbox_2', success, total_length)
        print_result('p8_e7_visum_1', success, total_length)

    elif variables['p8_d6_checkbox_2'] == 0 and datetime.strptime(variables['p8_a8_datum_1'], "%d.%m.%y") == faildate  and variables['p8_d8_checkbox_1'] == 0 and variables['p8_d8_checkbox_2'] == 1 and variables['p8_e8_visum_1'] == 1:
        success = True
        true_count += 6
        
        print_result('p8_d6_checkbox_2', success, total_length)
        print_result('p8_a8_datum_1', success, total_length)
        print_result('p8_d8_checkbox_1', success, total_length)
        print_result('p8_d8_checkbox_2', success, total_length)
        print_result('p8_e8_visum_1', success, total_length)

    else: 
        success = False
        false_count += 6
        print_result('p8_d6_checkbox_1', success, total_length)
        print_result('p8_d6_checkbox_2', success, total_length)
        print_result('p8_a8_datum_1', success, total_length)
        print_result('p8_d8_checkbox_1', success, total_length)
        print_result('p8_d8_checkbox_2', success, total_length)
        print_result('p8_e8_visum_1', success, total_length)

    #------------------------
    #AS 36
    #------------------------ 

    if variables['p8_d9_checkbox_1'] == 1 and variables['p8_d9_checkbox_2'] == 0 and startdate <= datetime.strptime(variables['p8_a9_datum_1'], "%d.%m.%y")<= enddate and variables['p8_e9_visum_1'] == 1:
        success = True
        true_count += 4
        print_result('p8_d9_checkbox_1', success, total_length)
        print_result('p8_d9_checkbox_2', success, total_length)
        print_result('p8_a9_datum_1', success, total_length)
        print_result('p8_e9_visum_1', success, total_length)

    elif variables['p8_d9_checkbox_2'] == 1 and variables['p8_d9_checkbox_1'] == 0 and datetime.strptime(variables['p8_a9_datum_1'], "%d.%m.%y")== faildate and variables['p8_e9_visum_1'] == 1:
        success = True
        true_count += 4
        print_result('p8_d9_checkbox_1', success, total_length)
        print_result('p8_d9_checkbox_2', success, total_length)
        print_result('p8_a9_datum_1', success, total_length)
        print_result('p8_e9_visum_1', success, total_length)
    else:
        success = False
        false_count += 4
        print_result('p8_d9_checkbox_1', success, total_length)
        print_result('p8_d9_checkbox_2', success, total_length)
        print_result('p8_a9_datum_1', success, total_length)
        print_result('p8_e9_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 9")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p9_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p9_tess_auftragsnummer', success, total_length)

    if variables['p9_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p9_tess_batchnummer', success, total_length)  


    #------------------------
    #AS 37
    #------------------------ 

    if variables['p9_d1_checkbox_1'] == 1 and variables['p9_d1_checkbox_2'] == 0 and startdate <= datetime.strptime(variables['p9_a1_datum_1'], "%d.%m.%y")<= enddate and variables['p9_e1_visum_1'] == 1:
        success = True
        true_count += 4
        print_result('p9_d1_checkbox_1', success, total_length)
        print_result('p9_d1_checkbox_2', success, total_length)
        print_result('p9_a1_datum_1', success, total_length)
        print_result('p9_e1_visum_1', success, total_length)

    elif variables['p9_d1_checkbox_2'] == 1 and variables['p9_d1_checkbox_1'] == 0 and datetime.strptime(variables['p9_a1_datum_1'], "%d.%m.%y")== faildate and variables['p9_e1_visum_1'] == 1:
        success = True
        true_count += 4
        print_result('p9_d1_checkbox_1', success, total_length)
        print_result('p9_d1_checkbox_2', success, total_length)
        print_result('p9_a1_datum_1', success, total_length)
        print_result('p9_e1_visum_1', success, total_length)
    else:
        success = False
        false_count += 4
        print_result('p9_d1_checkbox_1', success, total_length)
        print_result('p9_d1_checkbox_2', success, total_length)
        print_result('p9_a1_datum_1', success, total_length)
        print_result('p9_e1_visum_1', success, total_length)

    #------------------------
    #AS 38
    #------------------------ 
    valueresult = '.'.join([str(variables['p9_d2_value_1']), str(variables['p9_d2_value_2'])])
    
    if startdate <= datetime.strptime(variables['p9_a2_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p9_a2_datum_1', success, total_length)

    if 8.2 <= float(valueresult) <=9.0:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p9_d2_value_1', success, total_length)
    print_result('p9_d2_value_2', success, total_length)

    if variables['p9_d2_checkbox_1'] + variables['p9_d2_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p9_d2_checkbox_1', success, total_length)
    print_result('p9_d2_checkbox_2', success, total_length)

    if variables['p9_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p9_e2_visum_1', success, total_length)

    #------------------------
    #AS 39
    #------------------------ 
    if variables['p9_d3_checkbox_1'] + variables['p9_d3_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p9_d3_checkbox_1', success, total_length)
    print_result('p9_d3_checkbox_2', success, total_length)

    if variables['p9_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p9_e3_visum_1', success, total_length)

    #------------------------
    #AS 40
    #------------------------ 
    if variables['p9_d4_checkbox_1'] + variables['p9_d4_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p9_d4_checkbox_1', success, total_length)
    print_result('p9_d4_checkbox_2', success, total_length)

    if variables['p9_e4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p9_e4_visum_1', success, total_length)

    #------------------------
    #AS 41
    #------------------------ 
    if variables['p9_d5_checkbox_1'] + variables['p9_d5_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p9_d5_checkbox_1', success, total_length)
    print_result('p9_d5_checkbox_2', success, total_length)

    if variables['p9_e5_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p9_e5_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 10")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p10_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p10_tess_auftragsnummer', success, total_length)

    if variables['p10_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p10_tess_batchnummer', success, total_length)  


    if variables['p10_c1_visum_1'] + variables['p10_c1_visum_2'] == 2:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p10_c1_visum_1', success, total_length)
    print_result('p10_c1_visum_2', success, total_length)

    if variables['p10_d1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p10_d1_visum_1', success, total_length)


    if variables['p10_c2_visum_1'] + variables['p10_c2_visum_2'] == 2:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p10_c2_visum_1', success, total_length)
    print_result('p10_c2_visum_2', success, total_length)

    if variables['p10_d2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p10_d2_visum_1', success, total_length)

    if variables['p10_c3_visum_1'] + variables['p10_c3_visum_2'] == 2:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p10_c3_visum_1', success, total_length)
    print_result('p10_c3_visum_2', success, total_length)

    if variables['p10_d3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p10_d3_visum_1', success, total_length)

    
    if variables['p10_b4_checkbox_1'] + variables['p10_b4_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p10_b4_checkbox_1', success, total_length)
    print_result('p10_b4_checkbox_2', success, total_length)

    if variables['p10_c4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p10_c4_visum_1', success, total_length)

    if variables['p10_c5_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p10_c5_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 11")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p11_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p11_tess_auftragsnummer', success, total_length)

    if variables['p11_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p11_tess_batchnummer', success, total_length)  

    #------------------------
    #AS42
    #------------------------ 

    if startdate <= datetime.strptime(variables['p11_a1_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p11_a1_datum_1', success, total_length)

    if variables['p11_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p11_e1_visum_1', success, total_length)

    #------------------------
    #AS43
    #------------------------ 
    
    if variables['p11_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p11_e2_visum_1', success, total_length)


    if variables['p11_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p11_e3_visum_1', success, total_length)


    #------------------------
    #AS44, 45, 46
    #------------------------ 

    if variables['p11_d3_checkbox_1'] == 1 and startdate <= datetime.strptime(variables['p11_a3_datum_1'], "%d.%m.%y") <= enddate and starttime <= datetime.strptime(variables['p11_a4_time_1'], '%H:%M:%S').time() <= endtime and variables['p11_d4_checkbox_1'] == 1 and variables['p11_d4_checkbox_2'] == 0 and variables['p11_e4_visum_1'] == 1:
        success = True
        true_count += 6
        print_result('p11_d3_checkbox_1', success, total_length)
        print_result('p11_a3_datum_1', success, total_length)
        print_result('p11_a4_time_1', success, total_length)
        print_result('p11_d4_checkbox_1', success, total_length)
        print_result('p11_d4_checkbox_2', success, total_length)
        print_result('p11_e4_visum_1', success, total_length)

    elif variables['p11_d3_checkbox_1'] == 0 and datetime.strptime(variables['p11_a3_datum_1'], "%d.%m.%y") == faildate and datetime.strptime(variables['p11_a4_time_1'], '%H:%M:%S').time() == failtime and variables['p11_d4_checkbox_1'] == 0 and variables['p11_d4_checkbox_2'] == 1 and variables['p11_e4_visum_1'] == 1:
        success = True
        true_count += 6
        print_result('p11_d3_checkbox_1', success, total_length)
        print_result('p11_a3_datum_1', success, total_length)
        print_result('p11_a4_time_1', success, total_length)
        print_result('p11_d4_checkbox_1', success, total_length)
        print_result('p11_d4_checkbox_2', success, total_length)
        print_result('p11_e4_visum_1', success, total_length)

    else: 
        success = False
        false_count += 6
        print_result('p11_d3_checkbox_1', success, total_length)
        print_result('p11_a3_datum_1', success, total_length)
        print_result('p11_a4_time_1', success, total_length)
        print_result('p11_d4_checkbox_1', success, total_length)
        print_result('p11_d4_checkbox_2', success, total_length)
        print_result('p11_e4_visum_1', success, total_length)


    if variables['p11_d3_checkbox_2'] == 1 and startdate <= datetime.strptime(variables['p11_a5_datum_1'], "%d.%m.%y") <= enddate and starttime <= datetime.strptime(variables['p11_a5_time_1'], '%H:%M:%S').time() <= endtime and variables['p11_d5_checkbox_1'] == 1 and variables['p11_d5_checkbox_2'] == 0 and variables['p11_e5_visum_1'] == 1:
        success = True
        true_count += 6
        print_result('p11_d3_checkbox_2', success, total_length)
        print_result('p11_a5_datum_1', success, total_length)
        print_result('p11_a5_time_1', success, total_length)
        print_result('p11_d5_checkbox_1', success, total_length)
        print_result('p11_d5_checkbox_2', success, total_length)
        print_result('p11_e5_visum_1', success, total_length)

    elif variables['p11_d3_checkbox_2'] == 0 and datetime.strptime(variables['p11_a5_datum_1'], "%d.%m.%y") == faildate and datetime.strptime(variables['p11_a5_time_1'], '%H:%M:%S').time() == failtime and variables['p11_d5_checkbox_1'] == 0 and variables['p11_d5_checkbox_2'] == 1 and variables['p11_e5_visum_1'] == 1:
        success = True
        true_count += 6
        print_result('p11_d3_checkbox_2', success, total_length)
        print_result('p11_a5_datum_1', success, total_length)
        print_result('p11_a5_time_1', success, total_length)
        print_result('p11_d5_checkbox_1', success, total_length)
        print_result('p11_d5_checkbox_2', success, total_length)
        print_result('p11_e5_visum_1', success, total_length)

    else: 
        success = False
        false_count += 6
        print_result('p11_d3_checkbox_2', success, total_length)
        print_result('p11_a5_datum_1', success, total_length)
        print_result('p11_a5_time_1', success, total_length)
        print_result('p11_d5_checkbox_1', success, total_length)
        print_result('p11_d5_checkbox_2', success, total_length)
        print_result('p11_e5_visum_1', success, total_length)


    #------------------------
    #AS47 -52
    #------------------------ 
    
    if variables['p11_e6_visum_1'] + variables['p11_e7_visum_1'] +variables['p11_e8_visum_1'] +variables['p11_e9_visum_1'] +variables['p11_e10_visum_1'] + variables['p11_e11_visum_1'] == 0 or variables['p11_e6_visum_1'] + variables['p11_e7_visum_1'] +variables['p11_e8_visum_1'] +variables['p11_e9_visum_1'] +variables['p11_e10_visum_1'] + variables['p11_e11_visum_1'] == 6:
        success = True
        true_count += 6
    else:
        success = False
        false_count += 6
    print_result('p11_e6_visum_1', success, total_length)
    print_result('p11_e7_visum_1', success, total_length)
    print_result('p11_e8_visum_1', success, total_length)
    print_result('p11_e9_visum_1', success, total_length)
    print_result('p11_e10_visum_1', success, total_length)
    print_result('p11_e11_visum_1', success, total_length)

    #------------------------
    #AS53
    #------------------------ 
    if startdate <= datetime.strptime(variables['p11_a12_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p11_a12_datum_1', success, total_length)

    if variables['p11_e12_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p11_e12_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 12")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p12_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p12_tess_auftragsnummer', success, total_length)

    if variables['p12_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p12_tess_batchnummer', success, total_length)  


    #------------------------
    #AS54
    #------------------------ 
    if variables['p12_d1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p12_d1_visum_1', success, total_length)

    #------------------------
    #AS55
    #------------------------ 
    if variables['p12_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p12_e2_visum_1', success, total_length)

    #------------------------
    #AS56
    #------------------------ 
    if variables['p12_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p12_e3_visum_1', success, total_length)


    if variables['p12_a4_checkbox_1'] + variables['p12_a4_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p12_a4_checkbox_1', success, total_length)
    print_result('p12_a4_checkbox_2', success, total_length)

    #------------------------
    #AS 57 - 60
    #------------------------ 
    if variables['p12_a4_checkbox_1'] == 1 and variables['p12_a4_checkbox_2'] == 0 and variables['p12_a5_checkbox_1'] == 0 and variables['p12_a5_checkbox_2'] == 0 and variables['p12_a5_checkbox_3'] == 0 and variables['p12_e6_visum_1'] + variables['p12_e7_visum_1'] + variables['p12_e8_visum_1'] + variables['p12_e9_visum_1'] == 0:
        success = True
        true_count += 7
        print_result('p12_a5_checkbox_1', success, total_length)
        print_result('p12_a5_checkbox_2', success, total_length)
        print_result('p12_a5_checkbox_3', success, total_length)
        print_result('p12_e6_visum_1', success, total_length)
        print_result('p12_e7_visum_1', success, total_length)
        print_result('p12_e8_visum_1', success, total_length)
        print_result('p12_e9_visum_1', success, total_length)

    elif variables['p12_a4_checkbox_2'] == 1 and  variables['p12_a4_checkbox_1'] == 0 and variables['p12_a5_checkbox_1'] == 1 and variables['p12_a5_checkbox_2'] == 0 and variables['p12_a5_checkbox_3'] == 0 and variables['p12_e6_visum_1'] == 1 and variables['p12_e7_visum_1'] == 1 and variables['p12_e8_visum_1'] == 1 and variables['p12_e9_visum_1'] == 1:
        success = True
        true_count += 7
        print_result('p12_a5_checkbox_1', success, total_length)
        print_result('p12_a5_checkbox_2', success, total_length)
        print_result('p12_a5_checkbox_3', success, total_length)
        print_result('p12_e6_visum_1', success, total_length)
        print_result('p12_e7_visum_1', success, total_length)
        print_result('p12_e8_visum_1', success, total_length)
        print_result('p12_e9_visum_1', success, total_length)

    elif variables['p12_a4_checkbox_2'] == 1 and  variables['p12_a4_checkbox_1'] == 0 and variables['p12_a5_checkbox_1'] == 0 and variables['p12_a5_checkbox_2'] == 1 and variables['p12_a5_checkbox_3'] == 0 and variables['p12_e6_visum_1'] + variables['p12_e7_visum_1'] == 0 and variables['p12_e8_visum_1'] == 1 and variables['p12_e9_visum_1'] == 1:
        success = True
        true_count += 7
        print_result('p12_a5_checkbox_1', success, total_length)
        print_result('p12_a5_checkbox_2', success, total_length)
        print_result('p12_a5_checkbox_3', success, total_length)
        print_result('p12_e6_visum_1', success, total_length)
        print_result('p12_e7_visum_1', success, total_length)
        print_result('p12_e8_visum_1', success, total_length)
        print_result('p12_e9_visum_1', success, total_length)

    elif variables['p12_a4_checkbox_2'] == 1 and  variables['p12_a4_checkbox_1'] == 0 and variables['p12_a5_checkbox_1'] == 0 and variables['p12_a5_checkbox_2'] == 0 and variables['p12_a5_checkbox_3'] == 1 and variables['p12_e6_visum_1'] + variables['p12_e7_visum_1'] + variables['p12_e8_visum_1'] == 0 and variables['p12_e9_visum_1'] == 1:
        success = True
        true_count += 7
        print_result('p12_a5_checkbox_1', success, total_length)
        print_result('p12_a5_checkbox_2', success, total_length)
        print_result('p12_a5_checkbox_3', success, total_length)    
        print_result('p12_e6_visum_1', success, total_length)
        print_result('p12_e7_visum_1', success, total_length)
        print_result('p12_e8_visum_1', success, total_length)
        print_result('p12_e9_visum_1', success, total_length)
    else: 
        success = False
        false_count += 7
        print_result('p12_a5_checkbox_1', success, total_length)
        print_result('p12_a5_checkbox_2', success, total_length)
        print_result('p12_a5_checkbox_3', success, total_length)
        print_result('p12_e6_visum_1', success, total_length)
        print_result('p12_e7_visum_1', success, total_length)
        print_result('p12_e8_visum_1', success, total_length)
        print_result('p12_e9_visum_1', success, total_length)

    #------------------------
    #AS61
    #------------------------ 
    if variables['p12_e10_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p12_e10_visum_1', success, total_length)

    #------------------------
    #AS62
    #------------------------ 
    if variables['p12_e11_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p12_e11_visum_1', success, total_length)


    #------------------------
    #AS63
    #------------------------ 
    if startdate <= datetime.strptime(variables['p12_a12_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p12_a12_datum_1', success, total_length)

    if variables['p12_d13_checkbox_1'] + variables['p12_d13_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p12_d13_checkbox_1', success, total_length)
    print_result('p12_d13_checkbox_2', success, total_length)

    if variables['p12_e13_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p12_e13_visum_1', success, total_length)

    #------------------------
    #AS64
    #------------------------ 

    if variables['p12_d14_checkbox_1'] + variables['p12_d14_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p12_d14_checkbox_1', success, total_length)
    print_result('p12_d14_checkbox_2', success, total_length)

    if variables['p12_e14_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p12_e14_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 13")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p13_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p13_tess_auftragsnummer', success, total_length)

    if variables['p13_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p13_tess_batchnummer', success, total_length)  

    #------------------------
    #AS65 + 66
    #------------------------ 
    if variables['p12_d14_checkbox_1'] == 1 and variables['p13_e1_visum_1'] + variables['p13_e2_visum_1'] + variables['p13_e2_visum_2'] == 0 :
        success = True
        true_count += 3
        print_result('p13_e1_visum_1', success, total_length)
        print_result('p13_e2_visum_1', success, total_length)
        print_result('p13_e2_visum_2', success, total_length)

    elif variables['p12_d14_checkbox_2'] == 1 and variables['p13_e1_visum_1'] == 1 and variables['p13_e2_visum_1'] ==1 and variables['p13_e2_visum_2'] == 1 :
        success = True
        true_count += 3
        print_result('p13_e1_visum_1', success, total_length)
        print_result('p13_e2_visum_1', success, total_length)
        print_result('p13_e2_visum_2', success, total_length)
    
    else:
        success = False
        false_count += 3
        print_result('p13_e1_visum_1', success, total_length)
        print_result('p13_e2_visum_1', success, total_length)
        print_result('p13_e2_visum_2', success, total_length)


    #------------------------
    #AS67
    #------------------------ 

    if variables['p13_d3_checkbox_1'] + variables['p13_d3_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p13_d3_checkbox_1', success, total_length)
    print_result('p13_d3_checkbox_2', success, total_length)

    if variables['p13_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p13_e3_visum_1', success, total_length)


    #------------------------
    #AS68
    #------------------------
    if variables['p13_e4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p13_e4_visum_1', success, total_length)


    #------------------------
    #AS69
    #------------------------ 

    if variables['p13_d5_checkbox_1'] + variables['p13_d5_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p13_d5_checkbox_1', success, total_length)
    print_result('p13_d5_checkbox_2', success, total_length)

    if variables['p13_e5_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p13_e5_visum_1', success, total_length)



    #------------------------
    #AS70
    #------------------------ 

    if startdate <= datetime.strptime(variables['p13_a6_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p13_a6_datum_1', success, total_length)

    if variables['p13_d6_checkbox_1'] + variables['p13_d6_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p13_d6_checkbox_1', success, total_length)
    print_result('p13_d6_checkbox_2', success, total_length)


    if variables['p13_e6_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p13_e6_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 14")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p14_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_tess_auftragsnummer', success, total_length)

    if variables['p14_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_tess_batchnummer', success, total_length)  


    #------------------------
    #AS71
    #------------------------ 
    if variables['p14_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_e1_visum_1', success, total_length)


    #------------------------
    #AS72
    #------------------------ 
    if variables['p14_d2_checkbox_1'] + variables['p14_d2_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p14_d2_checkbox_1', success, total_length)
    print_result('p14_d2_checkbox_2', success, total_length)


    if variables['p14_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_e2_visum_1', success, total_length)


    #------------------------
    #AS73
    #------------------------ 
    if variables['p14_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_e3_visum_1', success, total_length)



    #------------------------
    #AS74
    #------------------------ 
    if variables['p14_d4_checkbox_1'] + variables['p14_d4_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p14_d4_checkbox_1', success, total_length)
    print_result('p14_d4_checkbox_2', success, total_length)


    if variables['p14_e4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_e4_visum_1', success, total_length)

    #------------------------
    #AS75
    #------------------------ 
    if variables['p14_d5_checkbox_1'] + variables['p14_d5_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p14_d5_checkbox_1', success, total_length)
    print_result('p14_d5_checkbox_2', success, total_length)


    if variables['p14_e5_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_e5_visum_1', success, total_length)


    #------------------------
    #AS76
    #------------------------ 
    if variables['p14_d6_checkbox_1'] + variables['p14_d6_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p14_d6_checkbox_1', success, total_length)
    print_result('p14_d6_checkbox_2', success, total_length)


    if variables['p14_e6_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_e6_visum_1', success, total_length)


    #------------------------
    #AS77
    #------------------------

    if startdate <= datetime.strptime(variables['p14_a7_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_a7_datum_1', success, total_length)


    if starttime <= datetime.strptime(variables['p14_a7_time_1'], '%H:%M:%S').time()<= endtime:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_a7_time_1', success, total_length)

    if variables['p14_d7_value_1'] >= 15:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_d7_value_1', success, total_length)

    if variables['p14_e7_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_e7_visum_1', success, total_length)



    #------------------------
    #AS78
    #------------------------

    if variables['p14_e8_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p14_e8_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 15")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p15_tess_Auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p15_tess_Auftragsnummer', success, total_length)

    if variables['p15_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p15_tess_batchnummer', success, total_length)  


    if variables['p15_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p15_e1_visum_1', success, total_length)

    if variables['p15_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p15_e2_visum_1', success, total_length)

    if variables['p15_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p15_e3_visum_1', success, total_length)

    if variables['p15_e4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p15_e4_visum_1', success, total_length)

    if variables['p15_e5_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p15_e5_visum_1', success, total_length)

    if variables['p15_e6_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p15_e6_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)

    total_true = total_true + true_count
    total_false = total_false + false_count   
    print("###################################################")
    print("Seite 16")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p16_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p16_tess_auftragsnummer', success, total_length)

    if variables['p16_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p16_tess_batchnummer', success, total_length)  


    #------------------------
    #AS 79
    #------------------------ 
    if startdate <= datetime.strptime(variables['p16_a1_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p16_a1_datum_1', success, total_length)

    if variables['p16_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p16_e1_visum_1', success, total_length)


    #------------------------
    #AS 80
    #------------------------ 
    if variables['p16_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p16_e2_visum_1', success, total_length)


    #------------------------
    #AS 81
    #------------------------ 
    if variables['p16_d3_checkbox_1'] + variables['p16_d3_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p16_d3_checkbox_1', success, total_length)
    print_result('p16_d3_checkbox_2', success, total_length)


    if variables['p16_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p16_e3_visum_1', success, total_length)


    #------------------------
    #AS 82
    #------------------------ 
    if variables['p16_e4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p16_e4_visum_1', success, total_length)

    #------------------------
    #AS 83
    #------------------------ 
    if variables['p16_e5_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p16_e5_visum_1', success, total_length)

    if 25 - variables['p16_d6_value_1'] - variables['p16_d6_value_2'] == variables['p16_d6_value_3']:
        success = True
        true_count += 3
    else:
        success = False
        false_count += 3
    print_result('p16_d6_value_1', success, total_length)
    print_result('p16_d6_value_2', success, total_length)
    print_result('p16_d6_value_3', success, total_length)


    if variables['p16_d6_checkbox_1'] + variables['p16_d6_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p16_d6_checkbox_1', success, total_length)
    print_result('p16_d6_checkbox_2', success, total_length)

    if variables['p16_d6_checkbox_1'] == 1 and variables['p16_e6_visum_1'] == 1 and variables['p16_e7_visum_1'] + variables['p16_e8_visum_1'] + variables['p16_e9_visum_1'] == 0 and datetime.strptime(variables['p16_a8_datum_1'], "%d.%m.%y")==faildate and variables['p16_d9_checkbox_1'] + variables['p16_d9_checkbox_2'] == 0:
        success = True
        true_count += 7
        
        print_result('p16_e6_visum_1', success, total_length)
        print_result('p16_e7_visum_1', success, total_length)
        print_result('p16_e8_visum_1', success, total_length)
        print_result('p16_e9_visum_1', success, total_length)
        print_result('p16_a8_datum_1', success, total_length)
        print_result('p16_d9_checkbox_1', success, total_length)
        print_result('p16_d9_checkbox_2', success, total_length)
 
    elif variables['p16_d6_checkbox_2'] == 1 and variables['p16_e6_visum_1'] == 1 and variables['p16_e7_visum_1'] == 1 and variables['p16_e8_visum_1'] == 1 and variables['p16_e9_visum_1'] == 1 and startdate <= datetime.strptime(variables['p16_a8_datum_1'], "%d.%m.%y")<=enddate and variables['p16_d9_checkbox_1'] + variables['p16_d9_checkbox_2'] == 1:
        success = True
        true_count += 7
        print_result('p16_e6_visum_1', success, total_length)
        print_result('p16_e7_visum_1', success, total_length)
        print_result('p16_e8_visum_1', success, total_length)
        print_result('p16_a8_datum_1', success, total_length)
        print_result('p16_e9_visum_1', success, total_length)
        print_result('p16_d9_checkbox_1', success, total_length)
        print_result('p16_d9_checkbox_2', success, total_length)

    else:
        success = False
        false_count += 7
        print_result('p16_e6_visum_1', success, total_length)
        print_result('p16_e7_visum_1', success, total_length)
        print_result('p16_e8_visum_1', success, total_length)
        print_result('p16_a8_datum_1', success, total_length)
        print_result('p16_e9_visum_1', success, total_length)
        print_result('p16_d9_checkbox_1', success, total_length)
        print_result('p16_d9_checkbox_2', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 17")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p17_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p17_tess_auftragsnummer', success, total_length)

    if variables['p17_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p17_tess_batchnummer', success, total_length)  

    #------------------------
    #AS 88 
    #------------------------ 
    if startdate <= datetime.strptime(variables['p17_a1_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p17_a1_datum_1', success, total_length)

    if starttime <= datetime.strptime(variables['p17_a1_time_1'], '%H:%M:%S').time()<= endtime:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p17_a1_time_1', success, total_length)

    if variables['p17_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p17_e1_visum_1', success, total_length)

    #------------------------
    #AS 89
    #------------------------ 
    if variables['p17_e2_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p17_e2_visum_1', success, total_length)


    #------------------------
    #AS 90
    #------------------------ 
    if variables['p17_e3_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p17_e3_visum_1', success, total_length)


    #------------------------
    #AS 91
    #------------------------ 
    if variables['p17_e4_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p17_e4_visum_1', success, total_length)

    #------------------------
    #AS 92
    #------------------------ 
    if variables['p17_d5_value_1'] - variables['p17_d5_value_2'] - variables['p17_d5_value_3'] -variables['p17_d5_value_4'] -variables['p17_d5_value_5'] == variables['p17_d5_value_6']:
        success = True
        true_count += 6
    else:
        success = False
        false_count += 6
    print_result('p17_d5_value_1', success, total_length)
    print_result('p17_d5_value_2', success, total_length)
    print_result('p17_d5_value_3', success, total_length)
    print_result('p17_d5_value_4', success, total_length)
    print_result('p17_d5_value_5', success, total_length)
    print_result('p17_d5_value_6', success, total_length)

    if variables['p17_e5_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p17_e5_visum_1', success, total_length)


    #------------------------
    #AS 93 
    #------------------------ 
    if startdate <= datetime.strptime(variables['p17_a6_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p17_a6_datum_1', success, total_length)

    #------------------------
    #AS 91
    #------------------------ 
    if variables['p17_e6_visum_1'] + variables['p17_e6_visum_2'] == 2:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p17_e6_visum_1', success, total_length)
    print_result('p17_e6_visum_2', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    print("###################################################")
    print("Seite 18")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p18_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p18_tess_auftragsnummer', success, total_length)

    if variables['p18_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p18_tess_batchnummer', success, total_length)

    valuelist1 = [str(variables['p18_value_1']), str(variables['p18_value_2']), str(variables['p18_value_3']), str(variables['p18_value_4']), str(variables['p18_value_5'])]
    value_string1 = ''.join(valuelist1)
    modified_string = value_string1[:-1] + "." + value_string1[-1] if len(value_string1) > 1 else value_string1
    value1 = float(modified_string)

    valuelist2 = [str(variables['p18_value_6']), str(variables['p18_value_7']), str(variables['p18_value_8'])]
    value_string2 = ''.join(valuelist2)
    modified_string2 = value_string2[:-1] + "." + value_string2[-1] if len(value_string2) > 1 else value_string2
    value2 = float(modified_string2)

    valuelist3 = [str(variables['p18_value_9']), str(variables['p18_value_10'])]
    value_string3 = ''.join(valuelist3)
    value3 =  int(value_string3)
    berechnung = int((value1 * value2)//270.7)
    if berechnung == value3 and 70 <= berechnung <=100:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('Ausbeuteberechnung', success, total_length)


    if startdate <= datetime.strptime(variables['p18_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p18_datum_1', success, total_length)

    if variables['p18_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p18_visum_1', success, total_length)


    if startdate <= datetime.strptime(variables['p18_datum_2'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p18_datum_2', success, total_length)

    if variables['p18_visum_2'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p18_visum_2', success, total_length)


    #------------------------
    #AS 94
    #------------------------ 
    if startdate <= datetime.strptime(variables['p18_a1_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p18_a1_datum_1', success, total_length)

    if variables['p18_d1_checkbox_1'] + variables['p18_d1_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p18_d1_checkbox_1', success, total_length)
    print_result('p18_d1_checkbox_2', success, total_length)

    if variables['p18_e1_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p18_e1_visum_1', success, total_length)

    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count
    
    print("###################################################")
    print("Seite 19")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p19_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p19_tess_auftragsnummer', success, total_length)

    if variables['p19_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p19_tess_batchnummer', success, total_length)

    if variables['p19_b1_checkbox_1'] + variables['p19_b1_checkbox_2'] == 1:
        success = True
        true_count += 2
    else:
        success = False
        false_count += 2
    print_result('p19_b1_checkbox_1', success, total_length)
    print_result('p19_b1_checkbox_2', success, total_length)


    if startdate <= datetime.strptime(variables['p19_datum_1'], "%d.%m.%y")<= enddate:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p19_datum_1', success, total_length)

    if variables['p19_visum_1'] == 1:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p19_visum_1', success, total_length)
    print("###################################################")
    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count

    print("###################################################")
    print("Seite 20")
    print("###################################################")
    true_count = 0
    false_count = 0
    #------------------------
    #Batch und Auftragsnummer
    #------------------------ 

    if variables['p20_tess_auftragsnummer'] == auftragsnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p20_tess_auftragsnummer', success, total_length)

    if variables['p20_tess_batchnummer'] == batchnummer:
        success = True
        true_count += 1
    else:
        success = False
        false_count += 1
    print_result('p20_tess_batchnummer', success, total_length)


    if variables['p20_a1_checkbox_1'] + variables['p20_a1_checkbox_2'] + variables['p20_a1_checkbox_3'] + variables['p20_a1_checkbox_4'] +variables['p20_a1_checkbox_5'] + variables['p20_b1_checkbox_1'] + variables['p20_b1_checkbox_2'] + variables['p20_b1_checkbox_3'] + variables['p20_b1_checkbox_4'] + variables['p20_b1_checkbox_5'] == 10:
        success = True
        true_count += 10
    else:
        success = False
        false_count += 10
    print_result('p20_a1_checkbox_1', success, total_length)
    print_result('p20_a1_checkbox_2', success, total_length)
    print_result('p20_a1_checkbox_3', success, total_length)
    print_result('p20_a1_checkbox_4', success, total_length)
    print_result('p20_a1_checkbox_5', success, total_length)
    print_result('p20_b1_checkbox_1', success, total_length)
    print_result('p20_b1_checkbox_2', success, total_length)
    print_result('p20_b1_checkbox_3', success, total_length)
    print_result('p20_b1_checkbox_4', success, total_length)
    print_result('p20_b1_checkbox_5', success, total_length)


    print("True count: ", true_count)
    print("False count: ", false_count)
    total_true = total_true + true_count
    total_false = total_false + false_count

    print("###################################################")
    print("Total counts")
    print("###################################################")   
    print("Total True: ", total_true)
    print("Total False: ", total_false)
    print("###################################################")
    

    # Pfad der CSV-Datei
    original_file = "./csv/Batch_"+str(auftragsnummer)+".csv"

    # Pfad des Zielordners
    destination_folder = './EXPORT/Results/'

    # Verschieben der Datei von dem ursprünglichen Ordner zum Zielordner
    shutil.move(original_file, destination_folder)

    customOutput.unregisterOutputFunction(logres.write)
    logres.close()