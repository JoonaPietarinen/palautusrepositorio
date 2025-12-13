from kps_tehdas import luo_peli

def main():
    while True:
        print("Valitse pelataanko"
              "\n (a) Ihmista vastaan"
              "\n (b) Tekoalya vastaan"
              "\n (c) Parannettua tekoalya vastaan"
              "\nMuilla valinnoilla lopetetaan"
              )

        vastaus = input()
        peli = luo_peli(vastaus)
        if not peli:
            break
        print("Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s")
        peli.pelaa()


if __name__ == "__main__":
    main()
