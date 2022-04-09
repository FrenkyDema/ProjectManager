# -*- coding: utf-8 -*-
__autor__ = "Francesco"
__version__ = "0101 2021/11/23"

import os

exist = False
percorso, tail = os.path.split(__file__)
os.chdir(percorso)

boold = False
if __name__ == '__main__':

    if boold:
        print("Start")

    clipBoard = []
    counterCapolinea = 1
    if not boold:
        print("inserire clipboard: ")
        while counterCapolinea < 2:

            inputConsegna = input()
            clipBoard.append(inputConsegna.replace("        ", "\t") + "\n")

            if inputConsegna == "":
                counterCapolinea += 1
            else:
                counterCapolinea = 1
        functionStr = input(
            "inserire funzone da eseguire\n1 - clipBoardToString\t\t2 - format clipBoard\n")
    else:
        clipBoard.append(
            "'package ' + nomeCartella + projectName + '.bin;\n\n' + \\".replace("'", '"'))
        functionStr = "2"
    print("-------------------------------------------------------------------------------------------------------")

    if functionStr == "1":
        for string in clipBoard:
            print(repr(string) + " + \\")

    elif functionStr == "2":
        # TODO finire funzione 2 (formattazione stringa data in input)

        for i in range(len(clipBoard)):
            clipBoard[i].strip()

        for i in range(len(clipBoard)):
            if clipBoard[i].find("\\\\n\\\\n") > -1:
                print("find")
                clipBoard[i] = clipBoard[i].replace("\\\\n\\\\n", "\\n")
                clipBoard.insert(i + 1, "\\n + \\")

        for string in clipBoard:
            print(repr(string).replace("'", "").encode().decode('unicode_escape'))

    print("-------------------------------------------------------------------------------------------------------")

    if boold:
        print("End")
