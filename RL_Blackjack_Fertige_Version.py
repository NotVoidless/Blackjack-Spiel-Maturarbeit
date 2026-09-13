import random
import os
import torch
import torch.nn as nn
from openpyxl import Workbook

farben = ["Herz", "Karo", "Pik", "Kreuz"]
kartenwerte = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
               "Bube", "Dame", "Koenig", "Ass"]

anzahl_decks = 6
mischgrenze = anzahl_decks * 52 // 4


def schuh_erstellen():
    schuh = []
    for i in range(anzahl_decks):
        for farbe in farben:
            for wert in kartenwerte:
                karte = {"wert": wert, "farbe": farbe}
                schuh.append(karte)
    random.shuffle(schuh)
    return schuh


def kartenpunkte(karte):
    wert = karte["wert"]
    if wert in ["Bube", "Dame", "Koenig"]:
        return 10
    elif wert == "Ass":
        return 11
    else:
        return int(wert)


def handwert(hand):
    summe = 0
    anzahl_asse = 0
    for karte in hand:
        summe = summe + kartenpunkte(karte)
        if karte["wert"] == "Ass":
            anzahl_asse = anzahl_asse + 1
    summe = summe - anzahl_asse * 10
    if anzahl_asse > 0 and summe + 10 <= 21:
        summe = summe + 10
    return summe


def ist_blackjack(hand):
    if len(hand) == 2 and handwert(hand) == 21:
        return True
    else:
        return False


def zaehlwert(karte):
    wert = karte["wert"]
    if wert in ["2", "3", "4", "5", "6"]:
        return 1
    elif wert in ["7", "8", "9"]:
        return 0
    else:
        return -1


def nutzbares_ass(hand):
    summe = 0
    anzahl_asse = 0
    for karte in hand:
        summe = summe + kartenpunkte(karte)
        if karte["wert"] == "Ass":
            anzahl_asse = anzahl_asse + 1
    summe = summe - anzahl_asse * 10
    if anzahl_asse > 0 and summe + 10 <= 21:
        return 1
    else:
        return 0


schuh = schuh_erstellen()
laufender_zaehler = 0
spieler_hand = []
dealer_hand = []


def karte_ziehen(sichtbar=True):
    global laufender_zaehler
    karte = schuh.pop()
    if sichtbar:
        laufender_zaehler = laufender_zaehler + zaehlwert(karte)
    return karte


def dealer_aufdecken():
    global laufender_zaehler
    laufender_zaehler = laufender_zaehler + zaehlwert(dealer_hand[1])


def mischen_falls_noetig():
    global schuh, laufender_zaehler
    if len(schuh) < mischgrenze:
        schuh = schuh_erstellen()
        laufender_zaehler = 0


def austeilen():
    global spieler_hand, dealer_hand
    spieler_hand = []
    dealer_hand = []
    spieler_hand.append(karte_ziehen())
    dealer_hand.append(karte_ziehen())
    spieler_hand.append(karte_ziehen())
    dealer_hand.append(karte_ziehen(sichtbar=False))


def dealer_ausspielen():
    while handwert(dealer_hand) < 17:
        dealer_hand.append(karte_ziehen())


def ergebnis_ermitteln(spieler_hand, dealer_hand):
    spieler_wert = handwert(spieler_hand)
    dealer_wert = handwert(dealer_hand)
    if spieler_wert > 21:
        return "Du hast dich ueberkauft. Der Dealer gewinnt."
    elif dealer_wert > 21:
        return "Der Dealer ueberkauft sich. Du gewinnst!"
    elif spieler_wert > dealer_wert:
        return "Du gewinnst!"
    elif spieler_wert < dealer_wert:
        return "Der Dealer gewinnt."
    else:
        return "Unentschieden (Push)."


def zustand_erstellen():
    spieler_wert = handwert(spieler_hand)
    dealer_punkte = kartenpunkte(dealer_hand[0])
    ass = nutzbares_ass(spieler_hand)
    verbleibende_decks = len(schuh) / 52
    echter_zaehler = laufender_zaehler / verbleibende_decks
    zustand = [spieler_wert / 21, dealer_punkte / 11, ass, echter_zaehler / 10]
    return zustand


def belohnung_ermitteln():
    spieler_wert = handwert(spieler_hand)
    dealer_wert = handwert(dealer_hand)
    if spieler_wert > 21:
        return -1
    elif dealer_wert > 21:
        return 1
    elif spieler_wert > dealer_wert:
        return 1
    elif spieler_wert < dealer_wert:
        return -1
    else:
        return 0


mit_kartenzaehler = True


def zustand_fuer_ki():
    zustand = zustand_erstellen()
    if not mit_kartenzaehler:
        zustand[3] = 0.0
    return zustand


def reset():
    mischen_falls_noetig()
    austeilen()
    return zustand_fuer_ki()


def step(aktion):
    if aktion == 1:
        spieler_hand.append(karte_ziehen())
        if handwert(spieler_hand) > 21:
            dealer_aufdecken()
            return zustand_fuer_ki(), belohnung_ermitteln(), True
        elif handwert(spieler_hand) == 21:
            dealer_aufdecken()
            dealer_ausspielen()
            return zustand_fuer_ki(), belohnung_ermitteln(), True
        else:
            return zustand_fuer_ki(), 0, False
    else:
        dealer_aufdecken()
        dealer_ausspielen()
        return zustand_fuer_ki(), belohnung_ermitteln(), True


anzahl_episoden = 300000
batch_groesse = 200
lernrate = 0.003
entropie_gewicht = 0.01
messintervall = 5000

netz = nn.Sequential(
    nn.Linear(4, 32),
    nn.ReLU(),
    nn.Linear(32, 2)
)

optimierer = torch.optim.Adam(netz.parameters(), lr=lernrate)


def aktion_waehlen(zustand):
    eingabe = torch.tensor(zustand, dtype=torch.float32)
    ausgabe = netz(eingabe)
    wahrscheinlichkeiten = torch.softmax(ausgabe, dim=0)
    if random.random() < wahrscheinlichkeiten[1].item():
        aktion = 1
    else:
        aktion = 0
    log_wahrscheinlichkeit = torch.log(wahrscheinlichkeiten[aktion] + 0.00000001)
    entropie = -(wahrscheinlichkeiten * torch.log(wahrscheinlichkeiten + 0.00000001)).sum()
    return aktion, log_wahrscheinlichkeit, entropie


if mit_kartenzaehler:
    zusatz = "mit_zaehler"
else:
    zusatz = "ohne_zaehler"

dateiname_netz = "blackjack_ki_" + zusatz + ".pt"
dateiname_daten = "trainingsdaten_" + zusatz + ".xlsx"
dateiname_strategie = "strategie_" + zusatz + ".xlsx"


def strategie_speichern(dateiname):
    arbeitsmappe = Workbook()
    tabelle = arbeitsmappe.active
    tabelle.title = "Strategie"
    tabelle.append(["handwert", "dealerkarte", "nutzbares_ass", "echter_zaehler",
                     "wahrscheinlichkeit_ziehen"])
    for zaehler in [-4, -2, 0, 2, 4]:
        for ass in [0, 1]:
            for dealerkarte in range(2, 12):
                for wert in range(4, 21):
                    zustand = [wert / 21, dealerkarte / 11, ass, zaehler / 10]
                    if not mit_kartenzaehler:
                        zustand[3] = 0.0
                    eingabe = torch.tensor(zustand, dtype=torch.float32)
                    wahrscheinlichkeiten = torch.softmax(netz(eingabe), dim=0)
                    ziehen = wahrscheinlichkeiten[1].item()
                    tabelle.append([wert, dealerkarte, ass, zaehler, round(ziehen, 4)])
    try:
        arbeitsmappe.save(dateiname)
    except PermissionError:
        print("Warnung: " + dateiname + " ist gerade in Excel geoeffnet und "
              "konnte nicht gespeichert werden. Bitte Datei schliessen und "
              "das Skript erneut ausfuehren.")


print("Training startet")
print("Runden: " + str(anzahl_episoden) + ", Kartenzaehler sichtbar: " + str(mit_kartenzaehler))
print()

arbeitsmappe_daten = Workbook()
tabelle_daten = arbeitsmappe_daten.active
tabelle_daten.title = "Trainingsdaten"
tabelle_daten.append(["episode", "siege", "niederlagen", "unentschieden",
                       "siegquote", "siegquote_ohne_push", "durchschnittliche_belohnung"])

gesammelte_logs = []
gesammelte_entropien = []
gesammelte_belohnungen = []

siege = 0
niederlagen = 0
unentschieden = 0
belohnungssumme = 0

for episode in range(1, anzahl_episoden + 1):
    zustand = reset()

    if ist_blackjack(spieler_hand):
        dealer_aufdecken()
        if ist_blackjack(dealer_hand):
            belohnung = 0
        else:
            belohnung = 1.5
    elif ist_blackjack(dealer_hand):
        dealer_aufdecken()
        belohnung = -1
    else:
        fertig = False
        logs_der_episode = []
        entropien_der_episode = []
        while not fertig:
            aktion, log_wahrscheinlichkeit, entropie = aktion_waehlen(zustand)
            zustand, belohnung, fertig = step(aktion)
            logs_der_episode.append(log_wahrscheinlichkeit)
            entropien_der_episode.append(entropie)

        for i in range(len(logs_der_episode)):
            gesammelte_logs.append(logs_der_episode[i])
            gesammelte_entropien.append(entropien_der_episode[i])
            gesammelte_belohnungen.append(belohnung)

    if belohnung >= 1:
        siege = siege + 1
    elif belohnung == -1:
        niederlagen = niederlagen + 1
    else:
        unentschieden = unentschieden + 1
    belohnungssumme = belohnungssumme + belohnung

    if episode % batch_groesse == 0 and len(gesammelte_logs) > 0:
        belohnungs_tensor = torch.tensor(gesammelte_belohnungen, dtype=torch.float32)
        vorteil = belohnungs_tensor - belohnungs_tensor.mean()
        log_tensor = torch.stack(gesammelte_logs)
        entropie_tensor = torch.stack(gesammelte_entropien)
        aktuelles_entropie_gewicht = entropie_gewicht * (1 - episode / anzahl_episoden)
        verlust = -(log_tensor * vorteil).mean() - aktuelles_entropie_gewicht * entropie_tensor.mean()
        optimierer.zero_grad()
        verlust.backward()
        optimierer.step()
        gesammelte_logs = []
        gesammelte_entropien = []
        gesammelte_belohnungen = []

    if episode % messintervall == 0:
        gespielt = siege + niederlagen + unentschieden
        siegquote = siege / gespielt * 100
        quote_ohne_push = siege / (siege + niederlagen) * 100
        schnitt = belohnungssumme / gespielt
        print("Runde " + str(episode) + ": Siegquote " + str(round(siegquote, 1))
              + " Prozent, ohne Push " + str(round(quote_ohne_push, 1))
              + " Prozent, durchschnittliche Belohnung " + str(round(schnitt, 3)))
        tabelle_daten.append([episode, siege, niederlagen, unentschieden,
                              round(siegquote, 2), round(quote_ohne_push, 2),
                              round(schnitt, 4)])
        try:
            arbeitsmappe_daten.save(dateiname_daten)
        except PermissionError:
            print("Warnung: " + dateiname_daten + " ist gerade in Excel geoeffnet "
                  "und konnte nicht aktualisiert werden.")
        siege = 0
        niederlagen = 0
        unentschieden = 0
        belohnungssumme = 0

try:
    arbeitsmappe_daten.save(dateiname_daten)
except PermissionError:
    print("Warnung: " + dateiname_daten + " ist gerade in Excel geoeffnet und "
          "konnte nicht final gespeichert werden. Bitte Datei schliessen und "
          "das Skript erneut ausfuehren, um die letzten Daten zu erhalten.")

torch.save(netz.state_dict(), dateiname_netz)
strategie_speichern(dateiname_strategie)

print()
print("Training fertig. Gespeichert im Ordner " + os.getcwd())
print("  " + dateiname_netz + "  (das trainierte Netz)")
print("  " + dateiname_daten + "  (Verlauf des Trainings, fuer Excel)")
print("  " + dateiname_strategie + "  (die gelernte Strategie, fuer Excel)")