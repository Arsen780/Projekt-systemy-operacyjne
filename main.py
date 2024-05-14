import pygame
import random
import threading
import time

pygame.init()

szerokosc, wysokosc = 800, 600
miejsca_w_doku = 3
holowniki = 7
oczekujace_statki = {'male': 0, 'srednie': 0, 'duze': 0}

bialy = (255, 255, 255)
niebieski = (70, 121, 203)
czarny = (0, 0, 0)
brazowy = (136, 59, 26)
zielony = (84, 226, 36)
zolty = (240, 255, 0)
czerwony = (255, 0, 0)

ekran = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption("Symulacja Portu")

class MalyStatek:
    def __init__(self, rozmiar=1):
        self.rozmiar = rozmiar
        self.potrzebne_holowniki = self.rozmiar
        self.miejsce = None

class SredniStatek:
    def __init__(self, rozmiar=2):
        self.rozmiar = rozmiar
        self.potrzebne_holowniki = self.rozmiar
        self.miejsce = None

class DuzyStatek:
    def __init__(self, rozmiar=3):
        self.rozmiar = rozmiar
        self.potrzebne_holowniki = self.rozmiar
        self.miejsce = None

class Holownik:
    def __init__(self, ilosc=holowniki):
        self.ilosc = ilosc

class Dok:
    def __init__(self):
        self.miejsca = [None] * miejsca_w_doku
        self.dostepne_holowniki = holowniki
        self.blokada = threading.Lock()

    def znajdz_wolne_miejsce(self):
        for i, statek in enumerate(self.miejsca):
            if statek is None:
                return i
        return None

def wjazd_do_portu(dok):
    while True:
        time.sleep(random.randint(1, 2))
        rozmiar_statku = random.choice([1, 2, 3])
        with dok.blokada:
            wolne_miejsce = dok.znajdz_wolne_miejsce()
            if wolne_miejsce is not None and dok.dostepne_holowniki >= rozmiar_statku:
                if rozmiar_statku == 1:
                    statek = MalyStatek()
                elif rozmiar_statku == 2:
                    statek = SredniStatek()
                elif rozmiar_statku == 3:
                    statek = DuzyStatek()
                dok.miejsca[wolne_miejsce] = statek
                dok.dostepne_holowniki -= rozmiar_statku
                threading.Thread(target=obsluga_statku, args=(statek, dok, wolne_miejsce)).start()
            else:
                if rozmiar_statku == 1:
                    oczekujace_statki['male'] += 1
                elif rozmiar_statku == 2:
                    oczekujace_statki['srednie'] += 1
                elif rozmiar_statku == 3:
                    oczekujace_statki['duze'] += 1

def obsluga_statku(statek, dok, miejsce):
    czas_w_doku = random.randint(3, 5)
    time.sleep(czas_w_doku)
    with dok.blokada:
        dok.miejsca[miejsce] = None
        dok.dostepne_holowniki += statek.potrzebne_holowniki
        if statek.rozmiar == 1 and oczekujace_statki['male']>0:
            oczekujace_statki['male'] -= 1
        elif statek.rozmiar == 2 and oczekujace_statki['srednie']>0:
            oczekujace_statki['srednie'] -= 1
        elif statek.rozmiar == 3 and oczekujace_statki['duze']>0:
            oczekujace_statki['duze'] -= 1

def rysuj_statek(x, y, rozmiar_statku):
    if rozmiar_statku == 1:
        kolor_statku = zielony
    elif rozmiar_statku == 2:
        kolor_statku = zolty
    elif rozmiar_statku == 3:
        kolor_statku = czerwony

    pygame.draw.rect(ekran, kolor_statku, [x, y, 50, 80])

def rysuj_dok(dok):
    for i, statek in enumerate(dok.miejsca):
        if statek is not None:
            rysuj_statek(130 + i * 170, 260, statek.rozmiar)

def rysuj_prostokat(x, y, szerokosc, wysokosc, kolor):
    pygame.draw.rect(ekran, kolor, [x, y, szerokosc, wysokosc])

def rysuj_tekst(tekst, czcionka, rozmiar, kolor, x, y, pogrubienie=False):
    czcionka_obiekt = pygame.font.SysFont(czcionka, rozmiar, pogrubienie)
    powierzchnia_tekstu = czcionka_obiekt.render(tekst, True, kolor)
    ekran.blit(powierzchnia_tekstu, (x, y))


port = Dok()

threading.Thread(target=wjazd_do_portu, args=(port,)).start()

rozmiar_czcionki1 = 14
rozmiar_czcionki2 = 18
kolor_czcionki = czarny
czcionka = "Arial"

dzialanie = True
while dzialanie:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            dzialanie = False

    ekran.fill(niebieski)
    rysuj_prostokat(60, 350, 580, 95, brazowy)
    rysuj_prostokat(szerokosc - 180, 0, 180, wysokosc, czarny)
    rysuj_tekst(f"Dostępne holowniki: {port.dostepne_holowniki}", czcionka, rozmiar_czcionki2, bialy, szerokosc - 175, 50,pogrubienie=True)
    rysuj_tekst("Oczekujące statki", czcionka, rozmiar_czcionki2, bialy, szerokosc - 175, 85, pogrubienie=True)
    rysuj_tekst(f"Duże: {oczekujace_statki['duze']}", czcionka, rozmiar_czcionki1, bialy, szerokosc - 175, 115, pogrubienie=False)
    rysuj_tekst(f"Średnie: {oczekujace_statki['srednie']}", czcionka, rozmiar_czcionki1, bialy, szerokosc - 175, 135, pogrubienie=False)
    rysuj_tekst(f"Małe: {oczekujace_statki['male']}", czcionka, rozmiar_czcionki1, bialy, szerokosc - 175, 155, pogrubienie=False)
    rysuj_tekst("Dok 1", czcionka, rozmiar_czcionki2, bialy, 130, 370, pogrubienie=True)
    rysuj_tekst("Dok 2", czcionka, rozmiar_czcionki2, bialy, 300, 370, pogrubienie=True)
    rysuj_tekst("Dok 3", czcionka, rozmiar_czcionki2, bialy, 470, 370, pogrubienie=True)

    rysuj_dok(port)
    pygame.display.flip()

pygame.quit()

