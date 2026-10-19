"""
Controle 2: rooktest in een echte (onzichtbare) Chromium-browser, met een NAGEBOOTSTE Firebase.
Er wordt niets naar het echte Firebase-project geschreven of daaruit gelezen.

Gebruik (vanuit de projectmap, met de venv geactiveerd of via .venv\\Scripts\\python):
    python tests/smoke_test.py
Verwacht: alle regels eindigen op OK en op het einde staat "ALLES OK (N controles)". Anders: exitcode 1.
"""
import functools
import http.server
import json
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

# projectmap = één niveau boven de map tests (draagbaar: geen vaste paden)
PROJECT = Path(__file__).resolve().parent.parent
MOCK_JS = (Path(__file__).resolve().parent / "mock_firebase.js").read_text(encoding="utf-8")

resultaten = []   # lijst van (omschrijving, geslaagd)


def controle(omschrijving, voorwaarde):
    """Noteert één controle en print het resultaat meteen."""
    resultaten.append((omschrijving, bool(voorwaarde)))
    print(("OK    " if voorwaarde else "FOUT  ") + omschrijving)


def start_server():
    """Dient de projectmap op een vrije poort van localhost (localStorage werkt alleen via http)."""
    class Stil(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args, **kwargs):   # geen logregels in de uitvoer
            pass
    handler = functools.partial(Stil, directory=str(PROJECT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1]


def nieuwe_pagina(browser, poort, query="", mock_data=None, breedte=390, hoogte=800):
    """Opent index.html met de nagebootste Firebase. Geeft (pagina, lijst met JS-fouten) terug."""
    pagina = browser.new_page(viewport={"width": breedte, "height": hoogte})
    fouten = []
    pagina.on("pageerror", lambda e: fouten.append(str(e)))

    def route(r):
        url = r.request.url
        if "gstatic.com/firebasejs" in url:                       # Firebase-SDK vervangen door de mock
            body = MOCK_JS if "firebase-app-compat" in url else ""
            r.fulfill(body=body, content_type="application/javascript")
        elif url.startswith("http://127.0.0.1"):
            r.continue_()
        else:
            r.abort()                                            # geen verkeer naar buiten (lettertypes enz.)
    pagina.route("**/*", route)
    # testgegevens vóór het laden van de pagina klaarzetten
    pagina.add_init_script("window.__mockData = " + json.dumps(mock_data or {}) + ";")
    pagina.goto(f"http://127.0.0.1:{poort}/index.html{query}")
    pagina.wait_for_timeout(500)
    return pagina, fouten


def main():
    server, poort = start_server()
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # ---- A. GSM-weergave, toogscherm UIT (standaard) ----
        pagina, fouten = nieuwe_pagina(browser, poort)
        controle("gsm: pagina laadt zonder JavaScript-fouten", not fouten)
        if fouten:
            print("      " + " | ".join(fouten))
        controle("gsm: er staan tegels op de pagina", pagina.locator(".tile").count() > 20)
        hoogte = pagina.evaluate("document.querySelector('.tile').offsetHeight")
        controle(f"gsm: tegel is laag genoeg (<= 60 px, nu {hoogte} px)", hoogte <= 60)
        controle("gsm: knop 'Stuur naar toog' is verborgen als het toogscherm uit staat",
                 not pagina.is_visible("#sendToog"))
        controle("gsm: instructiezin 'Tik op een tegel' is weg",
                 "Tik op een tegel" not in pagina.inner_text("body"))
        tekst_alles = pagina.inner_text("body")
        controle("gsm: geen dagtotaal en geen 'TOTAAL OPEN'",
                 "Vandaag afgerekend" not in tekst_alles and "TOTAAL OPEN" not in tekst_alles)
        onder = pagina.evaluate("""() => {
            const b = document.getElementById('admOpen').getBoundingClientRect().top;
            const t = [...document.querySelectorAll('.tile')].pop().getBoundingClientRect().top;
            return b > t;}""")
        controle("gsm: 'Beheer kaart' staat onder de laatste tegel", onder)
        pagina.close()

        # ---- B. GSM-weergave, toogscherm AAN: bestelling doorsturen ----
        pagina, fouten = nieuwe_pagina(browser, poort, mock_data={"cafe/instellingen/toogscherm": True})
        pagina.evaluate("""() => { order = ['Seef','Cola']; price['Seef'] = 380; price['Cola'] = 250;
                                   render(); document.getElementById('sheet').classList.add('open'); }""")
        controle("gsm: knop 'Stuur naar toog' is zichtbaar als het toogscherm aan staat",
                 pagina.is_visible("#sendToog"))
        pagina.fill("#custName", "Jan")
        pagina.click("#sendToog")
        controle("gsm: eerste keer wordt de naam van de medewerker gevraagd",
                 pagina.evaluate("document.getElementById('naamSheet').classList.contains('open')"))
        pagina.fill("#naamInput", "Sara")
        pagina.click("#naamOk")
        pagina.wait_for_timeout(300)
        geschreven = pagina.evaluate("window.__mockSchrijf")
        bestellingen = [w for w in geschreven if w[0] == "push" and w[1] == "cafe/bestellingen"]
        controle("gsm: bestelling is naar cafe/bestellingen geschreven", len(bestellingen) == 1)
        if bestellingen:
            b = bestellingen[0][2]
            controle("gsm: bestelling bevat medewerker, klant, regels en status 'open'",
                     b.get("door") == "Sara" and b.get("klant") == "Jan"
                     and [i[0] for i in b.get("items", [])] == ["Seef", "Cola"] and b.get("status") == "open")
        controle("gsm: bestelling staat ook op de klantrekening (transactie op cafe/rekeningen)",
                 any(w[0] == "transaction" and w[1].startswith("cafe/rekeningen") for w in geschreven))
        controle("gsm: geen JavaScript-fouten tijdens het doorsturen", not fouten)
        pagina.close()

        # ---- C. TABLET-weergave (?toog) ----
        nu = 1_700_000_000_000   # vaste 'nu' voor de testdata; hieronder omgerekend naar de echte klok
        data = {"cafe/instellingen/toogscherm": True, "cafe/bestellingen": {
            "oud":   {"door": "Sara", "klant": "Jan", "items": [["Seef", 380], ["Seef", 380], ["Cola", 250]],
                      "ts": nu - 20 * 60000, "status": "open"},
            "nieuw": {"door": "Tom", "klant": "Els", "items": [["Cola", 250]],
                      "ts": nu - 2 * 60000, "status": "open"},
            "klaar1": {"door": "Tom", "klant": "Piet", "items": [["Seef", 380]],
                       "ts": nu - 60 * 60000, "status": "geleverd", "geleverdTs": nu - 50 * 60000},
            "klaar2": {"door": "Sara", "klant": "An", "items": [["Cola", 250]],
                       "ts": nu - 40 * 60000, "status": "geleverd", "geleverdTs": nu - 10 * 60000},
        }}
        pagina, fouten = nieuwe_pagina(browser, poort, query="?toog", mock_data=data, breedte=1024, hoogte=700)
        # de pagina gebruikt de echte klok: tijden in de testdata vervangen door "nu"-relatieve waarden
        pagina.evaluate("""() => { const n = Date.now(); const verschil = n - 1700000000000;
            Object.values(bestellingen).forEach(b => { b.ts += verschil; if (b.geleverdTs) b.geleverdTs += verschil; });
            renderToog(); }""")
        kaarten = pagina.evaluate("""() => [...document.querySelectorAll('#toogRij .card')]
            .map(c => ({klant: c.querySelector('.klant').textContent, grijs: c.classList.contains('done'),
                        links: Math.round(c.getBoundingClientRect().left)}))""")
        volgorde = [k["klant"] for k in kaarten]
        controle(f"tablet: volgorde is oudste open, nieuwere open, dan recentst geleverd, dan ouder geleverd ({volgorde})",
                 volgorde == ["Jan", "Els", "An", "Piet"])
        controle("tablet: geleverde kaarten zijn grijs", [k["grijs"] for k in kaarten] == [False, False, True, True])
        controle("tablet: kaarten staan naast elkaar in één rij (van links naar rechts)",
                 [k["links"] for k in kaarten] == sorted(k["links"] for k in kaarten)
                 and len(set(k["links"] for k in kaarten)) == 4)
        controle("tablet: teller toont '2 open'", pagina.inner_text("#toogTeller").strip() == "2 open")
        pagina.locator("#toogRij .card").first.locator("button.btn").click()
        pagina.wait_for_timeout(200)
        geschreven = pagina.evaluate("window.__mockSchrijf")
        controle("tablet: 'Geleverd' zet status op 'geleverd' met tijdstip",
                 any(w[0] == "update" and w[1] == "cafe/bestellingen/oud" and w[2].get("status") == "geleverd"
                     and w[2].get("geleverdTs") for w in geschreven))
        controle("tablet: geen JavaScript-fouten", not fouten)
        pagina.close()
        browser.close()
    server.shutdown()

    mislukt = [o for o, ok in resultaten if not ok]
    if mislukt:
        print(f"\nMISLUKT: {len(mislukt)} van {len(resultaten)} controles")
        sys.exit(1)
    print(f"\nALLES OK ({len(resultaten)} controles)")


if __name__ == "__main__":
    main()
