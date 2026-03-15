import streamlit as st
import yagmail
import urllib.parse
import random

# --- CONFIGURARE SERVER ---
# Acesta rămâne "poștașul" aplicației
EMAIL_SISTEM = "ciolac.roxana.irina@gmail.com"
PAROLA_SISTEM = "lphxidawqbukpmuk"

# TOATE GIF-URILE TALE (48 de variante)
COLECTIE_GIFS = [
    "https://media.giphy.com/media/XIBQ0Bz51uRnlsj77Y/giphy.gif", "https://media.giphy.com/media/LWiwqFwaR2RgzRauBj/giphy.gif",
    "https://media.giphy.com/media/hbJtVo1FCArG2MDBmi/giphy.gif", "https://media.giphy.com/media/ZofRdFOAb22IbXz0ry/giphy.gif",
    "https://media.giphy.com/media/b5Hcaz7EPz26I/giphy.gif", "https://media.giphy.com/media/Jkk64Xj64mcfu/giphy.gif",
    "https://media.giphy.com/media/p0dFF6nzn1DZKKyNdo/giphy.gif", "https://media.giphy.com/media/a0N6ZmPmzGIPm/giphy.gif",
    "https://media.giphy.com/media/l2SqbIFulqPMQq9nq/giphy.gif", "https://media.giphy.com/media/or1QV1lTgkAxO/giphy.gif",
    "https://media.giphy.com/media/WxMBQU7IS82Q0/giphy.gif", "https://media.giphy.com/media/H7xnU8srPdP87PfCHD/giphy.gif",
    "https://media.giphy.com/media/avLdpWkQofnIRpa0pJ/giphy.gif", "https://media.giphy.com/media/w3IlnK3V6CS1q/giphy.gif",
    "https://media.giphy.com/media/1fjEMdnRjxYrLQ4vw0/giphy.gif", "https://media.giphy.com/media/oESgZ6uNs9xgQulYiK/giphy.gif",
    "https://media.giphy.com/media/zRH0N155CVvebVhOhp/giphy.gif", "https://media.giphy.com/media/2ya7xLyEeynlZM4FCw/giphy.gif",
    "https://media.giphy.com/media/w7CP59oLYw6PK/giphy.gif", "https://media.giphy.com/media/SKoWAIC135sSk/giphy.gif",
    "https://media.giphy.com/media/H31VnwaffLwmk/giphy.gif", "https://media.giphy.com/media/MwUPdnmcZOWCA/giphy.gif",
    "https://media.giphy.com/media/3lj7wxDu4hcDC/giphy.gif", "https://media.giphy.com/media/12uXi1GXBibALC/giphy.gif",
    "https://media.giphy.com/media/10ZpyYs0OvVlnO/giphy.gif", "https://media.giphy.com/media/1rOZNBi7qHDbLfpgDl/giphy.gif",
    "https://media.giphy.com/media/13xfs4HHM56n5e/giphy.gif", "https://media.giphy.com/media/42BsuUNl1GrjJNIWvy/giphy.gif",
    "https://media.giphy.com/media/3o7qE9AMeGruS75eSI/giphy.gif", "https://media.giphy.com/media/SY8V1Q35R1NMwx8aNl/giphy.gif",
    "https://media.giphy.com/media/AozJ3gQrzoSEjUXXMp/giphy.gif", "https://media.giphy.com/media/i2elLtqWrT0VtdVXRy/giphy.gif",
    "https://media.giphy.com/media/m530QoD3Sp6TB2PpAS/giphy.gif", "https://media.giphy.com/media/GkRJvt0qJItGeCdIZy/giphy.gif",
    "https://media.giphy.com/media/73trcfdnqJmrftTy7i/giphy.gif", "https://media.giphy.com/media/2FzhmhdGPhoCTMgDKl/giphy.gif",
    "https://media.giphy.com/media/N1TzDcgCw0m2Lors1I/giphy.gif", "https://media.giphy.com/media/sAyMI2dYpbXC6pzKDS/giphy.gif",
    "https://media.giphy.com/media/ri8JcEn1isXyPVbeNb/giphy.gif", "https://media.giphy.com/media/wm3Lc5T5NqJLa/giphy.gif",
    "https://media.giphy.com/media/3QyPiMPSTfRG8/giphy.gif", "https://media.giphy.com/media/h8VGOATq81wTS/giphy.gif",
    "https://media.giphy.com/media/2ey7YsQRFczEQ/giphy.gif", "https://media.giphy.com/media/cEsoz6GAoTubm/giphy.gif",
    "https://media.giphy.com/media/r8rKNIA7uQi9G/giphy.gif", "https://media.giphy.com/media/orVCf20E9iXpZIVHya/giphy.gif",
    "https://media.giphy.com/media/ZAQLWzxfGjI0T5O9lG/giphy.gif", "https://media.giphy.com/media/1lxNFxl0TrlEoN7v1K/giphy.gif",
    "https://media.giphy.com/media/vXIjTvGT6xKT46RPjw/giphy.gif"
]

GIF_SUCCES = "https://media.giphy.com/media/artj92VpL0XG8/giphy.gif"

def trimite_mail(destinatar, subiect, continut):
    try:
        yag = yagmail.SMTP(EMAIL_SISTEM, PAROLA_SISTEM)
        yag.send(to=destinatar, subject=subiect, contents=continut)
        return True
    except: return False

# --- UI ---
st.set_page_config(page_title="Dinner Roulette", page_icon="🍕")

p = st.query_params

if "de_la" in p:
    # --- VIZUALIZARE RESPONDENT ---
    nume_exp = p.get("nume_exp", "Cineva drag")
    st.image(random.choice(COLECTIE_GIFS), use_container_width=True)
    st.title(f"🥘 {nume_exp} vrea să pregătească cina!")
    
    optiuni = p["opt"].split(",")
    alegere = st.radio("Ce îți dorește stomacul azi?", optiuni)
    comentariu = st.text_input("Un mesaj extra? (ex: 'Vreau și ceva dulce!')")
    
    if st.button("Confirmă Alegerea 🚀"):
        mesaje = [
            f"Decizia a fost luată: **{alegere}**! Să înceapă Jocurile Foamei! 🔥",
            f"Victorie! S-a ales **{alegere}**. Sperăm că bucătarul e binedispus! 👨‍🍳",
            f"Habemus Papam! Avem meniu: **{alegere}**. Să vină farfuriile! 🍽️"
        ]
        msg = random.choice(mesaje)
        if comentariu: msg += f"<br><br><b>Mesaj extra de la el:</b> {comentariu}"
        
        if trimite_mail(p["de_la"], "Avem un câștigător! 🏆", msg):
            st.balloons()
            st.success("Alegerea a plecat spre ea!")
            st.image(GIF_SUCCES)
else:
    # --- VIZUALIZARE CREATOR ---
    st.title("📝 Planificator de Cină Universal")
    st.write("Creează-ți linkul personalizat și lasă-l pe el să aleagă!")
    
    with st.expander("👤 Datele tale", expanded=True):
        nume_meu = st.text_input("Numele tău *", placeholder="Ex: Irina")
        email_meu = st.text_input("E-mailul tău *", placeholder="Ex: adresa@gmail.com")
        
    with st.expander("👩‍❤️‍👨 Partenerul", expanded=True):
        nume_el = st.text_input("Nume respondent", placeholder="Ex: Florin")
        email_el = st.text_input("E-mail respondent (opțional)")

    st.subheader("🍴 Opțiuni Meniu")
    if 'n_opt' not in st.session_state: st.session_state.n_opt = 2

    optiuni_list = []
    for i in range(st.session_state.n_opt):
        val = st.text_input(f"Opțiunea {i+1}", key=f"o_{i}")
        if val: optiuni_list.append(val)

    if st.button("➕ Adaugă alt fel de mâncare"):
        st.session_state.n_opt += 1
        st.rerun()

    st.divider()
    
    # Construire Link
    opt_str = ",".join(optiuni_list)
    base_url = "https://idei-de-cina.streamlit.app/" 
    link_params = {"de_la": email_meu, "opt": opt_str, "nume_exp": nume_meu}
    link_final = f"{base_url}?{urllib.parse.urlencode(link_params)}"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 Generează Link"):
            if email_meu and nume_meu and optiuni_list: st.code(link_final)
            else: st.error("Completează numele, mailul și opțiunile!")

    with col2:
        if st.button("📧 Trimite pe Mail"):
            if not email_el: st.warning("⚠️ Introdu e-mailul respondentului!")
            else:
                sub = f"Mesaj special de la {nume_meu} ❤️"
                corp = f"Bună {nume_el}! {nume_meu} te întreabă ce mâncați diseară. Alege aici: {link_final}"
                if trimite_mail(email_el, sub, corp): st.success("Mail-ul a plecat!")
