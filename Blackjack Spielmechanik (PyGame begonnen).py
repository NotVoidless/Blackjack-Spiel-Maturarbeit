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


deck = deck_erstellen()
spieler_hand = []
dealer_hand = []
spieler_hand.append(deck.pop())
dealer_hand.append(deck.pop())
spieler_hand.append(deck.pop())
dealer_hand.append(deck.pop())

uhr = pygame.time.Clock()
laeuft = True
while laeuft:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False

    fenster.fill(gruen)
    text_zeichnen("Blackjack", schrift_gross, weiss, 360, 20)

    text_zeichnen("Dealer", schrift_mittel, weiss, 60, 80)
    hand_zeichnen(dealer_hand, 60, 115, erste_verdeckt=True)

    text_zeichnen("Du", schrift_mittel, weiss, 60, 300)
    hand_zeichnen(spieler_hand, 60, 335)
    text_zeichnen("Wert: " + str(handwert(spieler_hand)), schrift_klein, weiss, 60, 465)

    button_zeichnen(hit_button, "Ziehen")
    button_zeichnen(stand_button, "Stehen")

    pygame.display.flip()
    uhr.tick(30)

pygame.quit()