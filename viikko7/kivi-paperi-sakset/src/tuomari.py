

# Luokka pitaa kirjaa ensimmaisen ja toisen pelaajan pisteista seka tasapelien maarasta.
class Tuomari:
    def __init__(self, voittoon_tarvittavat_pisteet=3):
        self.ekan_pisteet = 0
        self.tokan_pisteet = 0
        self.tasapelit = 0
        self.voittoon_tarvittavat_pisteet = voittoon_tarvittavat_pisteet

    def kirjaa_siirto(self, ekan_siirto, tokan_siirto):
        if self._tasapeli(ekan_siirto, tokan_siirto):
            self.tasapelit = self.tasapelit + 1
        elif self._eka_voittaa(ekan_siirto, tokan_siirto):
            self.ekan_pisteet = self.ekan_pisteet + 1
        else:
            self.tokan_pisteet = self.tokan_pisteet + 1

    def onko_peli_ohi(self):
        """Tarkistaa onko peli paattynyt (jompikumpi saanut tarvittavan maaran voittoja)."""
        return self.ekan_pisteet >= self.voittoon_tarvittavat_pisteet or self.tokan_pisteet >= self.voittoon_tarvittavat_pisteet

    def voittaja(self):
        """Palauttaa voittajan (1 tai 2) tai None jos peli ei ole ohi."""
        if self.ekan_pisteet >= self.voittoon_tarvittavat_pisteet:
            return 1
        elif self.tokan_pisteet >= self.voittoon_tarvittavat_pisteet:
            return 2
        return None

    def __str__(self):
        return f"Pelitilanne: {self.ekan_pisteet} - {self.tokan_pisteet}\nTasapelit: {self.tasapelit}"

    # sisainen metodi, jolla tarkastetaan tuliko tasapeli
    def _tasapeli(self, eka, toka):
        if eka == toka:
            return True

        return False

    # sisainen metodi joka tarkastaa voittaako eka pelaaja tokan
    def _eka_voittaa(self, eka, toka):
        if eka == "k" and toka == "s":
            return True
        elif eka == "s" and toka == "p":
            return True
        elif eka == "p" and toka == "k":
            return True

        return False
