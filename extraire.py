import re
import sys
import urllib.request
from string import ascii_uppercase


def intervalFinder(start: str, end: str):
    letters = []
    for char in ascii_uppercase:
        if start <= char <= end:
            letters.append(char)

    return letters


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: Manque d'arguments...\nUsage: python extraire.py [A-Z] [port]\n")
    else:
        interval = sys.argv[1].upper()
        port = sys.argv[2]

        if not re.match(r'[A-Z]-[A-Z]', interval) or interval[0] > interval[2]:
            print("Error: L'interval donne est invalide...")
        else:

            infos1 = open('infos1.txt', 'w+', encoding='utf-8')
            dct = open('subst.dic', 'w+', encoding='utf-16')

            nbtotal = 0
            for c in intervalFinder(interval[0], interval[-1]):
                url = urllib.request.urlopen(
                    "http://localhost:%s/vidal/vidal-Sommaires-Substances-%c.htm" % (port, c))
                res = url.read().decode('utf-8')
                fin = re.findall(r'href="Substance/.*-.*.htm">(\w*)', res)
                for name in fin:
                    dct.write(name + ",.N+subst\n")
                infos1.write("\t- Nombre d'entrees in %c: %d\n" % (c, len(fin)))
                nbtotal += len(fin)
                print("http://localhost:%s/vidal/vidal-Sommaires-Substances-%c.htm" % (port, c), "done")
            infos1.write("\n- Nombre total d'entrees: %d" % nbtotal)
            infos1.close()
            dct.close()

#Merabti Amar
#Meziani Mehdi