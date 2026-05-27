import random



farben = ["Herz", "Karo", "Pik", "Kreuz"]
kartenwerte = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
               "Bube", "Dame", "Koenig", "Ass"]


def deck_erstellen():
    deck = []
    for farbe in farben:
        for wert in kartenwerte:
            karte = {"wert": wert, "farbe": farbe}
            deck.append(karte)
    random.shuffle(deck)
    return deck


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
    while summe > 21 and anzahl_asse > 0:
        summe = summe - 10
        anzahl_asse = anzahl_asse - 1
    return summe


def hand_anzeigen(hand, name):
    kartennamen = []
    for karte in hand:
        kartennamen.append(karte["wert"] + " " + karte["farbe"])
    text = ", ".join(kartennamen)
    print(name + ": " + text + "  (Wert: " + str(handwert(hand)) + ")")


def runde_spielen():
    deck = deck_erstellen()
 
    spieler_hand = []
    dealer_hand = []
 
    spieler_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    spieler_hand.append(deck.pop())
    dealer_hand.append(deck.pop())

    print("=== Neue Runde Blackjack ===")
    hand_anzeigen(spieler_hand, "Deine Hand")
    erste_dealer_karte = dealer_hand[0]["wert"] + " " + dealer_hand[0]["farbe"]
    print("Dealer: " + erste_dealer_karte + ", [verdeckte Karte]")
    print()

    spieler_fertig = False
    while not spieler_fertig:
        entscheidung = input("Karte ziehen (h) oder stehen bleiben (s)? ")
        if entscheidung == "h":
            spieler_hand.append(deck.pop())
            hand_anzeigen(spieler_hand, "Deine Hand")
            if handwert(spieler_hand) > 21:
                print("Du hast dich ueberkauft! Du hast diese Runde verloren.")
                spieler_fertig = True
        elif entscheidung == "s":
            print("Du bleibst stehen.")
            spieler_fertig = True
        else:
            print("Ungueltige Eingabe. Bitte 'h' oder 's' eingeben.")

    # TODO zweite Haelfte der Spielmechanik:
    # Dealer-Zug programmieren, Dealer zieht Karten bis mindestens 17
    # Gewinner ermitteln, Haende vergleichen
    # Blackjack-Sonderfall behandeln, 21 mit den ersten zwei Karten
    # Moeglichkeit fuer mehrere Runden/neues Spiel einbauen
    print()
    print("(Dealer-Zug und Auswertung sind noch nicht implementiert.)")


# Spiel starten
runde_spielen()