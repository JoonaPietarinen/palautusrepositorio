import pytest
import sys
from pathlib import Path

# Lis‰‰ src-hakemisto Python-polkuun
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from tuomari import Tuomari


class TestTuomari:
    def setup_method(self):
        self.tuomari = Tuomari()

    def test_tuomari_alustus(self):
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0
        assert self.tuomari.voittoon_tarvittavat_pisteet == 3

    def test_tuomari_custom_voittopisteilla(self):
        tuomari = Tuomari(voittoon_tarvittavat_pisteet=3)
        assert tuomari.voittoon_tarvittavat_pisteet == 3

    def test_tasapeli(self):
        self.tuomari.kirjaa_siirto("k", "k")
        assert self.tuomari.tasapelit == 1
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0

    def test_eka_voittaa_kivi_voittaa_sakset(self):
        self.tuomari.kirjaa_siirto("k", "s")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_eka_voittaa_paperi_voittaa_kiven(self):
        self.tuomari.kirjaa_siirto("p", "k")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0

    def test_eka_voittaa_sakset_voittaa_paperin(self):
        self.tuomari.kirjaa_siirto("s", "p")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0

    def test_toka_voittaa_kivi_voittaa_sakset(self):
        self.tuomari.kirjaa_siirto("s", "k")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1

    def test_toka_voittaa_paperi_voittaa_kiven(self):
        self.tuomari.kirjaa_siirto("k", "p")
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.ekan_pisteet == 0

    def test_toka_voittaa_sakset_voittaa_paperin(self):
        self.tuomari.kirjaa_siirto("p", "s")
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.ekan_pisteet == 0

    def test_usean_kierroksen_pisteet(self):
        self.tuomari.kirjaa_siirto("k", "s")  # eka voittaa
        self.tuomari.kirjaa_siirto("p", "p")  # tasapeli
        self.tuomari.kirjaa_siirto("s", "k")  # toka voittaa
        
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 1

    def test_tuomari_str(self):
        self.tuomari.kirjaa_siirto("k", "s")
        tulos = str(self.tuomari)
        assert "1 - 0" in tulos
        assert "Tasapelit: 0" in tulos

    def test_peli_ei_ohi_alussa(self):
        assert self.tuomari.onko_peli_ohi() == False
        assert self.tuomari.voittaja() is None

    def test_peli_ohi_kun_eka_saa_3_voittoa(self):
        for _ in range(3):
            self.tuomari.kirjaa_siirto("k", "s")
        
        assert self.tuomari.onko_peli_ohi() == True
        assert self.tuomari.voittaja() == 1

    def test_peli_ohi_kun_toka_saa_3_voittoa(self):
        for _ in range(3):
            self.tuomari.kirjaa_siirto("s", "k")
        
        assert self.tuomari.onko_peli_ohi() == True
        assert self.tuomari.voittaja() == 2

    def test_peli_ei_ohi_kun_molemmat_alle_3(self):
        for _ in range(2):
            self.tuomari.kirjaa_siirto("k", "s")
        for _ in range(2):
            self.tuomari.kirjaa_siirto("s", "k")
        
        assert self.tuomari.onko_peli_ohi() == False
        assert self.tuomari.voittaja() is None

    def test_peli_ohi_custom_voittopisteilla(self):
        tuomari = Tuomari(voittoon_tarvittavat_pisteet=3)
        
        for _ in range(3):
            tuomari.kirjaa_siirto("k", "s")
        
        assert tuomari.onko_peli_ohi() == True
        assert tuomari.voittaja() == 1
