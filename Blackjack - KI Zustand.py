import random


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


# Testlauf -> später löschen
def zustand_runden(zustand):
    gerundet = []
    for zahl in zustand:
        gerundet.append(round(zahl, 2))
    return gerundet
 
 
print("Test des Kartenzaehlers und des Zustands")
print("Der Schuh hat " + str(len(schuh)) + " Karten, gemischt wird unter " + str(mischgrenze))
print("Zustand: [Handwert, Dealer-Karte, Ass, Zaehler]")
print()
 
for runde in range(1, 13):
    mischen_falls_noetig()
    austeilen()
    print("Runde " + str(runde) + ": Zustand am Anfang " + str(zustand_runden(zustand_erstellen())))
    while handwert(spieler_hand) < 21 and random.randint(0, 1) == 1:
        spieler_hand.append(karte_ziehen())
    dealer_aufdecken()
    if handwert(spieler_hand) <= 21:
        dealer_ausspielen()
    print("   " + ergebnis_ermitteln(spieler_hand, dealer_hand))
    print("   noch " + str(len(schuh)) + " Karten im Schuh, laufender Zaehler " + str(laufender_zaehler))