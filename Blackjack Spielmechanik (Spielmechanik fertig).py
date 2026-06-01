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
 
 
def ist_blackjack(hand):
    if len(hand) == 2 and handwert(hand) == 21:
        return True
    else:
        return False
 
 
def dealer_zug(dealer_hand, deck):
    print("Der Dealer deckt seine verdeckte Karte auf.")
    hand_anzeigen(dealer_hand, "Dealer")
    while handwert(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        print("Der Dealer zieht eine Karte.")
        hand_anzeigen(dealer_hand, "Dealer")
 
 
def gewinner_ermitteln(spieler_hand, dealer_hand):
    spieler_wert = handwert(spieler_hand)
    dealer_wert = handwert(dealer_hand)
    if dealer_wert > 21:
        print("Der Dealer hat sich ueberkauft. Du gewinnst!")
    elif spieler_wert > dealer_wert:
        print("Du hast die hoehere Hand. Du gewinnst!")
    elif spieler_wert < dealer_wert:
        print("Der Dealer hat die hoehere Hand. Der Dealer gewinnt.")
    else:
        print("Gleichstand. Die Runde endet unentschieden (Push).")
 
 
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
 
    if ist_blackjack(spieler_hand):
        print("Blackjack! Du hast 21 mit den ersten zwei Karten.")
        print("Dein Zug ist damit vorbei, der Dealer ist an der Reihe.")
    else:
        spieler_fertig = False
        while not spieler_fertig:
            entscheidung = input("Karte ziehen (h) oder stehen bleiben (s)? ")
            if entscheidung == "h":
                spieler_hand.append(deck.pop())
                hand_anzeigen(spieler_hand, "Deine Hand")
                if handwert(spieler_hand) == 21:
                    print("Du hast 21! Dein Zug ist vorbei, der Dealer ist an der Reihe.")
                    spieler_fertig = True
                elif handwert(spieler_hand) > 21:
                    spieler_fertig = True
            elif entscheidung == "s":
                print("Du bleibst stehen.")
                spieler_fertig = True
            else:
                print("Ungueltige Eingabe. Bitte 'h' oder 's' eingeben.")
 
    if handwert(spieler_hand) > 21:
        print("Du hast dich ueberkauft! Der Dealer gewinnt diese Runde.")
        return
 
    print()
    dealer_zug(dealer_hand, deck)
    print()
    gewinner_ermitteln(spieler_hand, dealer_hand)
 
 
def spiel_starten():
    weiterspielen = True
    while weiterspielen:
        runde_spielen()
        print()
        antwort = input("Moechtest du nochmal spielen (j/n)? ")
        print()
        if antwort != "j":
            weiterspielen = False
    print("Danke fuers Spielen!")
 
 
spiel_starten()