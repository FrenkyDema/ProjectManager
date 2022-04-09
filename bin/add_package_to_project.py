# -*- coding: utf-8 -*-
__autor__ = "Francesco"
__version__ = "0101 2021/11/30"

from project_lib import *


exist = False
percorso, tail = os.path.split(__file__)
os.chdir(percorso)

boold = True
if __name__ == '__main__':
    if boold:
        print("Start")
    # CONSTANTI
    nomeCartella = get_key_value_JSON('nomeCartella')
    readmeName = get_key_value_JSON('readmeName')
    binName = get_key_value_JSON('binName')
    docName = get_key_value_JSON('docName')
    fileName = get_key_value_JSON('fileName')

    projectListDir = os.listdir()

    for directory in projectListDir:
        if isdir(directory) and directory.startswith(nomeCartella):
            package = "package " + directory + "." + binName + ";\n"
            directory += "/" + binName + "/"
            if isdir(directory):
                for javaFilePath in os.listdir(directory):
                    javaFilePath = directory + javaFilePath
                    if isfile(javaFilePath) and javaFilePath.endswith(".java"):

                        javaFile = open(javaFilePath, "r", )
                        listLines = javaFile.readlines()
                        javaFile.close()

                        if package not in listLines:
                            print(javaFilePath)
                            listLines.insert(0, package + "\n")
                            javaFile = open(javaFilePath, "w", )
                            listLines = javaFile.writelines(listLines)
                            javaFile.close()

    if boold:
        print("End")
