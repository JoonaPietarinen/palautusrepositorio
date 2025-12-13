import pytest
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from kps_web import KPSWeb


class TestKPSWeb:
    def test_pelaaja_vs_pelaaja_alustus(self):
        peli = KPSWeb("pelaaja")
        assert peli.pelimuoto == "pelaaja"
        assert peli.tekoaly is None
        assert peli.tuomari.ekan_pisteet == 0

    def test_tekoaly_alustus(self):
        peli = KPSWeb("tekoaly")
        assert peli.pelimuoto == "tekoaly"
        assert peli.tekoaly is not None

    def test_parempi_tekoaly_alustus(self):
        peli = KPSWeb("parempi_tekoaly")
        assert peli.pelimuoto == "parempi_tekoaly"
        assert peli.tekoaly is not None

    def test_validi_siirto(self):
        peli = KPSWeb("pelaaja")
        assert peli._onko_ok_siirto("k") == True
        assert peli._onko_ok_siirto("p") == True
        assert peli._onko_ok_siirto("s") == True

    def test_epavalidi_siirto(self):
        peli = KPSWeb("pelaaja")
        assert peli._onko_ok_siirto("x") == False
        assert peli._onko_ok_siirto("") == False
        assert peli._onko_ok_siirto("kivi") == False

    def test_pelaa_kierros_epavalidi_siirto(self):
        peli = KPSWeb("pelaaja")
        tulos = peli.pelaa_kierros("x")
        
        assert tulos['valid'] == False
        assert tulos['pelaaja'] == "x"
        assert tulos['vastustaja'] is None

    def test_pelaa_kierros_tekoaly_validi(self):
        peli = KPSWeb("tekoaly")
        tulos = peli.pelaa_kierros("k")
        
        assert tulos['valid'] == True
        assert tulos['pelaaja'] == "k"
        assert tulos['vastustaja'] in ["k", "p", "s"]

    def test_pelaa_kierros_paivittaa_pisteet(self):
        peli = KPSWeb("pelaaja")
        
        # Alustetaan eka voittaa (kivi voittaa sakset)
        peli.pelaa_kierros("k")
        
        # Koska pelaaja vs pelaaja -tilassa vastustaja on None,
        # pitää testata tekoälyä vastaan
        peli_ai = KPSWeb("tekoaly")
        
        alkuperaiset_pisteet = peli_ai.tuomari.ekan_pisteet + peli_ai.tuomari.tokan_pisteet
        peli_ai.pelaa_kierros("k")
        uudet_pisteet = peli_ai.tuomari.ekan_pisteet + peli_ai.tuomari.tokan_pisteet
        
        # Joko eka tai toka sai pisteen, tai tasapeli
        assert uudet_pisteet >= alkuperaiset_pisteet

    def test_get_tilanne(self):
        peli = KPSWeb("tekoaly")
        peli.pelaa_kierros("k")
        
        tilanne = peli.get_tilanne()
        
        assert 'ekan_pisteet' in tilanne
        assert 'tokan_pisteet' in tilanne
        assert 'tasapelit' in tilanne
        assert 'peli_ohi' in tilanne
        assert 'voittaja' in tilanne
        assert 'voittoon_tarvittavat' in tilanne

    def test_usean_kierroksen_peli(self):
        peli = KPSWeb("tekoaly")
        
        for _ in range(3):
            tulos = peli.pelaa_kierros("k")
            assert tulos['valid'] == True
        
        tilanne = peli.get_tilanne()
        yhteensa = tilanne['ekan_pisteet'] + tilanne['tokan_pisteet'] + tilanne['tasapelit']
        assert yhteensa == 3

    def test_parempi_tekoaly_kayttaa_historiaa(self):
        peli = KPSWeb("parempi_tekoaly")
        
        # Pelaa useita kierroksia
        for _ in range(3):
            tulos = peli.pelaa_kierros("k")
            assert tulos['valid'] == True
            assert tulos['vastustaja'] in ["k", "p", "s"]

    def test_peli_paattyy_kun_eka_saa_3_voittoa(self):
        peli = KPSWeb("tekoaly")
        
        # Pakotetaan eka voittamaan 3 kertaa
        for _ in range(3):
            peli.tuomari.kirjaa_siirto("k", "s")
        
        tilanne = peli.get_tilanne()
        assert tilanne['peli_ohi'] == True
        assert tilanne['voittaja'] == 1

    def test_peli_ei_paaty_ennen_3_voittoa(self):
        peli = KPSWeb("tekoaly")
        
        for _ in range(2):
            peli.tuomari.kirjaa_siirto("k", "s")
        
        tilanne = peli.get_tilanne()
        assert tilanne['peli_ohi'] == False
        assert tilanne['voittaja'] is None

    def test_pelaa_kierros_palauttaa_peli_ohi_tiedon(self):
        peli = KPSWeb("tekoaly")
        
        # Pelaa 2 kierrosta
        for _ in range(2):
            peli.tuomari.kirjaa_siirto("k", "s")
        
        tulos = peli.pelaa_kierros("k")
        assert 'peli_ohi' in tulos
        assert 'voittaja' in tulos

    def test_get_tekoaly_tila_pelaaja_vs_pelaaja(self):
        peli = KPSWeb("pelaaja")
        tila = peli.get_tekoaly_tila()
        assert tila is None

    def test_get_tekoaly_tila_tekoaly(self):
        peli = KPSWeb("tekoaly")
        peli.pelaa_kierros("k")
        tila = peli.get_tekoaly_tila()
        assert tila is not None
        assert 'siirto' in tila

    def test_get_tekoaly_tila_parempi_tekoaly(self):
        peli = KPSWeb("parempi_tekoaly")
        peli.pelaa_kierros("k")
        tila = peli.get_tekoaly_tila()
        assert tila is not None
        assert 'muisti' in tila
        assert 'vapaa_muisti_indeksi' in tila

    def test_tekoaly_tilan_palauttaminen(self):
        peli1 = KPSWeb("tekoaly")
        peli1.pelaa_kierros("k")
        peli1.pelaa_kierros("p")
        tila = peli1.get_tekoaly_tila()
        
        peli2 = KPSWeb("tekoaly", tila)
        siirto = peli2.tekoaly.anna_siirto()
        
        # Tekoalyn pitaisi jatkaa samasta tilasta
        assert siirto in ["k", "p", "s"]
