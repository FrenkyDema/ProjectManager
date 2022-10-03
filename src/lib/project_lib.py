# -*- coding: utf-8 -*-
__author__ = "Francesco"
__version__ = "0101 2022/03/14"

import json
import logging
import os
import re
import sys
from genericpath import isfile

# CONSTANTS
path_separation = "\\"
file_path = 'src\\resources\\'
header_path = 'src\\resources\\Headers\\'
image_path = 'resources\\Icons\\'

CONFIG_FILE = "config.json"
PROJECT_SETTINGS_FILE = "project_settings.json"
RECENT_PROJECT_FILE = "recent_project.json"


# ================== File functions ==================
def resource_path(relative_path: str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.getcwd()))
    print(os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)


# ================== JSON functions ==================


def open_json(file_name: str):
    try:
        f = open(resource_path(file_path + file_name), 'r+')
        return f
    except FileNotFoundError:
        with open(resource_path(file_path + file_name), 'w') as f:
            json.dump({}, f, indent=4)
        return open_json(file_name)
    except Exception as e:
        # TODO collect error
        logging.debug(e)


def update_key_json(file_name: str, key: str, value):
    f = open_json(file_name)
    data = json.load(f)
    data[key] = value
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()
    f.close()


def update_json(file_name: str, dix: dict):
    for key, value in dix.items():
        update_key_json(file_name, key, value)


def get_key_value_json(file_name: str, key: str):
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


def rotate(lista: list, n: int):
    return lista[n:] + lista[:n]


def make_project_dir():
    _path: str = get_key_value_json(PROJECT_SETTINGS_FILE, "path")
    project_name: str = get_key_value_json(PROJECT_SETTINGS_FILE, "project_name")
    folder_prefix: str = get_key_value_json(PROJECT_SETTINGS_FILE, "folder_prefix")
    bin_folder: str = get_key_value_json(PROJECT_SETTINGS_FILE, "bin_folder")
    doc_folder: str = get_key_value_json(PROJECT_SETTINGS_FILE, "doc_folder")
    file_folder: str = get_key_value_json(PROJECT_SETTINGS_FILE, "file_folder")
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


def create_project_file(bin_path: str, doc_path: str):
    project_name = get_key_value_json(PROJECT_SETTINGS_FILE, "project_name")
    readme_name = get_key_value_json(PROJECT_SETTINGS_FILE, "readme_name")
    language = get_key_value_json(PROJECT_SETTINGS_FILE, "selected_language")
    supported_languages: dict = get_key_value_json(CONFIG_FILE, "supported_languages")
    file_header = language_to_header_file(language)
    if isfile(header_path + file_header):
        file = open(resource_path(bin_path + path_separation + project_name + "." + supported_languages[language]), "w")
        try:
            file.writelines(replace_all_tags(file_header))
        except IOError as io_error:
            print(io_error)
        finally:
            file.close()
    readme_file = open(resource_path(doc_path + path_separation + readme_name), "w")
    readme_file.writelines(replace_all_tags(language_to_header_file("readme")))
    readme_file.close()


# ================== edit header functions ==================


def read_header(file_name: str):
    try:
        return open(resource_path(header_path + file_name), 'r+')
    except FileNotFoundError:
        open(resource_path(header_path + file_name), 'w')
        return read_header(file_name)
    except Exception as e:
        # TODO collect error
        logging.debug(e)


def write_header(file_name: str):
    return open(resource_path(header_path + file_name), 'w')


def save_header(file_name: str, text: str):
    f = write_header(file_name)

    f.write(text)

    f.close()


def header_available():
    return os.listdir(resource_path(header_path))


def get_header_text(file_name: str):
    f = read_header(file_name)
    list_lines = f.readlines()
    f.close()

    string = ""
    for line in list_lines:
        string += line
    return string


def language_to_header_file(language: str):
    return language + "_header.txt"


# ================== tags functions ==================


def replace_all_tags(file_name: str):
    f = read_header(file_name)
    list_lines = f.readlines()
    f.close()

    pattern = re.compile("{%.*?%}")
    matches = {}
    new_lines = []

    for line in list_lines:
        new_line = line
        for key in pattern.findall(line):
            temp_return_str = get_key_value_json(PROJECT_SETTINGS_FILE, key.strip("{%%}"))
            if temp_return_str == "":
                temp_return_str = get_key_value_json(CONFIG_FILE, key.strip("{%%}"))
            matches[key] = temp_return_str
            new_line = new_line.replace(key, matches[key])
        new_lines.append(new_line)
    return new_lines


def get_tags(file_name: str):
    tag_list: list = get_key_value_json(file_name, "tags")
    string: str = ""
    for tag in tag_list:
        string += "{%" + tag + "%}" + "\n"
    return string


# ================== recent projects functions ==================


def add_new_project(title: str, date: str, location: str):
    recent_project: list = get_key_value_json(RECENT_PROJECT_FILE, "recent_project")
    recent_project.append((title, date, location))
    update_key_json(RECENT_PROJECT_FILE, "recent_project", recent_project)


# ========= project_settings.json =========

def default_project_settings_values():
    update_json(PROJECT_SETTINGS_FILE, get_key_value_json(CONFIG_FILE, "default_project_config"))


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

    update_json(CONFIG_FILE, dix)


# ========= recent_project.json =========

def default_recent_project_values():
    dix = {
        "recent_project": [
            {"project_name": "",
             "location": "",
             "time": ""}
        ]
    }

    update_json(RECENT_PROJECT_FILE, dix)


# ========= image functions =========

def get_image_path(image_name: str):
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
