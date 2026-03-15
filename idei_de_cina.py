import streamlit as st
import yagmail
import urllib.parse
import random

# --- CONFIGURARE SERVER ---
EMAIL_SISTEM = "ciolac.roxana.irina@gmail.com"
PAROLA_SISTEM = "lphxidawqbukpmuk"

# COLECTIE GIFS (Păstrată pentru prima pagină)
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

def trimite_mail(destinatar, subiect, continut):
    try:
        yag = yagmail.SMTP(EMAIL_SISTEM, PAROLA_SISTEM)
        yag.send(to=destinatar, subject=subiect, contents=continut)
        return True
    except: return False

st.set_page_config(page_title="Dinner Roulette", page_icon="🍕")
p = st.query_params

if "de_la" in p:
    # --- VIZUALIZARE RESPONDENT ---
    nume_exp = p.get("nume_exp", "Cineva drag")
    mesaj_invitatie = p.get("msg", "") # Mesajul suplimentar din link

    if "trimis" not in st.session_state:
        st.image(random.choice(COLECTIE_GIFS), use_container_width=True)
        st.title(f"🥘 {nume_exp} vrea să pregătească cina!")
        
        # Afișăm mesajul de la creator dacă există
        if mesaj_invitatie:
            st.chat_message("assistant").write(f"**Mesaj de la {nume_exp}:** {mesaj_invitatie}")

        optiuni = p["opt"].split(",")
        alegere = st.radio("Ce îți dorește stomacul azi 😋?", optiuni)
        comentariu = st.text_input("Un mesaj extra pentru {nume_exp}? (ex: 'Vreau și ceva dulce 🍰!')")
        
        if st.button("Confirmă Alegerea 🚀"):
            mesaje_funny = [
                f"Decizia grea a fost luată: **{alegere}**! Să înceapă Jocurile Foamei! 🔥",
                f"Victorie! S-a ales **{alegere}**. Sperăm că bucătarul e binedispus! 👨‍🍳",
                f"Habemus Papam! Avem meniu: **{alegere}**. Să vină farfuriile! 🍽️"
            ]
            msg = random.choice(mesaje_funny)
            if comentariu: msg += f"<br><br><b>Mesaj extra de la el:</b> {comentariu}"
            
            if trimite_mail(p["de_la"], "Avem un câștigător! 🏆", msg):
                st.session_state.trimis = True
                st.session_state.mesaj_final = msg
                st.rerun()
    else:
        st.balloons()
        st.success("✅ Alegerea a plecat spre ea! Poți închide această pagină.")
        st.info(st.session_state.mesaj_final.replace("<br>", "\n"))
        st.markdown("### Poftă bună! ✨")

else:
    # --- VIZUALIZARE CREATOR ---
    st.title("📝 Planificator de Cină Universal")
    
    with st.expander("👤 Datele tale", expanded=True):
        nume_meu = st.text_input("Numele tău *", placeholder="Irina")
        email_meu = st.text_input("E-mailul tău *", placeholder="adresa.ta@gmail.com")
    
    # NOU: Mesajul tău suplimentar
    mesaj_suplimentar = st.text_area("Mesaj pentru partener (opțional)", placeholder="Ex: Alege cu grijă, că mi-e tare foame! ❤️")

    with st.expander("👩‍❤️‍👨 Partenerul", expanded=True):
        nume_el = st.text_input("Nume respondent", placeholder="Florin")
        email_el = st.text_input("E-mail respondent (opțional)")

    st.subheader("🍴 Opțiuni Meniu")
    if 'n_opt' not in st.session_state: st.session_state.n_opt = 2

    optiuni_list = []
    for i in range(st.session_state.n_opt):
        val = st.text_input(f"🥣Opțiunea {i+1}", key=f"o_{i}")
        if val: optiuni_list.append(val)

    if st.button("➕ Mai am o idee!"):
        st.session_state.n_opt += 1
        st.rerun()

    st.divider()
    
    opt_str = ",".join(optiuni_list)
    base_url = "https://idei-de-cina.streamlit.app/" 
    
    # Adăugăm și mesajul tău în parametrii link-ului
    lp = {"de_la": email_meu, "opt": opt_str, "nume_exp": nume_meu, "msg": mesaj_suplimentar}
    link_final = f"{base_url}?{urllib.parse.urlencode(lp)}"

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
                # Adăugăm mesajul tău și în mail-ul direct dacă alegi varianta asta
                corp = f"Bună {nume_el}! {nume_meu} te întreabă ce mâncați diseară.\n\nMesaj: {mesaj_suplimentar}\n\nAlege aici: {link_final}"
                if trimite_mail(email_el, sub, corp): st.success("Mail-ul a plecat!")
