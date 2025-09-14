import csv
import os
import json

adatok = []
elosztott_leltar = {}
file_nev = "leltar.csv"
elosztott_file = "elosztott_leltar.csv"

def betoltes_filebol():
    """Adatok betöltése CSV fájlból."""
    global adatok
    if os.path.exists(file_nev):
        with open(file_nev, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            adatok = list(reader)
        print(f"Adatok sikeresen betöltve a(z) '{file_nev}' fájlból.\n")
    else:
        print("A leltár fájl nem található. Új leltár létrehozása.\n")

# Elosztott leltár betöltése
    if os.path.exists(elosztott_file):
        with open(elosztott_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            # A CSV fájlban a kulcsok is adatsorok, ezért külön kell kezelni
            current_szemely = None
            for row in reader:
                if row and row[0].startswith('SZEMELY:'):
                    current_szemely = row[0].replace('SZEMELY:', '')
                    elosztott_leltar[current_szemely] = []
                elif current_szemely:
                    elosztott_leltar[current_szemely].append(row)
        print(f"Elosztott adatok sikeresen betöltve a(z) '{elosztott_file}' fájlból.\n")
    else:
        print("Az elosztott leltár fájl nem található. Új elosztott leltár létrehozása.\n")

def mentes_fileba():
    """Adatok mentése CSV fájlba."""
    with open(file_nev, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(adatok)
    print(f"Adatok sikeresen elmentve a(z) '{file_nev}' fájlba.\n")

    # Elosztott leltár mentése
    with open(elosztott_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for szemely, ruhak in elosztott_leltar.items():
            writer.writerow([f"SZEMELY:{szemely}"])
            writer.writerows(ruhak)
    print(f"Adatok sikeresen elmentve a(z) '{elosztott_file}' fájlba.\n")

def hozzaad():
    while True:
        while True:
            nem = input("\033[95mNői vagy férfi? (N/F) \033[0m")
            if nem.lower() == "f":
                nem = "férfi"
                break
            if nem.lower() == "n":
                nem = "női"
                break
            else:
                print("\033[95mRossz bemenet! \033[0m")
        nev = input(str("\033[95mRuha megnevezése: \033[0m"))
        szin = input(str("\033[95mRuha színe: \033[0m"))
        meret = input(str("\033[95mRuha mérete: \033[0m"))
        egyeb = input(str("\033[95mEgyéb info: \033[0m"))
        adatok.append([nem, nev, szin, meret, egyeb])
        mentes_fileba()
        print("Ruha hozzáadva!")
        folytat = input("Folytatja? (I/N) ")
        if folytat.lower() == "n":
            break


def megtekint():
    print("\033[95m----- Ruha leltár -----\033[0m")
    for i, ruha in enumerate(adatok, start=1):
        print(f"{i}. {ruha[0]}, {ruha[1]}, {ruha[2]}, {ruha[3]}, {ruha[4]}")

def torol():
    """Ruhadarab törlése a leltárból sorszám alapján."""
    megtekint()
    if not adatok:
        return

    try:
        sorszam = int(input("\033[95mAdd meg a törlendő ruha sorszámát: \033[0m"))
        if 1 <= sorszam <= len(adatok):
            torolt_elem = adatok.pop(sorszam - 1)
            print(f"\033[95mA következő ruhadarab törölve lett: \033[0m{torolt_elem[0]}\n")
            mentes_fileba()
        else:
            print("Érvénytelen sorszám.\n")
    except ValueError:
        print("Kérlek, számot adj meg.\n")


def keres():
    """Keresés a leltárban megnevezés, szín vagy méret alapján."""
    if not adatok:
        print("A leltár üres, nincs miben keresni.\n")
        return

    kereses_tipus = input("\033[95mMi alapján keresel? (nem/megnevezes/szin/meret/egyeb): \033[0m").lower()

    if kereses_tipus not in ['nem', 'megnevezes', 'szin', 'meret', 'egyeb']:
        print("Érvénytelen keresési szempont. Kérlek, válassz a megnevezes, szin, meret közül.\n")
        return

    kereso_szo = input("\033[95mAdd meg a keresett szót: \033[0m").lower()

    talalatok = []

    for ruha in adatok:
        if kereses_tipus == 'nem' and kereso_szo in ruha[0].lower():
            talalatok.append(ruha)
        elif kereses_tipus == 'megnevezes' and kereso_szo in ruha[1].lower():
            talalatok.append(ruha)
        elif kereses_tipus == 'szin' and kereso_szo in ruha[2].lower():
            talalatok.append(ruha)
        elif kereses_tipus == 'meret' and kereso_szo in ruha[3].lower():
            talalatok.append(ruha)
        elif kereses_tipus == 'egyeb' and kereso_szo in ruha[4].lower():
            talalatok.append(ruha)

    if talalatok:
        print("\033[95m--- Keresési találatok ---\033[0m")
        for i, ruha in enumerate(talalatok, start=1):
            print(f"{i}. {ruha[0]}, {ruha[1]}, {ruha[2]}, {ruha[3]}, {ruha[4]}")
        print("\033[95m--------------------------\n")
    else:
        print("Nincsenek találatok a keresésedre.\n")


def modosit():
    """Ruhadarab adatainak módosítása sorszám alapján."""
    megtekint()
    if not adatok:
        return

    try:
        sorszam = int(input("\033[95mAdd meg a módosítandó ruha sorszámát: \033[0m"))
        if 1 <= sorszam <= len(adatok):
            ruha_index = sorszam - 1
            print(f"\033[95mA módosítandó ruha: \033[0m{adatok[ruha_index][0]}, {adatok[ruha_index][1]}, {adatok[ruha_index][2]}, {adatok[ruha_index][3]}, {adatok[ruha_index][4]}")

            valasztas = input("\033[95mMelyik adatot szeretnéd módosítani? (nem/megnevezes/szin/meret/egyeb): \033[m").lower()

            if valasztas == "nem":
                uj_nev = input("Add meg az új nemet: ")
                adatok[ruha_index][0] = uj_nev
            elif valasztas == "megnevezes":
                uj_szin = input("Add meg az új megnevezést: ")
                adatok[ruha_index][1] = uj_szin
            elif valasztas == "szin":
                uj_meret = input("Add meg az új színt: ")
                adatok[ruha_index][2] = uj_meret
            elif valasztas == "meret":
                uj_meret = input("Add meg az új méretet: ")
                adatok[ruha_index][3] = uj_meret
            elif valasztas == "egyeb":
                uj_meret = input("Add meg az új információkat: ")
                adatok[ruha_index][4] = uj_meret

            else:
                print("Érvénytelen választás.\n")
                return
            mentes_fileba()
            print("Az adat sikeresen módosítva.\n")
        else:
            print("Érvénytelen sorszám.\n")
    except ValueError:
        print("Kérlek, számot adj meg sorszámként.\n")


def kiad():
    """Ruhadarab kiadása egy személynek."""
    megtekint()
    if not adatok:
        return

    try:
        sorszam = int(input("\033[95mAdd meg a kiadandó ruha sorszámát: \033[0m"))
        if 1 <= sorszam <= len(adatok):
            szemely_nev = input("\033[95mAdd meg a személy nevét, aki elviszi a ruhát: \033[0m").lower()
            kiadott_ruha = adatok.pop(sorszam - 1)

            if szemely_nev not in elosztott_leltar:
                elosztott_leltar[szemely_nev] = []

            elosztott_leltar[szemely_nev].append(kiadott_ruha)
            mentes_fileba()
            print(f"A(z) '{kiadott_ruha[0]}' sikeresen kiadva {szemely_nev} számára.\n")
        else:
            print("Érvénytelen sorszám.\n")
    except ValueError:
        print("Kérlek, számot adj meg sorszámként.\n")


def elosztott_leltar_megtekint():
    """Az embereknél lévő leltár kiírása."""
    if not elosztott_leltar:
        print("Az elosztott leltár jelenleg üres.\n")
        return

    print("\033[95m--- Elosztott leltár ---\033[0m")
    for szemely, ruhak in elosztott_leltar.items():
        print(f"➡️ **{szemely}**:")
        for i, ruha in enumerate(ruhak, start=1):
            print(f"   - {i}. {ruha[0]}, {ruha[1]}, {ruha[2]}, {ruha[3]}, {ruha[4]}"
                  f"")
    print("\033[95m--------------------------\n\033[0m")


def visszavesz():
    """Ruhadarab visszavétele egy személytől és visszahelyezése a raktárba."""
    elosztott_leltar_megtekint()
    if not elosztott_leltar:
        return

    try:
        szemely_nev = input("\033[95mAdd meg annak a személynek a nevét, akitől visszaveszed a ruhát: \033[0m").lower()
        if szemely_nev in elosztott_leltar:
            ruhak_a_szemelynel = elosztott_leltar[szemely_nev]

            print(f"\n\033[95m--- {szemely_nev} ruhái ---\033[0m")
            for i, ruha in enumerate(ruhak_a_szemelynel, start=1):
                print(f"{i}. {ruha[0]}, {ruha[1]}, {ruha[2]}, {ruha[3]}, {ruha[4]}")

            sorszam = int(input("\033[95mAdd meg a visszaadandó ruha sorszámát: \033[0m"))
            if 1 <= sorszam <= len(ruhak_a_szemelynel):
                visszavett_ruha = ruhak_a_szemelynel.pop(sorszam - 1)
                adatok.append(visszavett_ruha)
                print(
                    f"A(z) '{visszavett_ruha[0]}' sikeresen visszavéve {szemely_nev}-től, és visszakerült a raktárba.\n")

                if not elosztott_leltar[szemely_nev]:
                    del elosztott_leltar[szemely_nev]
                    print(f"A személynek már nincs több ruhája, a neve törölve lett a nyilvántartásból.\n")
            else:
                print("Érvénytelen sorszám.\n")
        else:
            print("A személy nem található a nyilvántartásban.\n")
    except ValueError:
        print("Kérlek, számot adj meg sorszámként.\n")


def elosztott_leltar_kereses():
    """Keresés az elosztott leltárban megnevezés, szín vagy méret alapján."""
    if not elosztott_leltar:
        print("Az elosztott leltár üres, nincs miben keresni.\n")
        return

    kereses_tipus = input("\033[95mMi alapján keresel? (nem/megnevezes/szin/meret/egyeb): \033[0m").lower()
    if kereses_tipus not in ['nem', 'megnevezes', 'szin', 'meret', 'egyeb']:
        print("Érvénytelen keresési szempont. Kérlek, válassz a nem, megnevezes, szin, meret, egyeb közül.\n")
        return

    kereso_szo = input("\033[95mAdd meg a keresett szót: \033[0m").lower()

    talalatok = {}

    for szemely, ruhak in elosztott_leltar.items():
        for ruha in ruhak:
            if kereses_tipus == 'nem' and kereso_szo in ruha[0].lower():
                if szemely not in talalatok:
                    talalatok[szemely] = []
                talalatok[szemely].append(ruha)
            elif kereses_tipus == 'megnevezes' and kereso_szo in ruha[1].lower():
                if szemely not in talalatok:
                    talalatok[szemely] = []
                talalatok[szemely].append(ruha)
            elif kereses_tipus == 'szin' and kereso_szo in ruha[2].lower():
                if szemely not in talalatok:
                    talalatok[szemely] = []
                talalatok[szemely].append(ruha)
            elif kereses_tipus == 'meret' and kereso_szo in ruha[3].lower():
                if szemely not in talalatok:
                    talalatok[szemely] = []
                talalatok[szemely].append(ruha)
            elif kereses_tipus == 'egyeb' and kereso_szo in ruha[4].lower():
                if szemely not in talalatok:
                    talalatok[szemely] = []
                talalatok[szemely].append(ruha)

    if talalatok:
        print("\n\033[95m--- Elosztott leltár keresési találatok ---\033[0m")
        for szemely, ruhak in talalatok.items():
            print(f"➡️ **{szemely}**:")
            for ruha in ruhak:
                print(f"    - {ruha[0]}, {ruha[1]}, {ruha[2]}, {ruha[3]}, {ruha[4]}")
        print("\033[95m------------------------------------------\n")
    else:
        print("Nincsenek találatok a keresésedre.\n")

def menu():
    betoltes_filebol()
    while True:
        print("\033[92m----- MENÜ -----")
        print("\033[96m0: Kilépés\n1: Hozzáadás\n2: Listázás\n3: Törlés\n4: Keresés\n5: Módosítás\n"
              "\033[92m----- KIADOTT RUHÁK MENÜ -----\n\033[96m6: Kiadás\n7: Listázás\n8: Visszavétel\n9: Keresés\033[0m")
        command = input("Mit szeretnél? ")
        if command == "1":
            hozzaad()
        if command == "2":
            megtekint()
        if command == "3":
            torol()
        if command == "4":
            keres()
        if command == "5":
            modosit()
        if command == "6":
            kiad()
        if command == "7":
            elosztott_leltar_megtekint()
        if command == "8":
            visszavesz()
        if command == "9":
            elosztott_leltar_kereses()
        if command == "0":
            mentes_fileba()
            break

if __name__ == '__main__':
    menu()