###########################################################################
###########################################################################
###### Imports
###########################################################################
###########################################################################

import BR_config
import os
import zipfile
import sys


###########################################################################
###########################################################################
###### ZIP
###########################################################################
###########################################################################
# Der folgende Codeblock zippt den Ordner EXPORT und stellt ihn zum Download bereit.
auftragsnummer = BR_config.auftragsnummer
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def zipexport(customOutput):
    sys.stdout = customOutput
    zipf = zipfile.ZipFile("./ZIP/Batch_"+str(auftragsnummer)+".zip", 'w', zipfile.ZIP_DEFLATED)
    zipdir("./EXPORT/", zipf)
    zipf.close()
    print("ZIP Datei wurde erstellt: ./EXPORT/", str(zipf))