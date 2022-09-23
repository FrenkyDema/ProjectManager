# -*- coding: utf-8 -*-
__author__ = "Francesco"
__version__ = "0101 2022/03/14"

import json
import os
import re
from genericpath import isfile

path, tail = os.path.split(__file__)
os.chdir(path)

# CONSTANT
path_separation = "//"
file_path = '../resources/'
header_path = '../resources/Headers/'
image_path = '../resources/Icons/'


# ================== JSON functions ==================


def open_json(file_name):
    try:
        f = open(file_path + file_name, 'r+')
        return f
    except FileNotFoundError:
        with open(file_path + file_name, 'w') as f:
            json.dump({}, f, indent=4)
        return open_json(file_name)
    except:
        exit(1)


def update_key_json(file_name, key, value):
    f = open_json(file_name)
    data = json.load(f)
    data[key] = value
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()
    f.close()


def update_json(file_name, dix):
    for key, value in dix.items():
        update_key_json(file_name, key, value)


def get_key_value_json(file_name, key):
    f = open_json(file_name)
    data = json.load(f)
    f.close()
    try:
        return data[key]
    except KeyError:
        return ""


def get_dix_json(file_name: str):
    f = open_json(file_name)
    data = json.load(f)
    f.close()
    return data


# ================== create project functions ==================


def rotate(lista: list, n):
    return lista[n:] + lista[:n]


def make_project_dir():
    _path: str = get_key_value_json("project_settings.json", "path")
    project_name: str = get_key_value_json(
        "project_settings.json", "project_name")
    folder_prefix: str = get_key_value_json(
        "project_settings.json", "folder_prefix")
    bin_folder: str = get_key_value_json(
        "project_settings.json", "bin_folder")
    doc_folder: str = get_key_value_json(
        "project_settings.json", "doc_folder")
    file_folder: str = get_key_value_json(
        "project_settings.json", "file_folder")
    folder: str = _path + path_separation + folder_prefix + project_name
    exist = os.path.isdir(folder)
    per_bin = ""
    per_doc = ""

    if not exist:
        os.makedirs(folder)

        per_bin = folder + path_separation + bin_folder
        os.makedirs(per_bin)

        per_doc = folder + path_separation + doc_folder
        os.makedirs(per_doc)

        per_file = folder + path_separation + file_folder
        os.makedirs(per_file)

    return exist, per_bin, per_doc


def create_project_file(per_bin, per_doc):
    project_name = get_key_value_json(
        "project_settings.json", "project_name")
    nome_readme = get_key_value_json("project_settings.json", "nome_readme")
    language = get_key_value_json(
        "project_settings.json", "selected_language")
    selected_languages: dict = get_key_value_json(
        "config.json", "selected_languages")

    file_header = lenguage_to_header_file(language)
    if isfile(header_path + file_header):
        file = open(per_bin + path_separation +
                    project_name + "." + selected_languages[language], "w")
        try:
            file.writelines(replace_all_tags(file_header))
        except IOError as e:
            print(e)
        finally:
            file.close()
    readme_file = open(per_doc + path_separation + nome_readme, "w")
    readme_file.writelines(replace_all_tags(lenguage_to_header_file("readme")))
    readme_file.close()


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
            temp_return_str = get_key_value_json(
                "project_settings.json", key.strip("{%%}"))
            if temp_return_str == "":
                temp_return_str = get_key_value_json(
                    "config.json", key.strip("{%%}"))
            matchs[key] = temp_return_str
            new_line = new_line.replace(key, matchs[key])
        new_lines.append(new_line)
    return new_lines


def get_tags(file_name):
    tag_list: list = get_key_value_json(file_name, "tags")
    stringa: str = ""
    for tag in tag_list:
        stringa += "{%" + tag + "%}" + "\n"
    return stringa


# ================== recent projects functions ==================


def add_new_project(title, date, location):
    recent_preoject: list = get_key_value_json("recent_poject.json", "recent_poject")
    recent_preoject.append((title, date, location))
    update_key_json("recent_poject.json", "recent_poject", recent_preoject)


# ========= project_settings.json =========

def default_project_settings_values():
    update_json("project_settings.json", get_key_value_json("config.json", "default_project_config"))


# ========= config.json =========

def default_config_values():
    dix = {
        "supported_languages": {
            "java": "java",
            "python": "py"
        },
        "tags": [
            "folder_prefix",
            "readme_name",
            "bin_folder",
            "doc_folder",
            "file_folder",
            "description",
            "project_name",
            "auto_readme"
        ],
        "work_space_name": "src",
        "default_project_config": {
            "selected_language": "",
            "project_name": "",
            "description": "",
            "auto_readme": False
        }
    }

    update_json('config.json', dix)


# ========= recent_project.json =========

def default_recent_project_values():
    dix = {"recent_poject": [("", "", "")]}

    update_json('recent_project.json', dix)


# ========= image functions =========

def get_image_path(image_name):
    return os.path.abspath(image_path + image_name)


boold = True
if __name__ == "__main__":
    if boold:
        print("Start")

    default_project_settings_values()
    default_config_values()
    default_recent_project_values()

    if boold:
        print("End")
