# -*- coding: utf-8 -*-
__autor__ = "Francesco"
__version__ = "0101 2021/10/12"

import glob
import shutil
from project_lib import *


boold = True
if __name__ == "__main__":
    if boold:
        print("Start")

    head, tail = os.path.split(__file__)
    os.chdir(head)
    percorso = os.getcwd()

    # CONSTANTI
    nomeCartella = get_key_value_JSON('nomeCartella')
    readmeName = get_key_value_JSON('readmeName')
    binName = get_key_value_JSON('binName')
    docName = get_key_value_JSON('docName')
    fileName = get_key_value_JSON('fileName')

    vettFile = glob.glob('*.java')
    for f in vettFile:

        projectName = (f.rsplit(".", 1))[0].capitalize()
        newFileName = shutil.move(f, projectName + ".java")

        # Readme
        headerMd = "# Program name: " + newFileName + "\n" + \
                   "---\n" + \
                   "\n" + \
                   "## Consegna\n _________________"

        exist, perBin, perDoc, perFile, cartella = make_project_dir(
            projectName, nomeCartella, binName, docName, fileName)

        if (not exist == False):
            print(exist)
            break

        filejava = open(perDoc + pathSeparation + readmeName, "w")
        filejava.write(headerMd)
        filejava.close()

        fjava = open(newFileName, "r")
        vRighe = fjava.readlines()
        fjava.close()

        vRighe.append("package " + nomeCartella +
                      projectName + "." + binName + ";\n\n")
        vRighe = rotate(vRighe, -1)

        fjava = open(newFileName, "w")
        fjava.writelines(vRighe)
        fjava.close()

        shutil.move(percorso + "\\" + newFileName, perBin)

    if boold:
        print("End")
