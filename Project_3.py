"""
Project_3.py: poslední projekt do Engeto Online Python Akademie

author: Robert Pešek
email: robert.pesek@email.cz
discord: Robert P.#6988
"""

import argparse
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re


def projdi_stranku(stranka, vysledny_soubor, navstivene_stranky):
    """Procházení jedné stránky a získávání informací o obci a o počtech voličů.
    Pokud jsou všechny informace k dispozici, jsou zapsány do výstupního souboru.
    Funkce kontroluje, zda již byla stránka navštívena, aby se zabránilo znovuprocházení.
    """

    if stranka in navstivene_stranky:
        return

    # Přidá stránku do seznamu navštívených stránek.
    navstivene_stranky.add(stranka)
    r1 = requests.get(stranka)
    soup1 = BeautifulSoup(r1.content, "html.parser")

    # Najde tag 'h3', který obsahuje informaci o obci.
    obec_h3 = soup1.find("h3", string=lambda t: t and "Obec:" in t)
    obec_jmeno = None
    if obec_h3:
        obec_jmeno = obec_h3.text.replace("Obec:", "").strip()

    # Získá informace o voličích, vydáných obálkách a platných hlasech.
    sa2 = soup1.find("td", {"headers": "sa2", "class": "cislo"})
    sa3 = soup1.find("td", {"headers": "sa3", "class": "cislo"})
    sa6 = soup1.find("td", {"headers": "sa6", "class": "cislo"})
    t1_hodnoty = []
    t1_casti = soup1.find_all("td", {"headers": "t1sa2 t1sb3", "class": "cislo"})
    for t1_hodnota in t1_casti:
        t1_hodnoty.append(t1_hodnota.text)
    t2_hodnoty = []
    t2_casti = soup1.find_all("td", {"headers": "t2sa2 t2sb3", "class": "cislo"})
    for t2_hodnota in t2_casti:
        t2_hodnoty.append(t2_hodnota.text)

    #  Pokud jsou všechny informace k dispozici, uloží je do výstupního souboru.
    if sa2 and sa3 and sa6 and obec_jmeno:
        with open(vysledny_soubor, "a", encoding="utf-8") as f:
            obec = stranka.split("obec=")[1][:6]
            f.write(
                f"{obec_jmeno};{obec};{sa2.text};{sa3.text};{sa6.text};{';'.join(t1_hodnoty)};{';'.join(t2_hodnoty)}\n"
            )
        navstivene_stranky.add(stranka)


def dostan_hlavicku(stranka_pro_hlavicku, navstivene_stranky_pro_hlavicku):
    """Získání názvů sloupců z hlaviček podstránky"""

    r2 = requests.get(stranka_pro_hlavicku)
    soup2 = BeautifulSoup(r2.content, "html.parser")

    t1_hlavicka = []
    t2_hlavicka = []

    for odkaz in soup2.find_all("a", href=True):
        podstranka = urljoin(stranka_pro_hlavicku, odkaz["href"])
        if podstranka not in navstivene_stranky_pro_hlavicku:
            r2 = requests.get(podstranka)
            podstranka_soup = BeautifulSoup(r2.content, "html.parser")

            # Získá informace o voličích, vydání obálkách a platných hlasech.
            sa2 = podstranka_soup.find("td", {"headers": "sa2", "class": "cislo"})
            sa3 = podstranka_soup.find("td", {"headers": "sa3", "class": "cislo"})
            sa6 = podstranka_soup.find("td", {"headers": "sa6", "class": "cislo"})

            # Pokud jsou všechny informace k dispozici, získá hlavičky t1 a t2.
            if sa2 and sa3 and sa6:
                t1_casti_hlavicka = podstranka_soup.find_all(
                    "td", {"class": "overflow_name", "headers": "t1sa1 t1sb2"}
                )
                t2_casti_hlavicka = podstranka_soup.find_all(
                    "td", {"class": "overflow_name", "headers": "t2sa1 t2sb2"}
                )

                # Přidá t1 a t2 hlavičky do seznamů.
                for t1_casti_hlavicka in t1_casti_hlavicka:
                    t1_hlavicka.append(t1_casti_hlavicka.text.strip())
                for t2_casti_hlavicka in t2_casti_hlavicka:
                    t2_hlavicka.append(t2_casti_hlavicka.text.strip())
                break

    return t1_hlavicka, t2_hlavicka


def zpracuj_stránky(
    stranky, vysledny_soubor_2, t1_hlavicka_2, t2_hlavicka_2, navstivene_stranky_2
):
    """Slouží k procházení všech stránek, které jsou v seznamu stranky. Funkce volá funkci projdi_stranku
    pro každou stránku a přidá všechny odkazy na další stránky do seznamu stranky_ke_zpracovani.
    Funkce zapisuje do výstupního souboru a vytváří hlavičku tabulky."""

    navstivene_stranky_2 = set()
    stranky_ke_zpracovani = stranky

    # Otevření souboru pro zápis hlavičky tabulky
    with open(vysledny_soubor_2, "w", encoding="utf-8") as f:
        f.write(
            f"Obec;Číslo obce;Voliči v seznamu;Vydané obálky;Platné hlasy;{';'.join(t1_hlavicka_2)};{';'.join(t2_hlavicka_2)}\n"
        )

    # Zpracování stránek v seznamu, dokud není seznam prázdný
    first_page = True
    while stranky_ke_zpracovani:
        # Vyjmutí první stránky ze seznamu a zpracování
        stranka_2 = stranky_ke_zpracovani.pop(0)
        projdi_stranku(stranka_2, vysledny_soubor_2, navstivene_stranky_2)

        # Získání odkazů na další stránky
        r = requests.get(stranka_2)
        soup = BeautifulSoup(r.content, "html.parser")
        obec_odkazy = []
        for odkaz_2 in soup.find_all("a", href=True):
            odkaz_spravny = odkaz_2["href"]

            # Ověření, zda odkaz obsahuje správný formát
            if (
                odkaz_spravny
                and not odkaz_spravny.startswith("#")
                and not odkaz_spravny.startswith("javascript:")
                and re.search(r"obec=\d{6}", odkaz_spravny)
            ):
                final_stranka = urljoin(stranka_2, odkaz_spravny)

                # Přidání odkazu na další stránku do seznamu, pokud ještě nebyla zpracována
                if final_stranka not in navstivene_stranky_2:
                    obec_odkazy.append(final_stranka)

        if not obec_odkazy:
            break

        # Pokud první stránka, nebude zpracovávána znovu.
        if first_page:
            stranky_ke_zpracovani.extend(obec_odkazy[1:])
            first_page = False

        # Pokud není první stárnka, přidej do seznamu.
        else:
            stranky_ke_zpracovani.extend(obec_odkazy)


def remove_duplicate_last_line(file_path):
    """Pokud druhý řádek v souboru je stejný jako poslední řádek v souboru (lines[-1]),
    funkce smaže tento poslední řádek."""

    with open(file_path, "r+", encoding="utf-8") as f:
        lines = f.readlines()
        if lines[1] == lines[-1]:
            f.seek(0)
            f.writelines(lines[:-1])
            f.truncate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some URLs.")

    # Definování argumentu
    parser.add_argument(
        "url",
        metavar="Chybí jeden nebo oba dva (web.stránka/výstupní soubor) argumenty",
        type=str,
        help="webová stránka",
    )
    parser.add_argument(
        "output_file",
        metavar="Chybí jeden nebo oba dva (web.stránka/výstupní soubor) argumenty",
        type=str,
        help="výstupní soubor",
    )

    # Zpracování argumentů ze vstupu
    argumenty = parser.parse_args()
    navstivene_stranky_3 = set()

    # Získání názvů sloupců z hlaviček podstránek
    t1_hlavicka_3, t2_hlavicka_3 = dostan_hlavicku(argumenty.url, navstivene_stranky_3)

    # Zpracování URL adresy a uložení výsledků do výstupního souboru
    zpracuj_stránky(
        [argumenty.url],
        argumenty.output_file,
        t1_hlavicka_3,
        t2_hlavicka_3,
        navstivene_stranky_3,
    )
    remove_duplicate_last_line(argumenty.output_file)
