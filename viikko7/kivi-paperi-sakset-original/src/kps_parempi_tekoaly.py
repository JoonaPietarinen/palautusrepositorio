from kps import KiviPaperiSakset
from tekoaly_parannettu import TekoalyParannettu

class KPSParempiTekoaly(KiviPaperiSakset):
    def __init__(self):
        self._tekoaly = TekoalyParannettu(10)

    def _toisen_siirto(self):
        siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {siirto}")
        return siirto

    def _toisen_siirto_jatko(self, ekan_siirto):
        self._tekoaly.aseta_siirto(ekan_siirto)
        return self._toisen_siirto()
