# Extraction de médicaments et de posologies avec Unitex

Projet de traitement automatique du langage (Licence 3 informatique, USTHB, 2022–2023). Dans un corpus de comptes rendus médicaux en français, on repère les **médicaments** et leur **posologie** (dose, rythme, heure, durée), avec la plateforme linguistique [Unitex/GramLab](https://unitexgramlab.org) et des scripts Python.

## Chaîne de traitement

1. **Construction du dictionnaire** — `extraire.py`
   - Récupère les pages « Sommaires des substances » du Vidal, servies en local, pour un intervalle de lettres.
   - En extrait les noms de substances par expression régulière.
   - Écrit un dictionnaire Unitex au format DELAF (`abacavir,.N+subst`), encodé en UTF-16 comme l'exige Unitex.
   - Compte les entrées par lettre (`infos1.txt`).
2. **Enrichissement** — `enrichir.py`
   - Repère dans le corpus d'autres noms de médicaments grâce à leur contexte (un mot suivi d'une dose : `mg`, `ml`, `cp`, `µg`, `/j`…).
   - Les ajoute au dictionnaire, puis dédoublonne et trie.
   - Produit des statistiques par lettre sur les entrées nouvelles (`infos2.txt`, `info3.txt`).
3. **Analyse Unitex** — `unitex.py` enchaîne `Normalize`, `Tokenize`, `Compress`, `Dico`, `Grf2Fst2`, `Locate` et `Concord`, avec le graphe [`graphs/posologie.grf`](graphs/posologie.grf).
   - Le graphe reconnaît un médicament (`<subst>`) suivi de sa dose, de son unité et de son rythme (`/jour`, `matin`, `soir`, `à 8h`…).
   - Sur le corpus du projet, il produit une concordance de **798 posologies**.
4. **Stockage** — `create_db.py` range les posologies extraites (nom, dosage, dose, rythme, heure, durée) dans une base SQLite.

## Lancer

Prérequis : Python 3 et Unitex/GramLab (outil en ligne de commande `UnitexToolLogger`, fichiers `Alphabet.txt` et `Norm.txt` de la ressource française).

```bash
# 1. Pages Vidal enregistrées dans ./vidal/, servies localement
python -m http.server 8000
python extraire.py A-Z 8000          # -> subst.dic, infos1.txt

# 2. Enrichissement à partir du corpus
python enrichir.py corpus-medical.txt

# 3. Analyse Unitex (chemins configurables : UNITEX_TOOL, UNITEX_ALPHA, UNITEX_NORM)
python unitex.py

# 4. Base des posologies
python create_db.py
```

## Données non incluses

Les pages du Vidal sont protégées par le droit d'auteur et le corpus de comptes rendus médicaux a été fourni pour le cours : ils ne sont pas redistribués.

## Modifications par rapport à la version rendue

- `extraire.py` : chaque entrée du dictionnaire est écrite avec son suffixe `,.N+subst`. Auparavant, la dernière entrée de chaque lettre perdait son suffixe et se collait à la première entrée de la lettre suivante.
- `enrichir.py` : lecture des dictionnaires UTF-16 corrigée. Sauter « 2 caractères » de BOM amputait le premier mot (`kardegic` devenait `rdegic`), et les fins de ligne Windows créaient des doublons.
- `unitex.py` : chemins configurables, `Tokenize` appliqué au texte normalisé `.snt` comme l'attend Unitex, et suppression du dossier de travail portable (au lieu de `rd /s` sous Windows, qui demandait une confirmation).
- `sqlite3.py`, dont le nom masquait le module standard `sqlite3`, est renommé `create_db.py`. Ses fautes (`curor`, `FORGEIGN KEY`, types) sont corrigées.

La chaîne complète a été revérifiée avant publication, avec Unitex/GramLab et un mini-corpus synthétique de quatre lignes : enrichissement du dictionnaire, puis concordance des quatre posologies attendues (`kardegic 75 mg 1/jour pendant 8 jours`, `Lasilix 40 mg 2 cp/j`…). `extraire.py` a été testé sur des pages Vidal servies en local : 279 substances pour les lettres A et B.

## Licence

Code distribué sous [licence MIT](LICENSE).

## Auteurs

**Amar Merabti** et **Mehdi Meziani** — Licence 3 informatique, USTHB.
