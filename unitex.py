"""Chaîne de traitement Unitex : normalisation, tokenisation, dictionnaire, graphe, concordance.

Usage : python unitex.py
Variables d'environnement :
    UNITEX_TOOL    chemin de UnitexToolLogger (défaut : ./UnitexToolLogger)
    UNITEX_ALPHA   fichier alphabet français d'Unitex (défaut : Alphabet.txt)
    UNITEX_NORM    règles de normalisation (défaut : Norm.txt)
"""
import os
import shutil
import subprocess

TOOL = os.environ.get("UNITEX_TOOL", os.path.join(".", "UnitexToolLogger"))
ALPHABET = os.environ.get("UNITEX_ALPHA", "Alphabet.txt")
NORM = os.environ.get("UNITEX_NORM", "Norm.txt")


def run(*args):
    print(">", TOOL, *args)
    subprocess.run([TOOL, *args], check=True)


if os.path.exists("corpus-medical_snt"):
    shutil.rmtree("corpus-medical_snt")
os.mkdir("corpus-medical_snt")

run("Normalize", "corpus-medical.txt", "-r", NORM)
run("Tokenize", "corpus-medical.snt", "-a", ALPHABET)
run("Compress", "subst.dic", "-o", "subst.bin")
run("Dico", "-t", "corpus-medical.snt", "-a", ALPHABET, "subst.bin")
run("Grf2Fst2", os.path.join("graphs", "posologie.grf"))
run("Locate", "-t", "corpus-medical.snt", os.path.join("graphs", "posologie.fst2"), "-a", ALPHABET, "-L", "-I", "--all")
run("Concord", os.path.join("corpus-medical_snt", "concord.ind"), "-f", "Courier new", "-s", "12", "-l", "40", "-r", "55")

# Le fichier alphabet décrit tous les caractères de la langue et les correspondances
# minuscules / majuscules ; Unitex en a besoin pour tokeniser le texte et appliquer
# les dictionnaires.

# Merabti Amar
# Meziani Mehdi
