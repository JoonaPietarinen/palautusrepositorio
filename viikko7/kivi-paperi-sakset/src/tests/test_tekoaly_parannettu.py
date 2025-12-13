import pytest
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from tekoaly_parannettu import TekoalyParannettu


class TestTekoalyParannettu:
    def setup_method(self):
        self.tekoaly = TekoalyParannettu(10)

    def test_tekoaly_alustus(self):
        assert len(self.tekoaly._muisti) == 10
        assert self.tekoaly._vapaa_muisti_indeksi == 0

    def test_ensimmainen_siirto_ilman_historiaa(self):
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"

    def test_toinen_siirto_ilman_historiaa(self):
        self.tekoaly.aseta_siirto("k")
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"

    def test_aseta_siirto_tallentaa_muistiin(self):
        self.tekoaly.aseta_siirto("k")
        assert self.tekoaly._muisti[0] == "k"
        assert self.tekoaly._vapaa_muisti_indeksi == 1

    def test_muisti_tayttyy_ja_unohtaa(self):
        # Täytetään muisti
        for i in range(11):
            self.tekoaly.aseta_siirto("k")
        
        # Varmistetaan että indeksi ei ylitä muistin kokoa
        assert self.tekoaly._vapaa_muisti_indeksi == 10

    def test_tekoaly_oppii_pelaajan_mallia(self):
        # Pelaaja pelaa useasti kivi -> paperi
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.anna_siirto()
        
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.anna_siirto()
        
        # Kun pelaaja pelaa kiven, tekoälyn pitäisi odottaa paperia
        # ja pelata sakset
        self.tekoaly.aseta_siirto("k")
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "s"

    def test_eri_muistikoot(self):
        tekoaly_pieni = TekoalyParannettu(3)
        assert len(tekoaly_pieni._muisti) == 3
        
        tekoaly_iso = TekoalyParannettu(20)
        assert len(tekoaly_iso._muisti) == 20
