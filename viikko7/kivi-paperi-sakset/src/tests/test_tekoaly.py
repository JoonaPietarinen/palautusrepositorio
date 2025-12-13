import pytest
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from tekoaly import Tekoaly


class TestTekoaly:
    def setup_method(self):
        self.tekoaly = Tekoaly()

    def test_tekoaly_alustus(self):
        assert self.tekoaly._siirto == 0

    def test_tekoaly_ensimmainen_siirto(self):
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "p"

    def test_tekoaly_toinen_siirto(self):
        self.tekoaly.anna_siirto()  # p
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "s"

    def test_tekoaly_kolmas_siirto(self):
        self.tekoaly.anna_siirto()  # p
        self.tekoaly.anna_siirto()  # s
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"

    def test_tekoaly_sykli(self):
        # Tarkistetaan että sykli toistuu
        siirrot = []
        for _ in range(6):
            siirrot.append(self.tekoaly.anna_siirto())
        
        assert siirrot == ["p", "s", "k", "p", "s", "k"]

    def test_aseta_siirto_ei_tee_mitaan(self):
        self.tekoaly.aseta_siirto("k")
        # Metodi ei tee mitään, mutta ei myöskään kaadu
        assert self.tekoaly._siirto == 0
