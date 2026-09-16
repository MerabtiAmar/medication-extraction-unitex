# coding=utf-8
import re
import sys
import os
from codecs import open

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def updateNames(file_tmp, file_org):
    try:
        os.rename(file_org, 'old__' + file_org)
        os.rename(file_tmp, file_org)
        os.remove('old__' + file_org)
    except Exception as e:
        print(e)
        raise


def encoder_UCS2_LE_BOM(file_name, mode, bom_included=True):
    if mode == 'r':
        # 'utf-16' détecte et retire le BOM (sauter 2 caractères amputait le premier mot)
        return open(file_name, mode, encoding='utf-16')
    file = open(file_name, mode, encoding='utf-16-le')
    if mode == 'w' and bom_included:
        file.write(u'\ufeff')
    return file


def normalize(text):
    return text.lower().replace(u'é', 'e') + text


def trier():
    dic = encoder_UCS2_LE_BOM('subst.dic', 'r')
    fichier_tempo = encoder_UCS2_LE_BOM('fichier_tempo.dic', 'w')
    # clés sans fin de ligne : les fins \r\n (Windows) et \n ne doivent pas créer de doublons
    sort_dic = {normalize(line.strip()): line.strip() + '\n' for line in dic.readlines() if line.strip()}
    for line_key in sorted(sort_dic.keys()):
        fichier_tempo.write(sort_dic[line_key])
    dic.close()
    fichier_tempo.close()
    updateNames('fichier_tempo.dic', 'subst.dic')


def eliminer_doubles():
    dic = encoder_UCS2_LE_BOM('subst.dic', 'r')
    fichier_tempo = encoder_UCS2_LE_BOM('fichier_tempo.dic', 'w')

    result = dic.readlines()
    new_result = {line.strip().lower(): line.strip() + '\n' for line in result if line.strip()}.values()

    for line in new_result:
        fichier_tempo.write(line)
    dic.close()
    fichier_tempo.close()
    updateNames('fichier_tempo.dic', 'subst.dic')


subst = open("subst.dic", 'r', encoding="utf-16")
subst_lines = subst.readlines()
subst.close()

if len(sys.argv) < 2:
    print(" Manque de paramètres en entrée ! (il faut passer un argument) ")
    exit()
else:
    corpus_medical = open(sys.argv[1], 'r', encoding='utf-8').read()
    dic_init = encoder_UCS2_LE_BOM('subst.dic', 'a')
    dic_enri = encoder_UCS2_LE_BOM('subst_enri.dic', 'w')
    code = r'(?:([A-Za-z][\w-]{5,}))\s*(?:[0-9]+\s*(?:mg|ml|cp|g|flac|gramme|gamma|kg|mn|½|µg).+\b|[0-9]+/j\b)'
    subst_extracted = re.findall(code, corpus_medical, re.I)
    cpt = 0
    for ss in subst_extracted:
        dic_init.write(ss.lower() + ',.N+subst\n')
        dic_enri.write(ss.lower() + ',.N+subst\n')
        cpt += 1
    dic_init.close()
    dic_enri.close()

    eliminer_doubles()
    trier()

sortie = open("subst_enri.dic", 'r', encoding="utf-16")
lis = sortie.readlines()
cpt_aff = 1
for j in lis:
    print(str(cpt_aff) + "- " + j.split(',')[0])
    cpt_aff = cpt_aff + 1
sortie.close()

cpt_aff = 1
cpt = 0
infos2 = open("infos2.txt", 'w', encoding="utf-8")
sortie = open("subst_enri.dic", 'r', encoding="utf-16")
lis = sortie.readlines()
for i in list(set(lis)):
    cpt_aff = cpt_aff + 1
lettre = 'a'
while ord(lettre) <= ord('z'):
    for j in list(set(lis)):
        if j.startswith(lettre):
            cpt = cpt + 1
    infos2.write("le nombre des mediacaments avec la lettre " + str(lettre) + " est: " + str(cpt) + "\n")
    lettre = chr(ord(lettre) + 1)
infos2.write("le nombre des mediacaments total est: " + str(cpt_aff - 1) + "\n")
sortie.close()
infos2.close()

cpt_aff = 1
cpt = 0
out = open("subst_enri.dic", 'r', encoding="utf-16")
inf = out.readlines()
out.close()

chaine = []
for a in list(set(inf)):
    if a in list(set(subst_lines)):
        x = 0
    else:
        chaine.append(a)
infos3 = open("info3.txt", 'w', encoding="utf-8")
lettre = 'a'
while ord(lettre) <= ord('z'):
    for j in list(set(chaine)):
        if j.startswith(lettre):
            cpt = cpt + 1
            cpt_aff = cpt_aff + 1
    infos3.write("le nombre des mediacaments avec la lettre " + str(lettre) + " est: " + str(cpt) + "\n")
    lettre = chr(ord(lettre) + 1)
infos3.write("le nombre des mediacaments total est: " + str(cpt_aff - 1) + "\n")
infos3.close()


#Merabti Amar
#Meziani Mehdi