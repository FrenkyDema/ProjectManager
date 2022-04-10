# -*- coding: utf-8 -*-
from doctest import master
from email import header
from genericpath import isdir, isfile
__autor__ = "Francesco"
__version__ = "0101 2022/03/14"

from ProjectManager import *


percorso, tail = os.path.split(__file__)
os.chdir(percorso)

# CONSTANTI
path_separation = "//"
file_path = './file/'
header_path = './file/Headers/'

# ================== JSON functions ==================


def open_JSON(file_name):
    try:
        f = open(file_path + file_name, 'r+')
        return f
    except FileNotFoundError:
        with open(file_path + file_name, 'w') as f:
            json.dump({}, f, indent=4)
        return open_JSON(file_name)
    except:
        exit(1)


def update_key_JSON(file_name, key, value):
    f = open_JSON(file_name)
    data = json.load(f)
    data[key] = value
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()
    f.close()


def update_JSON(file_name, dix):
    for key, value in dix.items():
        update_key_JSON(file_name, key, value)


def get_key_value_JSON(file_name, key):
    f = open_JSON(file_name)
    data = json.load(f)
    f.close()
    try:
        return data[key]
    except KeyError:
        return ""


def get_dix_JSON(file_name):
    f = open_JSON(file_name)
    data = json.load(f)
    f.close()
    return data

# ================== create project functions ==================


def rotate(lista: list, n):
    return lista[n:] + lista[:n]


def make_project_dir():
    path: str = get_key_value_JSON("project_settings.json", "percorso")
    nome_progetto: str = get_key_value_JSON(
        "project_settings.json", "nome_progetto")
    prefisso_cartella: str = get_key_value_JSON(
        "project_settings.json", "prefisso_cartella")
    cartella_bin: str = get_key_value_JSON(
        "project_settings.json", "cartella_bin")
    cartella_doc: str = get_key_value_JSON(
        "project_settings.json", "cartella_doc")
    cartella_file: str = get_key_value_JSON(
        "project_settings.json", "cartella_file")
    cartella: str = path + path_separation + prefisso_cartella + nome_progetto
    esiste = os.path.isdir(cartella)
    per_bin = ""
    per_doc = ""
    per_file = ""

    if not esiste:
        os.makedirs(cartella)

        per_bin = cartella + path_separation + cartella_bin
        os.makedirs(per_bin)

        per_doc = cartella + path_separation + cartella_doc
        os.makedirs(per_doc)

        per_file = cartella + path_separation + cartella_file
        os.makedirs(per_file)

    return esiste, per_bin, per_doc


def create_project_file(per_bin, per_doc):
    nome_progetto = get_key_value_JSON(
        "project_settings.json", "nome_progetto")
    nome_readme = get_key_value_JSON("project_settings.json", "nome_readme")
    linguaggi_selezionati = get_key_value_JSON(
        "project_settings.json", "linguaggi_selezionati")
    supported_leguages: dict = get_key_value_JSON(
        "config.json", "supported_leguages")

    for lenguage in linguaggi_selezionati:
        file_header = lenguage_to_header_file(lenguage)
        if isfile(header_path + file_header):
            file = open(per_bin + path_separation +
                            nome_progetto + "." + supported_leguages[lenguage], "w")
            try:
                file.writelines(replace_all_tags(file_header))
            except IOError as e:
                print(e)
            finally:
                file.close()
    file_redme = open(per_doc + path_separation + nome_readme, "w")
    file_redme.writelines(replace_all_tags(lenguage_to_header_file("readme")))
    file_redme.close()

# ================== edit header functions ==================


def read_header(file_name):
    try:
        return open(header_path + file_name, 'r+')
    except FileNotFoundError:
        open(header_path + file_name, 'w')
        return read_header(file_name)
    except:
        exit(1)


def write_header(file_name):
    return open(header_path + file_name, 'w')


def save_header(file_name, text):
    f = write_header(file_name)

    f.write(text)

    f.close()


def header_avable():
    return os.listdir(header_path)


def get_header_text(file_name):
    f = read_header(file_name)
    list_lines = f.readlines()
    f.close()

    string = ""
    for line in list_lines:
        string += line
    return string


def lenguage_to_header_file(lenguage: str):
    return lenguage + "_header.txt"

# ================== tags functions ==================


def replace_all_tags(file_name):
    f = read_header(file_name)
    list_lines = f.readlines()
    f.close()

    pattern = re.compile("{%.*?%}")
    matchs = {}
    new_lines = []

    for line in list_lines:
        new_line = line
        for key in pattern.findall(line):
            temp_return_str = get_key_value_JSON(
                "project_settings.json", key.strip("{%%}"))
            if temp_return_str == "":
                temp_return_str = get_key_value_JSON(
                    "config.json", key.strip("{%%}"))
            matchs[key] = temp_return_str
            new_line = new_line.replace(key, matchs[key])
        new_lines.append(new_line)
    return new_lines


def get_tags(file_name):
    tag_list: list = get_key_value_JSON(file_name, "tags")
    stringa: str = ""
    for tag in tag_list:
        stringa += "{%" + tag + "%}" + "\n"
    return stringa


# ========= project_settings.json =========

def default_project_settings_values():
    
    update_JSON("project_settings.json", get_key_value_JSON("config.json", "default_project_config"))


# ========= config.json =========

def default_config_values():
    dix = {}

    dix["supported_leguages"] = {"java": "java", "python": "py"}
    dix["tags"] = ["prefisso_cartella",
                   "nome_readme",
                   "cartella_bin",
                   "cartella_doc",
                   "cartella_file",
                   "descrizione",
                   "nome_progetto",
                   "auto_readme"]
    dix["work_space_name"] = "src"
    dix["default_project_config"] = {
        "linguaggi_selezionati": [],
        "nome_progetto": "",
        "descrizione": "",
        "auto_readme": False
    }

    update_JSON('config.json', dix)


boold = True
if __name__ == "__main__":
    if boold:
        print("Start")

    default_config_values()

    # dix = {}

    # dix["prefisso_cartella"] = "demartini_F_"
    # dix["nome_readme"] = "README.md"
    # dix["cartella_bin"] = "bin"
    # dix["cartella_doc"] = "doc"
    # dix["cartella_file"] = "file"
    # dix["linguaggi_selezionati"] = []
    # dix["nome_progetto"] = ""
    # dix["descrizione"] = ""
    # dix["auto_readme"] = False
    # dix["percorso"] = "C://Users//frenk//OneDrive//Documenti//School//INI//Test"

    # update_JSON('project_settings.json', dix)

    if boold:
        print("End")
