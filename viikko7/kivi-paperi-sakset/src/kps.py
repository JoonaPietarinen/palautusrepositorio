from tuomari import Tuomari

class KiviPaperiSakset:
    def pelaa(self):
        tuomari = Tuomari()
        ekan = self._ensimmaisen_siirto()
        tokan = self._toisen_siirto()

        while self._onko_ok_siirto(ekan) and self._onko_ok_siirto(tokan):
            tuomari.kirjaa_siirto(ekan, tokan)
            print(tuomari)

            ekan = self._ensimmaisen_siirto()
            tokan = self._toisen_siirto_jatko(ekan)

        print("Kiitos!")
        print(tuomari)

    def _ensimmaisen_siirto(self):
        return input("Ensimmisen pelaajan siirto: ")

    def _toisen_siirto(self):
        raise NotImplementedError

    def _toisen_siirto_jatko(self, ekan_siirto):
        return self._toisen_siirto()

    def _onko_ok_siirto(self, s):
        return s in ("k", "p", "s")
