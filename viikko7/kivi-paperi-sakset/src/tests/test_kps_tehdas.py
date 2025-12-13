import pytest
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from kps_tehdas import luo_peli
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


class TestKpsTehdas:
    def test_luo_pelaaja_vs_pelaaja(self):
        peli = luo_peli("a")
        assert isinstance(peli, KPSPelaajaVsPelaaja)

    def test_luo_tekoaly(self):
        peli = luo_peli("b")
        assert isinstance(peli, KPSTekoaly)

    def test_luo_parempi_tekoaly(self):
        peli = luo_peli("c")
        assert isinstance(peli, KPSParempiTekoaly)

    def test_virheellinen_valinta_palauttaa_none(self):
        peli = luo_peli("d")
        assert peli is None

    def test_tyhja_valinta_palauttaa_none(self):
        peli = luo_peli("")
        assert peli is None

    def test_numero_valinta_palauttaa_none(self):
        peli = luo_peli("1")
        assert peli is None
