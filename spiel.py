# Bibliothek spiel.py
# Stand Dez 2017, Copyright Wilhelm Buechner Hochschule

import pygame
import sys
import time


class Einstellungen(object):
    fps = 40  # Frames pro Sekunde

    # Farben
    schwarz = (0, 0, 0)
    weiss = (255, 255, 255)

    # Dimensionen
    fensterBreite = 640
    fensterHoehe = 480
    linienDicke = 10
    abstand = 2*linienDicke
    schlaegerBreite = 10
    schlaegerHoehe = 50
    schriftGroesse = 16
    ballRadius = 5  # nur fuer runden Ball notwendig
    geschwindigkeit = 5

    def __init__(self):
        # Notwendige Initialisierung fuer pygame
        pygame.init()
        pygame.display.set_caption('Pong')
        pygame.mouse.set_visible(0)  # setze Mauszeiger unsichtbar

    def fenster_mitte(self):
        return self.fensterHoehe // 2

    def schlaeger_mitte(self):
        return self.fenster_mitte() - self.schlaegerHoehe // 2

    def linker_rand(self):
        return self.abstand

    def rechter_rand(self):
        return self.fensterBreite - self.schlaegerBreite - self.abstand

    def schrift(self):
        return pygame.font.SysFont('arial', self.schriftGroesse, bold=True)

    def ball_x(self):
        return self.fensterBreite / 2-20

    def ball_y(self):
        return self.fensterHoehe  / 2-20

    def welcome_screen_height(self):
        return self.fensterHoehe * 1//3

    def welcome_screen_width(self):
        return self.fensterBreite * 2//3

    def welcome_screen_x(self):
        return self.abstand + 80

    def welcome_screen_y(self):
        return self.abstand + 60

    def punkte_x(self):
        return self.fensterBreite - 150

    def punkte_y(self):
        return 25



'''Idealer Weise waere dies kein globales Objekt'''
config = Einstellungen()


class Form(pygame.sprite.Sprite):

    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=config.weiss):
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.farbe = farbe
        self.geschwindigkeit = geschwindigkeit


class Rectangle(Form):

    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=config.weiss):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.rect = pygame.Rect(self.x, self.y, self.breite, self.hoehe)

    def draw(self, fensterFlaeche):
        pygame.draw.rect(fensterFlaeche, self.farbe, self.rect)


class Circle(Form):

    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=config.weiss):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.rect = pygame.Rect(self.x, self.y, self.breite, self.hoehe)
        self.radius = config.ballRadius

    def draw(self, fensterFlaeche):
        pygame.draw.circle(fensterFlaeche, self.farbe,
                           (self.rect.x, self.rect.y), self.radius)

class Willkommen():
    # Willkommensbildschirm beim Programmstart
    def __init__(self, x, y, breite, hoehe, vordergrundFarbe, hintergrundFarbe, schrift, text):
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.vordergrundFarbe = vordergrundFarbe
        self.hintergrundFarbe = hintergrundFarbe
        self.schrift = schrift
        self.text = text

    def draw(self, fensterFlaeche):
        self._draw_screen(fensterFlaeche)
        self._draw_text(fensterFlaeche)

    def _draw_screen(self, fensterFlaeche):
        popupFenster = pygame.Rect(self.x, self.y, self.breite, self.hoehe)
        fensterFlaeche.fill(self.hintergrundFarbe, popupFenster)

    def _bottom_y(self, text_height):
        return self.y + self.hoehe - text_height

    def _center_x(self, text_width):
        return self.x + (self.breite // 2) - (text_width // 2)

    def _center_y(self, text_height):
        return self.y + (self.hoehe // 2) - (text_height // 2)

    def _draw_text(self, fensterFlaeche):
        '''
            Diese Methode ist sehr redundant.
            Wenn noch mehr Text gezeichnet werden muss,
            würde ich sie weiter strukturieren und die X und Y offsets
            parametrisieren. Die Beiden Blöcke unterscheiden sich
            nur anhand ihres Y Offsets,
            eine Zeile steht in der mitte die andere am unteren Rand
        '''
        zeile1, zeile2  = self.text.split('\n')

        # Message at center
        text_width, text_height = self.schrift.size(zeile1)
        text_region = self.schrift.render(zeile1, False,
                                          self.vordergrundFarbe)
        x = self._center_x(text_width)
        y = self._center_y(text_height)
        fensterFlaeche.blit(text_region, (x, y))

        # Spielstart at Bottom
        text_width, text_height = self.schrift.size(zeile2)
        text_region = self.schrift.render(zeile2, False,
                                          self.vordergrundFarbe)
        x = self._center_x(text_width)
        y = self._bottom_y(text_height) # (1)
        fensterFlaeche.blit(text_region, (x, y))

        # (1) Das hier ist der einzige Unterschied zum Block weiter oben


class Spiel():
    # Initialisierung (OOP Konstruktor)

    def __init__(self, spielfeld, spieler, computer, ball, punkte_anzeige, willkommen):
        self.punkte = 0

        self._fpsTimer = pygame.time.Clock()
        self._fensterFlaeche = pygame.display.set_mode(
            (config.fensterBreite, config.fensterHoehe))

        # Der Konstruktor merkt sich lediglich die Abhängigkeiten
        self._spielfeld = spielfeld
        self._spieler = spieler
        self._computer = computer
        self._ball = ball
        self._allSchlaeger = [self._spieler, self._computer]  # Liste
        self._punkteAnzeige = punkte_anzeige
        self._willkommen = willkommen

    def run(self):
        '''
        Spielschleife - Game Loop Pattern, siehe auch:
        http://gameprogrammingpatterns.com/game-loop.html
        '''
        running = False
        # Willkommensbildschirm anzeigen, weiter mit Taste
        while running == False:

            # Hier stand vormals ein Konstruktoraufruf
            self._willkommen.draw(self._fensterFlaeche)
            pygame.display.update()
            # Ueberpruefe ob Taste gedrueckt wurde
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    running = True
        # Spielschleife
        while running:
            self._ereignisse_behandeln()
            self._update()
            self._zeichnen()
            pygame.display.update()
            self._fpsTimer.tick(config.fps)

    def _ereignisse_behandeln(self):
        # Ereignis abfragen
        for ereignis in pygame.event.get():
            self._behandle(ereignis)

    def _behandle(self, event):
        # Ueberpruefe ob Schliessen-Symbol im Fenster gedrueckt wurde
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return
        # Ueberpruefe ob Maus bewegt wurde
        elif event.type == pygame.MOUSEMOTION:
            self._spieler.move(event.pos)
            return
        return event

    def _update(self):
        self._bewegen()
        self._aufprall_berechnen()

    def _bewegen(self):
        self._ball.move()
        self._computer.move(self._ball)

    def _aufprall_berechnen(self):
        if self._ball.hit_schlaeger(self._computer):
            self._ball.bounce('x')

        elif self._ball.hit_schlaeger(self._spieler):
            self._ball.bounce('x')
            self.punkte += 1

        elif self._ball.trefferComputer():
            self.punkte += 5

        elif self._ball.trefferSpieler():
            self.punkte = 0

    def _zeichnen(self):
        self._spielfeld.draw(self._fensterFlaeche)
        self._ball.draw(self._fensterFlaeche)
        for schlaeger in self._allSchlaeger:
            schlaeger.draw(self._fensterFlaeche)
        self._punkteAnzeige.draw(self.punkte, self._fensterFlaeche)


class Spielfeld(object):

    def draw(self, fensterFlaeche):
        fensterFlaeche.fill(config.schwarz)
        self._umrandung(fensterFlaeche)
        self._mittellinie(fensterFlaeche)

    def _umrandung(self, fensterFlaeche):
        pygame.draw.rect(fensterFlaeche, config.weiss,
                         ((0, 0), (config.fensterBreite, config.fensterHoehe)),
                         config.linienDicke*2)

    def _mittellinie(self, fensterFlaeche):
        pygame.draw.line(fensterFlaeche, config.weiss,
                         (config.fensterBreite//2, 0),
                         (config.fensterBreite//2, config.fensterHoehe),
                         config.linienDicke//4)


class Ball(Rectangle):  # Alternativer Parameter: Circle
    # Pfeiltasten
    LEFT = -1
    RIGHT = 1
    UP = -1
    DOWN = 1

    # Initialisierung (OOP Konstruktor)
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=config.weiss):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.richtungX = self.LEFT
        self.richtungY = self.UP

    # Funktion zum Bewegen des Balls, neue Position setzen
    def move(self):
        self.rect.x += (self.richtungX * self.geschwindigkeit)
        self.rect.y += (self.richtungY * self.geschwindigkeit)

        # Pruefe Kollision mit Wand
        if self.hit_ceiling() or self.hit_floor():
            self.bounce('y')
        if self.hit_wall():
            self.bounce('x')

    # Richtungsaenderung fuer Ball
    def bounce(self, axis):
        if axis == 'x':
            self.richtungX *= -1
        elif axis == 'y':
            self.richtungY *= -1

    # Treffen von Ball auf Schlaeger
    def hit_schlaeger(self, schlaeger):
        return pygame.sprite.collide_rect(self, schlaeger)

    # Treffen von Ball auf Wand links oder rechts
    def hit_wall(self):
        return (
            (self.richtungX == -1
                and self.rect.left <= self.breite) or
            (self.richtungX == 1
                and self.rect.right >= config.fensterBreite - self.breite)
        )

    # Treffen von Ball auf Decke
    def hit_ceiling(self):
        return self.richtungY == -1 and self.rect.top <= self.breite

    # Treffen von Ball auf Boden
    def hit_floor(self):
        return (self.richtungY == 1
                and self.rect.bottom >= config.fensterHoehe - self.breite)

    def trefferSpieler(self):
        return self.rect.left <= self.breite

    def trefferComputer(self):
        return self.rect.right >= config.fensterBreite - self.breite


class Schlaeger(Rectangle):
    # Funktion zum Zeichnen des Schlaegers

    def draw(self, fensterFlaeche):
        # Stoppt Schlaeger am unteren Spielfeldrand
        if self.rect.bottom > config.fensterHoehe - config.linienDicke:
            self.rect.bottom = config.fensterHoehe - config.linienDicke
        # Stoppt Schlaeger am oberen Spielfeldrand
        elif self.rect.top < config.linienDicke:
            self.rect.top = config.linienDicke+1  # randkorrektur

        super().draw(fensterFlaeche)

    # Funktion zum Bewegen des Schlaegers mit Maus
    def move(self, pos):
        self.rect.y = pos[1]


class AutoSchlaeger(Schlaeger):
    # Initialisierung (OOP Konstruktor)

    def __init__(self, x, y, breite, hoehe, geschwindigkeit, ball, farbe=config.weiss):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self._ball = ball

    # Automatische Bewegung, richtet sich nach dem Ball
    def move(self, pos):
        # Wenn Ball sich vom Schlaeger wegbewegt, zentriere ihn
        if self._ball.richtungX == -1:
            self._zentrieren()
        # Wenn Ball sich auf Schlaeger zubewegt, beoachte seine Bewegung
        elif self._ball.richtungX == 1:
            self._beobachten()

    def _beobachten(self):
        if self.rect.centery < self._ball.rect.centery:
            self.rect.y += self.geschwindigkeit
        else:
            self.rect.y -= self.geschwindigkeit

    def _zentrieren(self):
        if self.rect.centery < config.fenster_mitte():
            self.rect.y += self.geschwindigkeit
        elif self.rect.centery > config.fenster_mitte():
            self.rect.y -= self.geschwindigkeit


class PunkteAnzeige():
    # Initialisierung (OOP Konstruktor)

    def __init__(self, punkte, x, y, schrift):
        self.punkte = punkte
        self.x = x
        self.y = y
        self.schrift = schrift

    # Schreibe aktuellen Punktestand an den Bildschirm
    def draw(self, punkte, fensterFlaeche):
        self.punkte = punkte
        result_surf = self.schrift.render(
            'Punkte: %s' % (self.punkte), True, config.weiss)
        rect = result_surf.get_rect()
        rect.topleft = (self.x, self.y)
        fensterFlaeche.blit(result_surf, rect)
