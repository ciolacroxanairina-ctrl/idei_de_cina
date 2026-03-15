import streamlit as st
import yagmail
import urllib.parse
import random
import requests

# --- CONFIGURARE SERVER ---
EMAIL_SISTEM = "ciolac.roxana.irina@gmail.com"
PAROLA_SISTEM = "lphxidawqbukpmuk"

# Funcție stabilă pentru GIF-uri
def get_funny_cooking_gif():
    # Cuvintele tale cheie preferate
    keywords = ["cooking cartoon", "cooking anime", "cooking food", "funny chef", "ratatouille cooking"]
    tag = random.choice(keywords)
    # API Key public GIPHY
    url = f"https://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={urllib.parse.quote(tag)}&rating=g"
    try:
        response = requests.get(url).json()
        # Luăm ID-ul GIF-ului pentru a construi un link stabil de afișare
        gif_id = response['data']['id']
        return f"https://media.giphy.com/media/{gif_id}/giphy.gif"
    except:
        # Imagine de rezervă sigură dacă pică internetul/API-ul
        return "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/demgpwJ6ZeDSM/giphy.gif"

def trimite_mail(destinatar, subiect, continut):
    try:
        yag = yagmail.SMTP(EMAIL_SISTEM, PAROLA_SISTEM)
        yag.send(to=destinatar, subject=subiect, contents=continut)
        return True
    except: return False

# --- UI ---
st.set_page_config(page_title="Dinner Picker", page_icon="🍕")

params = st.query_params

if "de_la" in params:
    # --- VIZUALIZARE RESPONDENT (Florin/Partener) ---
    nume_exp = params.get("nume_exp", "Cineva drag")
    
    # Afișăm GIF-ul
    st.image(get_funny_cooking_gif(), use_container_width=True)
    
    st.title(f"🥘 {nume_exp} te întreabă: Ce mâncăm?")
    
    optiuni = params["opt"].split(",")
    alegere = st.radio("Alege cu grijă:", optiuni)
    comentariu = st.text_input("Vrei să adaugi un mesaj/dorință? (ex: 'Vreau și desert!')")
    
    if st.button("Confirmă Alegerea 🚀"):
        mesaje_funny = [
            "Decizia grea a fost luată: **{alegere}**! Să înceapă Jocurile Foamei! 🔥",
            "Victorie! S-a ales **{alegere}**. Sperăm că bucătarul e binedispus! 👨‍🍳",
            "Habemus Papam! Avem meniu: **{alegere}**. Să vină farfuriile! 🍽️"
        ]
        msg_text = random.choice(mesaje_funny).format(alegere=alegere)
        if comentariu: 
            msg_text += f"<br><br><b>Mesaj de la respondent:</b> {comentariu}"
        
        if trimite_mail(params["de_la"], "Avem o decizie! 🏆", msg_text):
            st.balloons()
            st.success("Notificarea a plecat!")
            # GIF de succes la final
            st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/artj92VpL0XG8/giphy.gif")
else:
    # --- VIZUALIZARE CREATOR (Irina/Oricine) ---
    st.title("📝 Planificator de Cină Universal")
    
    with st.expander("👤 Datele tale", expanded=True):
        nume_meu = st.text_input("Numele tău *", placeholder="Ex: Irina")
        email_meu = st.text_input("E-mailul tău *", placeholder="Ex: adresa@gmail.com")
        
    with st.expander("👨‍👩‍ Partenerul", expanded=True):
        nume_el = st.text_input("Numele respondentului", placeholder="Ex: Florin")
        email_el = st.text_input("E-mail respondent (opțional)")

    st.subheader("🍴 Ce propuneri ai?")
    if 'n_opt' not in st.session_state: st.session_state.n_opt = 2

    optiuni_list = []
    for i in range(st.session_state.n_opt):
        val = st.text_input(f"Opțiunea {i+1}", key=f"o_{i}")
        if val: optiuni_list.append(val)

    if st.button("➕ Adaugă alt fel de mâncare"):
        st.session_state.n_opt += 1
        st.rerun()

    st.divider()
    
    # Construire Link - ATENȚIE: Verifică dacă adresa de mai jos e linkul tău!
    opt_str = ",".join(optiuni_list)
    base_url = "https://idei-de-cina.streamlit.app/" 
    link_params = {"de_la": email_meu, "opt": opt_str, "nume_exp": nume_meu}
    link_final = f"{base_url}?{urllib.parse.urlencode(link_params)}"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 Generează Link"):
            if email_meu and nume_meu and optiuni_list:
                st.code(link_final)
            else: st.error("Completează toate câmpurile obligatorii!")

    with col2:
        if st.button("📧 Trimite pe Mail"):
            if not email_el:
                st.warning("⚠️ Introdu e-mailul respondentului!")
            else:
                sub = f"Mesaj special de la {nume_meu} ❤️"
                corp = f"Bună {nume_el}! {nume_meu} te întreabă ce mâncați diseară. Alege aici: {link_final}"
                if trimite_mail(email_el, sub, corp):
                    st.success("Mail-ul a plecat!")
