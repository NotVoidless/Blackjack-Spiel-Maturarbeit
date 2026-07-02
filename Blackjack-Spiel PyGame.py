import random
import pygame


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
    summe = summe - anzahl_asse * 10
    if anzahl_asse > 0 and summe + 10 <= 21:
        summe = summe + 10
    return summe


def ist_blackjack(hand):
    if len(hand) == 2 and handwert(hand) == 21:
        return True
    else:
        return False


def dealer_ausspielen(dealer_hand, deck):
    while handwert(dealer_hand) < 17:
        dealer_hand.append(deck.pop())


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


pygame.init()

fenster_breite = 900
fenster_hoehe = 650
fenster = pygame.display.set_mode((fenster_breite, fenster_hoehe))
pygame.display.set_caption("Blackjack")

gruen = (0, 110, 0)
weiss = (255, 255, 255)
schwarz = (0, 0, 0)
rot = (200, 0, 0)
grau = (200, 200, 200)
dunkelgrau = (80, 80, 80)

schrift_klein = pygame.font.Font(None, 28)
schrift_mittel = pygame.font.Font(None, 36)
schrift_gross = pygame.font.Font(None, 52)

hit_button = pygame.Rect(200, 555, 180, 60)
stand_button = pygame.Rect(520, 555, 180, 60)
neue_runde_button = pygame.Rect(340, 555, 220, 60)


def text_zeichnen(text, schrift, farbe, x, y):
    bild = schrift.render(text, True, farbe)
    fenster.blit(bild, (x, y))


def karte_zeichnen(karte, x, y, verdeckt=False):
    kartenflaeche = pygame.Rect(x, y, 80, 120)
    if verdeckt:
        pygame.draw.rect(fenster, dunkelgrau, kartenflaeche, border_radius=8)
        pygame.draw.rect(fenster, weiss, kartenflaeche, width=3, border_radius=8)
        return
    pygame.draw.rect(fenster, weiss, kartenflaeche, border_radius=8)
    pygame.draw.rect(fenster, schwarz, kartenflaeche, width=2, border_radius=8)
    if karte["farbe"] in ["Herz", "Karo"]:
        textfarbe = rot
    else:
        textfarbe = schwarz
    text_zeichnen(karte["wert"], schrift_klein, textfarbe, x + 8, y + 8)
    text_zeichnen(karte["farbe"], schrift_klein, textfarbe, x + 8, y + 88)


def hand_zeichnen(hand, x, y, erste_verdeckt=False):
    for i in range(len(hand)):
        if erste_verdeckt and i == 1:
            karte_zeichnen(hand[i], x + i * 100, y, verdeckt=True)
        else:
            karte_zeichnen(hand[i], x + i * 100, y)


def button_zeichnen(rechteck, beschriftung):
    pygame.draw.rect(fenster, grau, rechteck, border_radius=8)
    pygame.draw.rect(fenster, schwarz, rechteck, width=2, border_radius=8)
    text_zeichnen(beschriftung, schrift_mittel, schwarz, rechteck.x + 20, rechteck.y + 18)


def neue_runde():
    global deck, spieler_hand, dealer_hand, zustand, ergebnis_text
    deck = deck_erstellen()
    spieler_hand = []
    dealer_hand = []
    spieler_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    spieler_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    ergebnis_text = ""
    if ist_blackjack(spieler_hand):
        dealer_ausspielen(dealer_hand, deck)
        ergebnis_text = ergebnis_ermitteln(spieler_hand, dealer_hand)
        zustand = "ende"
    else:
        zustand = "spieler"


def spieler_zieht():
    global zustand, ergebnis_text
    spieler_hand.append(deck.pop())
    if handwert(spieler_hand) > 21:
        ergebnis_text = ergebnis_ermitteln(spieler_hand, dealer_hand)
        zustand = "ende"
    elif handwert(spieler_hand) == 21:
        dealer_ausspielen(dealer_hand, deck)
        ergebnis_text = ergebnis_ermitteln(spieler_hand, dealer_hand)
        zustand = "ende"


def spieler_bleibt_stehen():
    global zustand, ergebnis_text
    dealer_ausspielen(dealer_hand, deck)
    ergebnis_text = ergebnis_ermitteln(spieler_hand, dealer_hand)
    zustand = "ende"


neue_runde()

uhr = pygame.time.Clock()
laeuft = True
while laeuft:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False
        elif ereignis.type == pygame.MOUSEBUTTONDOWN:
            if zustand == "spieler":
                if hit_button.collidepoint(ereignis.pos):
                    spieler_zieht()
                elif stand_button.collidepoint(ereignis.pos):
                    spieler_bleibt_stehen()
            elif zustand == "ende":
                if neue_runde_button.collidepoint(ereignis.pos):
                    neue_runde()

    fenster.fill(gruen)
    text_zeichnen("Blackjack", schrift_gross, weiss, 360, 20)

    text_zeichnen("Dealer", schrift_mittel, weiss, 60, 80)
    if zustand == "spieler":
        hand_zeichnen(dealer_hand, 60, 115, erste_verdeckt=True)
    else:
        hand_zeichnen(dealer_hand, 60, 115)
        text_zeichnen("Wert: " + str(handwert(dealer_hand)), schrift_klein, weiss, 60, 245)

    text_zeichnen("Du", schrift_mittel, weiss, 60, 300)
    hand_zeichnen(spieler_hand, 60, 335)
    text_zeichnen("Wert: " + str(handwert(spieler_hand)), schrift_klein, weiss, 60, 465)

    if zustand == "spieler":
        button_zeichnen(hit_button, "Ziehen")
        button_zeichnen(stand_button, "Stehen")
    else:
        text_zeichnen(ergebnis_text, schrift_klein, weiss, 60, 505)
        button_zeichnen(neue_runde_button, "Neue Runde")

    pygame.display.flip()
    uhr.tick(30)

pygame.quit()
