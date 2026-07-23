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


schuh = schuh_erstellen()
spieler_hand = []
dealer_hand = []


def karte_ziehen():
    karte = schuh.pop()
    return karte


def mischen_falls_noetig():
    global schuh
    if len(schuh) < mischgrenze:
        schuh = schuh_erstellen()


def austeilen():
    global spieler_hand, dealer_hand
    spieler_hand = []
    dealer_hand = []
    spieler_hand.append(karte_ziehen())
    dealer_hand.append(karte_ziehen())
    spieler_hand.append(karte_ziehen())
    dealer_hand.append(karte_ziehen())


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