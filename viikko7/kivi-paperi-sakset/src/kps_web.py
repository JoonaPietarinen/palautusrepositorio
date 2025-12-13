from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu


class KPSWeb:
    """Web-versio pelista, joka ei kayta input()-komentoja."""
    
    def __init__(self, pelimuoto, tekoaly_tila=None):
        self.tuomari = Tuomari()
        self.pelimuoto = pelimuoto
        self.tekoaly = None
        
        if pelimuoto == "tekoaly":
            self.tekoaly = Tekoaly()
            if tekoaly_tila and 'siirto' in tekoaly_tila:
                self.tekoaly._siirto = tekoaly_tila['siirto']
        elif pelimuoto == "parempi_tekoaly":
            self.tekoaly = TekoalyParannettu(10)
            if tekoaly_tila:
                if 'muisti' in tekoaly_tila:
                    self.tekoaly._muisti = tekoaly_tila['muisti']
                if 'vapaa_muisti_indeksi' in tekoaly_tila:
                    self.tekoaly._vapaa_muisti_indeksi = tekoaly_tila['vapaa_muisti_indeksi']
    
    def pelaa_kierros(self, pelaajan_siirto):
        """
        Pelaa yhden kierroksen.
        Palauttaa dict: {
            'pelaaja': pelaajan siirto,
            'vastustaja': vastustajan siirto,
            'valid': oliko siirto validi,
            'tuomari': tuomarin tila str-muodossa,
            'peli_ohi': onko peli paattynyt,
            'voittaja': voittaja (1 tai 2) tai None
        }
        """
        if not self._onko_ok_siirto(pelaajan_siirto):
            return {
                'pelaaja': pelaajan_siirto,
                'vastustaja': None,
                'valid': False,
                'tuomari': str(self.tuomari),
                'peli_ohi': self.tuomari.onko_peli_ohi(),
                'voittaja': self.tuomari.voittaja()
            }
        
        vastustajan_siirto = self._vastustajan_siirto(pelaajan_siirto)
        
        self.tuomari.kirjaa_siirto(pelaajan_siirto, vastustajan_siirto)
        
        return {
            'pelaaja': pelaajan_siirto,
            'vastustaja': vastustajan_siirto,
            'valid': True,
            'tuomari': str(self.tuomari),
            'peli_ohi': self.tuomari.onko_peli_ohi(),
            'voittaja': self.tuomari.voittaja()
        }
    
    def _vastustajan_siirto(self, pelaajan_siirto):
        """Palauttaa vastustajan siirron pelimuodon mukaan."""
        if self.pelimuoto == "pelaaja":
            return None
        elif self.pelimuoto == "tekoaly":
            return self.tekoaly.anna_siirto()
        elif self.pelimuoto == "parempi_tekoaly":
            self.tekoaly.aseta_siirto(pelaajan_siirto)
            return self.tekoaly.anna_siirto()
        return None
    
    def _onko_ok_siirto(self, s):
        """Tarkistaa, onko siirto kelvollinen (k, p tai s)."""
        return s in ("k", "p", "s")
    
    def get_tilanne(self):
        """Palauttaa pelin tilanteen."""
        return {
            'ekan_pisteet': self.tuomari.ekan_pisteet,
            'tokan_pisteet': self.tuomari.tokan_pisteet,
            'tasapelit': self.tuomari.tasapelit,
            'peli_ohi': self.tuomari.onko_peli_ohi(),
            'voittaja': self.tuomari.voittaja(),
            'voittoon_tarvittavat': self.tuomari.voittoon_tarvittavat_pisteet
        }
    
    def get_tekoaly_tila(self):
        """Palauttaa tekoalyn tilan tallennettavaksi."""
        if self.tekoaly is None:
            return None
        
        if self.pelimuoto == "tekoaly":
            return {'siirto': self.tekoaly._siirto}
        elif self.pelimuoto == "parempi_tekoaly":
            return {
                'muisti': self.tekoaly._muisti.copy(),
                'vapaa_muisti_indeksi': self.tekoaly._vapaa_muisti_indeksi
            }
        return None
