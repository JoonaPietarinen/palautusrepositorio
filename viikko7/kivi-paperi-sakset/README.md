# Kivi-Paperi-Sakset Web-sovellus

## Yleiskatsaus

Web-pohjainen Kivi-Paperi-Sakset-peli, joka on toteutettu Flask-frameworkilla. Sovellus k‰ytt‰‰ olemassa olevaa pelilogiikkaa ja tarjoaa kolme erilaista pelimuotoa.

## Ominaisuudet

### Pelimuodot
1. **Pelaaja vs Pelaaja** - Kaksi pelaajaa pelaa toisiaan vastaan
2. **Pelaaja vs Teko‰ly** - Pelaa yksinkertaista teko‰ly‰ vastaan (kiert‰‰ k ? p ? s)
3. **Pelaaja vs Parannettu Teko‰ly** - Pelaa ‰lyk‰st‰ teko‰ly‰ vastaan, joka oppii pelaajan siirroista

### Pelin kulku
- Peli jatkuu kunnes toinen pelaaja saa **5 voittoa**
- Tasapelit eiv‰t laske voitoksi
- Pelin tulos n‰ytet‰‰n selke‰sti voittajan ilmoituksen kera

### Pelaajien nimet
- Pelaajat voivat syˆtt‰‰ omat nimens‰ aloitussivulla
- Nimet n‰kyv‰t koko pelin ajan
- Jos nimi‰ ei anneta, k‰ytet‰‰n oletusnimi‰ (Pelaaja 1, Pelaaja 2, Tietokone)

### Kaksi pelaajaa -tila
- Pelaaja 1 tekee siirtonsa ? odottaa Pelaaja 2:n siirtoa
- Pelaaja 2 tekee siirtonsa ? kierros k‰sitell‰‰n
- Selke‰t ilmoitukset kenen vuoro on

### Teko‰lyn toiminta
- **Yksinkertainen teko‰ly**: Kiert‰‰ siirtoja j‰rjestyksess‰
- **Parannettu teko‰ly**: Tallentaa pelaajan siirtohistorian ja yritt‰‰ ennustaa seuraavan siirron
- Teko‰lyn tila s‰ilyy kierrosten v‰lill‰ (tallennetaan sessioon)

## K‰ynnistys

### Asenna riippuvuudet
```bash
poetry install
```

### K‰ynnist‰ sovellus
```bash
poetry run python src/app.py
```

Tai suoraan Pythonilla:
```bash
python src/app.py
```

Sovellus k‰ynnistyy osoitteessa: **http://localhost:5001**

## Testit

### Aja kaikki testit
```bash
poetry run pytest src/tests -v
```

Tai suoraan:
```bash
python -m pytest src/tests -v
```

### Testikattavuus
Sovelluksessa on **74 testi‰** jotka kattavat:
- Tuomarin logiikan
- Teko‰lyjen toiminnan
- Web-pelilogiikan
- Flask-sovelluksen endpointit
- Pelin p‰‰ttymisen
- Pelaajien nimien tallennuksen

## Projektirakenne

```
viikko7/kivi-paperi-sakset/
??? src/
?   ??? app.py                      # Flask-sovellus
?   ??? kps_web.py                  # Web-yhteensopiva pelilogiikka
?   ??? tuomari.py                  # Tuomarin logiikka
?   ??? tekoaly.py                  # Yksinkertainen teko‰ly
?   ??? tekoaly_parannettu.py       # Parannettu teko‰ly
?   ??? kps.py                      # Alkuper‰inen pelilogiikka (CLI)
?   ??? kps_tehdas.py              # Pelien luontitehdas (CLI)
?   ??? templates/
?   ?   ??? index.html             # Aloitussivu
?   ?   ??? peli.html              # Pelisivu
?   ??? tests/
?       ??? test_tuomari.py
?       ??? test_tekoaly.py
?       ??? test_tekoaly_parannettu.py
?       ??? test_kps_web.py
?       ??? test_app.py
?       ??? test_kps_tehdas.py
??? pyproject.toml
??? pytest.ini
```

## Tekniset yksityiskohdat

### Flask Session
- K‰ytet‰‰n pelin tilan tallentamiseen
- Tallentaa: pelimuoto, pelaajien nimet, pisteet, historia, teko‰lyn tila

### Teko‰lyn tilan hallinta
- Teko‰lyn sis‰inen tila serialisoidaan ja tallennetaan sessioon
- Tila palautetaan kun luodaan uusi peliinstanssi
- Mahdollistaa teko‰lyn "muistin" kierrosten v‰lill‰

### Turvallinen session key
- Generoidaan satunnainen session key `secrets.token_hex(16)`

## Lisenssi

MIT

## Tekij‰t

- Alkuper‰inen pelilogiikka: Matti Luukkainen
- Web-toteutus ja parannukset: [Projektin kehitt‰j‰]
