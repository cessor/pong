### Spiel Pong programmiert mit Python und Bibliotheken pygame und spiel
### Loesung der Aufgabe im Praesenzunterricht
### Stand Dez 2017, Copyright Wilhelm Buechner Hochschule

from spiel import *

# das Hauptprogramm, Einstiegspunkt fuer den Aufruf vom Betriebssystem
def main():

    '''Konkrete Instanzen hier deklarieren'''

    # Die Abhängigkeit wird von aussen erzeugt:
    willkommen = Willkommen(
        x=config.welcome_screen_x(),
        y=config.welcome_screen_x(),
        breite=config.welcome_screen_width(),
        hoehe=config.welcome_screen_height(),
        vordergrundFarbe=config.schwarz,
        hintergrundFarbe=config.weiss,
        schrift=config.schrift(),
        text='Willkommen zu Pong\nSpielstart mit beliebiger Taste'
    )

    ## hier Objekt ball von Klasse Ball anlegen
    ## und mit Parametern (x, y, breite, hoehe, geschwindigkeit) initialisieren
    ball = Ball(
        x=config.ball_x(),
        y=config.ball_y(),
        breite=config.linienDicke,
        hoehe=config.linienDicke,
        geschwindigkeit=config.geschwindigkeit
    )

    ## hier Objekt spieler von Klasse Schlaeger anlegen
    ## und mit Parametern (x, y, breite, hoehe, geschwindigkeit) initialisieren
    spieler = Schlaeger(
        x=config.linker_rand(),
        y=config.schlaeger_mitte(),
        breite=config.schlaegerBreite,
        hoehe=config.schlaegerHoehe,
        geschwindigkeit=0,
    )

    ## hier Objekt spielfeld von Klasse Spielfeld anlegen (keine Parameter)
    spielfeld = Spielfeld()

    ## Objekt computer von Klasse AutoSchlaeger wird angelegt
    ## und mit Parametern (x, y, breite, hoehe, geschwindigkeit, farbe) initialisiert
    ## Objekt ball wird uebergeben, damit computer Schlaeger dem ball folgen kann
    computer = AutoSchlaeger(
        x=config.rechter_rand(),
        y=config.schlaeger_mitte(),
        breite=config.schlaegerBreite,
        hoehe=config.schlaegerHoehe,
        geschwindigkeit=config.geschwindigkeit,
        ball=ball
    )

    ## Objekt punkte_anzeige von Klasse PunkteAnzeige wird angelegt
    ## und mit Parametern (punkte, x, y, schrift) initialisiert
    punkte_anzeige = PunkteAnzeige(
        punkte=0,
        x=config.punkte_x(),
        y=config.punkte_y(),
        schrift=config.schrift()
    )


    ## Aufruf der Methode run der Klasse Spiel
    Spiel(
        # Separate Game States
        SplashScreen(willkommen),
        Playing(spielfeld, spieler, computer, ball, punkte_anzeige)
    ).run()

# Aufruf der Main-Funktion
if __name__=='__main__':
    main()
