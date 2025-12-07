class Summa:
    def __init__(self, sovelluslogiikka, lue_syote, historia):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._historia = historia

    def suorita(self):
        self._historia.append(self._sovelluslogiikka.arvo())
        try:
            arvo = int(self._lue_syote())
        except Exception:
            arvo = 0

        self._sovelluslogiikka.plus(arvo)


class Erotus:
    def __init__(self, sovelluslogiikka, lue_syote, historia):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._historia = historia

    def suorita(self):
        self._historia.append(self._sovelluslogiikka.arvo())
        try:
            arvo = int(self._lue_syote())
        except Exception:
            arvo = 0

        self._sovelluslogiikka.miinus(arvo)


class Nollaus:
    def __init__(self, sovelluslogiikka, lue_syote, historia):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._historia = historia

    def suorita(self):
        self._historia.append(self._sovelluslogiikka.arvo())
        self._sovelluslogiikka.nollaa()

class Kumoa:
    def __init__(self, sovelluslogiikka, historia):
        self._sovelluslogiikka = sovelluslogiikka
        self._historia = historia

    def suorita(self):
        if not self._historia:
            edellinen = 0
        else:
            edellinen = self._historia.pop()

        self._sovelluslogiikka.aseta_arvo(edellinen)

