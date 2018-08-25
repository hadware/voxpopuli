from urllib import request
from zipfile import ZipFile
from io import BytesIO
from os import makedirs
import re
import argparse


BASE_URL = "http://tcts.fpms.ac.be/synthesis/mbrola/dba/"
MBROLA_FOLDER = "/usr/share/mbrola/"

LANG_FILES = {"fr": ["fr1/fr1-990204.zip",
                     "fr2/fr2-980806.zip",
                     "fr3/fr3-990324.zip",
                     "fr4/fr4-990521.zip",
                     "fr5/fr5-991020.zip",
                     "fr6/fr6-010330.zip",
                     "fr7/fr7-010330.zip"],
              "en": ["en1/en1-980910.zip"],
              "us": ["us1/us1-980512.zip",
                     "us2/us2-980812.zip",
                     "us3/us3-990208.zip"],
              "es": ["es1/es1-980610.zip",
                     "es2/es2-989825.zip",
                     "es3/es3.zip",
                     "es4/es4.zip"],
              "de": ["de1/de1-980227.zip",
                     "de2/de2-990106.zip",
                     "de3/de3-000307.zip",
                     "de4/de4.zip",
                     "de5/de5.zip",
                     "de6/de6.zip",
                     "de7/de7.zip",
                     "de8/de8.zip"]}


def create_folder_and_extract(voice_name, zfile):
    try:
        makedirs(MBROLA_FOLDER + voice_name + "/")
    except FileExistsError:
        pass
    zfile.extract(voice_name, MBROLA_FOLDER + voice_name + "/")


def install_voices(lang="fr"):
    """Automatically downloads and extracts all the voices for one language in the /usr/share/mbrola folder"""
    for file in LANG_FILES[lang]:
        print("Downloading file %s" % file)
        zipfile = request.urlopen(BASE_URL + file).read()
        filename = re.match(r"[a-z]{2}[1-9]/[a-z]{2}[1-9]", file).group()
        print("Extracting file")
        with ZipFile(BytesIO(zipfile), "r") as zfile:
            if filename.split("/")[0] in ["fr4", "de4", "de7"]:
                create_folder_and_extract(filename.split("/")[0], zfile)
            else:
                zfile.extract(filename, MBROLA_FOLDER)


argparser = argparse.ArgumentParser()
argparser.add_argument("languages", nargs="+", choices=list(LANG_FILES.keys()), type=str, help="Languages to install")

if __name__ == "__main__":
    args = argparser.parse_args()
    for lang in args.languages:
        print("Installing voices for languages %s" % lang)
        install_voices(lang)