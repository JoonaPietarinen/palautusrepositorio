from flask import Flask, render_template, request, session, redirect, url_for
import secrets
from kps_web import KPSWeb

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    """Aloitussivu, jossa valitaan pelimuoto."""
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    """Aloittaa uuden pelin valitulla pelimuodolla."""
    pelimuoto = request.form.get('pelimuoto')
    
    if pelimuoto not in ['pelaaja', 'tekoaly', 'parempi_tekoaly']:
        return redirect(url_for('index'))
    
    # Hae pelaajien nimet
    pelaaja1_nimi = request.form.get('pelaaja1_nimi', '').strip()
    pelaaja2_nimi = request.form.get('pelaaja2_nimi', '').strip()
    
    # Aseta oletusnimet jos ei annettu
    if not pelaaja1_nimi:
        pelaaja1_nimi = 'Pelaaja 1'
    
    if pelimuoto == 'pelaaja' and not pelaaja2_nimi:
        pelaaja2_nimi = 'Pelaaja 2'
    elif pelimuoto != 'pelaaja':
        pelaaja2_nimi = 'Tietokone'
    
    session['pelimuoto'] = pelimuoto
    session['pelaaja1_nimi'] = pelaaja1_nimi
    session['pelaaja2_nimi'] = pelaaja2_nimi
    session['historia'] = []
    session['peli_data'] = {
        'ekan_pisteet': 0,
        'tokan_pisteet': 0,
        'tasapelit': 0,
        'peli_ohi': False,
        'voittaja': None,
        'voittoon_tarvittavat': 3
    }
    session['tekoaly_tila'] = None
    session['odottaa_pelaaja2_siirtoa'] = False
    session['pelaaja1_siirto'] = None
    
    return redirect(url_for('peli'))


@app.route('/peli')
def peli():
    """Pelisivu."""
    if 'pelimuoto' not in session:
        return redirect(url_for('index'))
    
    pelimuoto = session['pelimuoto']
    historia = session.get('historia', [])
    peli_data = session.get('peli_data', {})
    odottaa_pelaaja2 = session.get('odottaa_pelaaja2_siirtoa', False)
    pelaaja1_siirto = session.get('pelaaja1_siirto', None)
    pelaaja1_nimi = session.get('pelaaja1_nimi', 'Pelaaja 1')
    pelaaja2_nimi = session.get('pelaaja2_nimi', 'Pelaaja 2' if pelimuoto == 'pelaaja' else 'Tietokone')
    
    pelimuoto_nimet = {
        'pelaaja': 'Pelaaja vs Pelaaja',
        'tekoaly': 'Pelaaja vs Tekoaly',
        'parempi_tekoaly': 'Pelaaja vs Parannettu Tekoaly'
    }
    
    return render_template('peli.html', 
                         pelimuoto=pelimuoto,
                         pelimuoto_nimi=pelimuoto_nimet.get(pelimuoto, ''),
                         historia=historia,
                         peli_data=peli_data,
                         odottaa_pelaaja2=odottaa_pelaaja2,
                         pelaaja1_siirto=pelaaja1_siirto,
                         pelaaja1_nimi=pelaaja1_nimi,
                         pelaaja2_nimi=pelaaja2_nimi)


@app.route('/siirto', methods=['POST'])
def siirto():
    """Kasittelee pelaajan siirron."""
    if 'pelimuoto' not in session:
        return redirect(url_for('index'))
    
    # Tarkista onko peli jo ohi
    if session.get('peli_data', {}).get('peli_ohi', False):
        return redirect(url_for('peli'))
    
    pelimuoto = session['pelimuoto']
    pelaajan_siirto = request.form.get('siirto', '').lower()
    
    # Pelaaja vs Pelaaja -logiikka
    if pelimuoto == 'pelaaja':
        if not session.get('odottaa_pelaaja2_siirtoa', False):
            # Pelaaja 1:n siirto
            session['pelaaja1_siirto'] = pelaajan_siirto
            session['odottaa_pelaaja2_siirtoa'] = True
            session.modified = True
            return redirect(url_for('peli'))
        else:
            # Pelaaja 2:n siirto
            pelaaja2_siirto = pelaajan_siirto
            pelaaja1_siirto = session.get('pelaaja1_siirto')
            
            # Kasittele molemmat siirrot
            peli = KPSWeb(pelimuoto)
            peli.tuomari.ekan_pisteet = session['peli_data']['ekan_pisteet']
            peli.tuomari.tokan_pisteet = session['peli_data']['tokan_pisteet']
            peli.tuomari.tasapelit = session['peli_data']['tasapelit']
            
            # Kirjaa molemmat siirrot
            if pelaaja1_siirto and pelaaja1_siirto in ('k', 'p', 's') and pelaaja2_siirto in ('k', 'p', 's'):
                peli.tuomari.kirjaa_siirto(pelaaja1_siirto, pelaaja2_siirto)
                
                session['peli_data'] = peli.get_tilanne()
                
                siirto_nimet = {'k': 'Kivi', 'p': 'Paperi', 's': 'Sakset'}
                kierros_data = {
                    'pelaaja': siirto_nimet.get(pelaaja1_siirto, pelaaja1_siirto),
                    'vastustaja': siirto_nimet.get(pelaaja2_siirto, pelaaja2_siirto)
                }
                
                historia = session.get('historia', [])
                historia.append(kierros_data)
                session['historia'] = historia
            
            # Nollaa pelaaja 2:n odotus
            session['odottaa_pelaaja2_siirtoa'] = False
            session['pelaaja1_siirto'] = None
            session.modified = True
            return redirect(url_for('peli'))
    
    # Tekoaly-logiikka
    tekoaly_tila = session.get('tekoaly_tila')
    peli = KPSWeb(pelimuoto, tekoaly_tila)
    peli.tuomari.ekan_pisteet = session['peli_data']['ekan_pisteet']
    peli.tuomari.tokan_pisteet = session['peli_data']['tokan_pisteet']
    peli.tuomari.tasapelit = session['peli_data']['tasapelit']
    
    tulos = peli.pelaa_kierros(pelaajan_siirto)
    
    if not tulos['valid']:
        return redirect(url_for('peli'))
    
    session['peli_data'] = peli.get_tilanne()
    session['tekoaly_tila'] = peli.get_tekoaly_tila()
    
    siirto_nimet = {'k': 'Kivi', 'p': 'Paperi', 's': 'Sakset'}
    
    kierros_data = {
        'pelaaja': siirto_nimet.get(tulos['pelaaja'], tulos['pelaaja']),
        'vastustaja': siirto_nimet.get(tulos['vastustaja'], tulos['vastustaja']) if tulos['vastustaja'] else '-'
    }
    
    if 'historia' not in session:
        session['historia'] = []
    
    historia = session['historia']
    historia.append(kierros_data)
    session['historia'] = historia
    
    session.modified = True
    
    return redirect(url_for('peli'))


@app.route('/uusi_peli')
def uusi_peli():
    """Aloittaa uuden pelin."""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
