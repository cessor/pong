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
        breite=config.fensterBreite * 2//3,
        hoehe=config.fensterHoehe * 1//3,
        vordergrundFarbe=config.schwarz,
        hintergrundFarbe=config.weiss,
        schrift=config.schrift(),
        text='Willkommen zu Pong\nSpielstart mit beliebiger Taste'
    )

    ## hier Objekt ball von Klasse Ball anlegen
    ## und mit Parametern (x, y, breite, hoehe, geschwindigkeit) initialisieren
    ball = Ball(
        x=config.fensterBreite/2-20,
        y=config.fensterHoehe/2-20,
        breite=config.linienDicke,
        hoehe=config.linienDicke,
        geschwindigkeit=5
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
        geschwindigkeit=5,
        ball=ball
    )

    ## Objekt punkte_anzeige von Klasse PunkteAnzeige wird angelegt
    ## und mit Parametern (punkte, x, y, schrift) initialisiert
    punkte_anzeige = PunkteAnzeige(
        punkte=0,
        x=config.fensterBreite - 150,
        y=25,
        schrift=config.schrift()
    )

    ## Aufruf der Methode run der Klasse Spiel
    Spiel(spielfeld, spieler, computer, ball, punkte_anzeige, willkommen).run()

# Aufruf der Main-Funktion
if __name__=='__main__':
    main()
