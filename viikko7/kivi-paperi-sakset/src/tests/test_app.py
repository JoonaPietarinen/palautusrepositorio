import pytest
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from app import app


@pytest.fixture
def client():
    """Luo Flask-testiklientin."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        yield client


class TestFlaskApp:
    def test_index_sivu_latautuu(self, client):
        """Testaa etta aloitussivu latautuu."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi-Paperi-Sakset' in response.data

    def test_index_sisaltaa_pelimuodot(self, client):
        """Testaa etta aloitussivu sisaltaa kaikki pelimuodot."""
        response = client.get('/')
        assert b'Pelaaja vs Pelaaja' in response.data
        assert b'Tekoaly' in response.data or b'Tekoaly' in response.data
        assert b'Parannettu' in response.data

    def test_start_pelaaja_pelimuoto(self, client):
        """Testaa pelin aloitus pelaaja vs pelaaja -tilassa."""
        response = client.post('/start', data={
            'pelimuoto': 'pelaaja',
            'pelaaja1_nimi': 'Matti',
            'pelaaja2_nimi': 'Maija'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Pelitilanne' in response.data

    def test_start_tekoaly_pelimuoto(self, client):
        """Testaa pelin aloitus tekoaly-tilassa."""
        response = client.post('/start', data={
            'pelimuoto': 'tekoaly',
            'pelaaja1_nimi': 'Pelaaja'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_start_parempi_tekoaly_pelimuoto(self, client):
        """Testaa pelin aloitus parannettu tekoaly -tilassa."""
        response = client.post('/start', data={
            'pelimuoto': 'parempi_tekoaly',
            'pelaaja1_nimi': 'Pelaaja'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_start_virheellinen_pelimuoto(self, client):
        """Testaa etta virheellinen pelimuoto ohjaa takaisin alkuun."""
        response = client.post('/start', data={'pelimuoto': 'virheellinen'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Valitse pelimuoto' in response.data

    def test_peli_ilman_sessiota_ohjaa_alkuun(self, client):
        """Testaa etta pelisivulle paasy ilman sessiota ohjaa alkuun."""
        response = client.get('/peli', follow_redirects=True)
        assert response.status_code == 200
        assert b'Valitse pelimuoto' in response.data

    def test_pelisivu_latautuu_kun_sessio_on(self, client):
        """Testaa etta pelisivu latautuu kun sessio on olemassa."""
        with client.session_transaction() as sess:
            sess['pelimuoto'] = 'tekoaly'
            sess['historia'] = []
            sess['peli_data'] = {
                'ekan_pisteet': 0,
                'tokan_pisteet': 0,
                'tasapelit': 0,
                'peli_ohi': False,
                'voittaja': None,
                'voittoon_tarvittavat': 3
            }
            sess['tekoaly_tila'] = None
            sess['odottaa_pelaaja2_siirtoa'] = False
            sess['pelaaja1_siirto'] = None
        
        response = client.get('/peli')
        assert response.status_code == 200
        assert b'Pelitilanne' in response.data

    def test_siirto_ilman_sessiota(self, client):
        """Testaa etta siirto ilman sessiota ohjaa alkuun."""
        response = client.post('/siirto', data={'siirto': 'k'}, follow_redirects=True)
        assert response.status_code == 200

    def test_siirto_tekoalya_vastaan(self, client):
        """Testaa siirron tekeminen tekoalya vastaan."""
        # Alusta sessio
        with client.session_transaction() as sess:
            sess['pelimuoto'] = 'tekoaly'
            sess['historia'] = []
            sess['peli_data'] = {
                'ekan_pisteet': 0,
                'tokan_pisteet': 0,
                'tasapelit': 0,
                'peli_ohi': False,
                'voittaja': None,
                'voittoon_tarvittavat': 3
            }
        
        # Tee siirto
        response = client.post('/siirto', data={'siirto': 'k'}, follow_redirects=True)
        assert response.status_code == 200

    def test_siirto_paivittaa_historiaa(self, client):
        """Testaa etta siirto paivittaa historiaa."""
        # Alusta peli
        client.post('/start', data={'pelimuoto': 'tekoaly'})
        
        # Tee siirto
        client.post('/siirto', data={'siirto': 'k'})
        
        # Tarkista etta pelisivulla nakyy historia
        response = client.get('/peli')
        assert response.status_code == 200

    def test_uusi_peli_tyhjentaa_session(self, client):
        """Testaa etta uusi peli -toiminto tyhjentaa session."""
        # Luo sessio
        with client.session_transaction() as sess:
            sess['pelimuoto'] = 'tekoaly'
            sess['historia'] = [{'pelaaja': 'Kivi', 'vastustaja': 'Sakset'}]
        
        # Aloita uusi peli
        response = client.get('/uusi_peli', follow_redirects=True)
        assert response.status_code == 200
        assert b'Valitse pelimuoto' in response.data

    def test_pelaa_useita_kierroksia(self, client):
        """Testaa usean kierroksen pelaaminen."""
        # Aloita peli
        client.post('/start', data={'pelimuoto': 'tekoaly'})
        
        # Pelaa 3 kierrosta
        siirrot = ['k', 'p', 's', 'k', 'p']
        for siirto in siirrot:
            response = client.post('/siirto', data={'siirto': siirto}, follow_redirects=True)
            assert response.status_code == 200

    def test_epavalidi_siirto_ei_paivita_historiaa(self, client):
        """Testaa etta epavalidi siirto ei paivita historiaa."""
        # Alusta peli
        with client.session_transaction() as sess:
            sess['pelimuoto'] = 'tekoaly'
            sess['historia'] = []
            sess['peli_data'] = {
                'ekan_pisteet': 0,
                'tokan_pisteet': 0,
                'tasapelit': 0,
                'peli_ohi': False,
                'voittaja': None,
                'voittoon_tarvittavat': 3
            }
        
        # Tee epavalidi siirto
        response = client.post('/siirto', data={'siirto': 'x'}, follow_redirects=True)
        assert response.status_code == 200

    def test_pelisivu_nayttaa_oikean_pelimuodon_nimen(self, client):
        """Testaa etta pelisivu nayttaa oikean pelimuodon nimen."""
        client.post('/start', data={'pelimuoto': 'parempi_tekoaly'}, follow_redirects=True)
        response = client.get('/peli')
        assert b'Parannettu' in response.data

    def test_peli_paattyy_kun_pelaaja_saa_3_voittoa(self, client):
        """Testaa etta peli paattyy kun pelaaja saa 3 voittoa."""
        with client.session_transaction() as sess:
            sess['pelimuoto'] = 'tekoaly'
            sess['historia'] = []
            sess['peli_data'] = {
                'ekan_pisteet': 3,
                'tokan_pisteet': 0,
                'tasapelit': 0,
                'peli_ohi': True,
                'voittaja': 1,
                'voittoon_tarvittavat': 3
            }
        
        response = client.get('/peli')
        assert response.status_code == 200
        assert b'PELI OHI' in response.data
        assert b'Pelaaja 1 voitti' in response.data

    def test_siirto_estetaan_kun_peli_ohi(self, client):
        """Testaa etta siirtoa ei voi tehda kun peli on ohi."""
        with client.session_transaction() as sess:
            sess['pelimuoto'] = 'tekoaly'
            sess['historia'] = []
            sess['peli_data'] = {
                'ekan_pisteet': 3,
                'tokan_pisteet': 0,
                'tasapelit': 0,
                'peli_ohi': True,
                'voittaja': 1,
                'voittoon_tarvittavat': 3
            }
        
        response = client.post('/siirto', data={'siirto': 'k'}, follow_redirects=True)
        assert response.status_code == 200

    def test_voittoon_tarvittavat_pisteet_nakyy(self, client):
        """Testaa etta voittoon tarvittavat pisteet nakyy pelisivulla."""
        client.post('/start', data={'pelimuoto': 'tekoaly'})
        response = client.get('/peli')
        assert b'/ 3 voittoa' in response.data

    def test_pelaaja_vs_pelaaja_kaksi_vuoroa(self, client):
        """Testaa etta pelaaja vs pelaaja -pelissa on kaksi vuoroa."""
        client.post('/start', data={
            'pelimuoto': 'pelaaja',
            'pelaaja1_nimi': 'Matti',
            'pelaaja2_nimi': 'Maija'
        })
        
        # Pelaaja 1 tekee siirron
        response = client.post('/siirto', data={'siirto': 'k'}, follow_redirects=False)
        assert response.status_code == 302
        
        # Tarkista etta session odottaa pelaaja 2:n siirtoa
        with client.session_transaction() as sess:
            assert sess.get('odottaa_pelaaja2_siirtoa') == True
            assert sess.get('pelaaja1_siirto') == 'k'
        
        # Pelaaja 2 tekee siirron
        response = client.post('/siirto', data={'siirto': 'p'}, follow_redirects=False)
        assert response.status_code == 302
        
        # Tarkista etta vuoro on paattynyt
        with client.session_transaction() as sess:
            assert sess.get('odottaa_pelaaja2_siirtoa') == False
            assert sess.get('pelaaja1_siirto') is None

    def test_pelaajien_nimet_tallennetaan(self, client):
        """Testaa etta pelaajien nimet tallennetaan sessioon."""
        client.post('/start', data={
            'pelimuoto': 'pelaaja',
            'pelaaja1_nimi': 'Matti',
            'pelaaja2_nimi': 'Maija'
        })
        
        with client.session_transaction() as sess:
            assert sess.get('pelaaja1_nimi') == 'Matti'
            assert sess.get('pelaaja2_nimi') == 'Maija'

    def test_oletusnimet_jos_ei_anneta(self, client):
        """Testaa etta kaytetaan oletusnimet jos ei anneta."""
        client.post('/start', data={'pelimuoto': 'tekoaly'})
        
        with client.session_transaction() as sess:
            assert sess.get('pelaaja1_nimi') == 'Pelaaja 1'
            assert sess.get('pelaaja2_nimi') == 'Tietokone'
