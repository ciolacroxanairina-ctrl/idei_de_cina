import streamlit as st
import yagmail
import urllib.parse
import random

# --- CONFIGURARE SERVER (Poștașul aplicației) ---
EMAIL_SISTEM = "ciolac.roxana.irina@gmail.com"
PAROLA_SISTEM = "lphxidawqbukpmuk"

# --- REZURSE VIZUALE ---
gif_cooking = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/demgpwJ6ZeDSM/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/12uXi1GXBibzp6/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKVUn7iM8FMEU24/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l46C6z7vYdvZ7GXT2/giphy.gif"
]

mesaje_funny = [
    "Decizia grea a fost luată: **{alegere}**! Să înceapă Jocurile Foamei! 🔥",
    "Victorie! S-a ales **{alegere}**. Sperăm că bucătarul e binedispus! 👨‍🍳",
    "Habemus Papam! Adică avem meniu: **{alegere}**. Să vină farfuriile! 🍽️",
    "Zarurile au fost aruncate! Diseară avem **{alegere}**. Poftă bună! 🥂",
    "Alertă de deliciu! **{alegere}** a câștigat bătălia papilelor gustative! 🏆"
]

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
    # --- INTERFAȚĂ RESPONDENT (Partenerul) ---
    nume_exp = params.get("nume_exp", "Cineva drag")
    st.image(random.choice(gif_cooking))
    st.title(f"🥘 {nume_exp} te întreabă: Ce mâncăm?")
    
    optiuni = params["opt"].split(",")
    alegere = st.radio("Alege cu grijă:", optiuni)
    comentariu = st.text_input("Vrei să adaugi un mesaj/dorință? (ex: 'Vreau și desert!')")
    
    if st.button("Confirmă Alegerea 🚀"):
        msg_text = random.choice(mesaje_funny).format(alegere=alegere)
        if comentariu:
            msg_text += f"\n\nPS: {comentariu}"
        
        # Trimitem mail către cel care a generat link-ul
        if trimite_mail(params["de_la"], "Avem un câștigător! 🏆", msg_text):
            st.balloons()
            st.success("Notificarea a plecat!")
            st.info(msg_text)
            st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/artj92VpL0XG8/giphy.gif")
else:
    # --- INTERFAȚĂ CREATOR (Oricine vrea să gătească) ---
    st.title("📝 Planificator de Cină Universal")
    st.write("Creează-ți propriul meniu și lasă partenerul să decidă!")
    
    with st.expander("👤 Datele tale", expanded=True):
        nume_meu = st.text_input("Numele tău *", placeholder="Ex: Irina")
        email_meu = st.text_input("E-mailul tău *", placeholder="Ex: adresa@gmail.com")
        
    with st.expander("👨‍👩‍ Partenerul", expanded=True):
        nume_el = st.text_input("Numele partenerului", placeholder="Ex: Florin")
        email_el = st.text_input("E-mail partener (opțional pentru trimitere directă)")

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
    base_url = "https://idei-de-cina.streamlit.app/" # Asigură-te că e linkul tău corect!
    link_params = {"de_la": email_meu, "opt": opt_str, "nume_exp": nume_meu}
    link_final = f"{base_url}?{urllib.parse.urlencode(link_params)}"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 Generează Link"):
            if email_meu and nume_meu and optiuni_list:
                st.code(link_final)
            else: st.error("Completează câmpurile marcate cu *!")

    with col2:
        if st.button("📧 Trimite pe Mail"):
            if not email_el:
                st.warning("⚠️ Introdu e-mailul respondentului!")
            elif not email_meu:
                st.error("Introdu e-mailul tău mai întâi!")
            else:
                sub = f"Mesaj special de la {nume_meu} ❤️"
                corp = f"Bună {nume_el}! {nume_meu} te întreabă ce mâncați diseară. Alege aici: {link_final}"
                if trimite_mail(email_el, sub, corp):
                    st.success("Mail-ul a plecat! 🕊️")
