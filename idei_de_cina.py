import streamlit as st
import yagmail
import urllib.parse
import random

# --- CONFIGURARE SISTEM ---
EMAIL_SISTEM = "ciolac.roxana.irina@gmail.com"
PAROLA_SISTEM = "lphxidawqbukpmuk"

# --- REZURSE FUNNY ---
gif_gatit_funny = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/demgpwJ6ZeDSM/giphy.gif", # Ratatouille
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/12uXi1GXBibzp6/giphy.gif", # Anime cooking
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKVUn7iM8FMEU24/giphy.gif", # Exasperated
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l46C6z7vYdvZ7GXT2/giphy.gif"  # Happy dance
]

mesaje_funny = [
    "Decizia grea a fost luată: **{alegere}**! Să înceapă Jocurile Foamei! 🔥",
    "Victorie! S-a ales **{alegere}**. Sperăm că bucătarul e binedispus! 👨‍🍳",
    "Habemus Papam! Adică avem meniu: **{alegere}**. Să vină farfuriile! 🍽️",
    "Zarurile au fost aruncate! Diseară avem **{alegere}**. Poftă bună! 🥂"
]

def trimite_mail(destinatar, subiect, continut):
    try:
        yag = yagmail.SMTP(EMAIL_SISTEM, PAROLA_SISTEM)
        yag.send(to=destinatar, subject=subiect, contents=continut)
        return True
    except: return False

# --- UI SETTINGS ---
st.set_page_config(page_title="Dinner Roulette", page_icon="🍕")

query_params = st.query_params

if "de_la" in query_params:
    # --- VIZUALIZARE RESPONDENT ---
    nume_exp = query_params.get("nume_exp", "Cineva drag")
    
    st.image(random.choice(gif_gatit_funny))
    st.title(f"🥘 {nume_exp} vrea să pregătească cina!")
    
    optiuni = query_params["opt"].split(",")
    alegere = st.radio("Ce îți dorește inimioara (și stomacul)?", optiuni)
    
    if st.button("Confirmă și surprinde-o! 🚀"):
        # Generăm un GIF random cu mâncare pentru mail
        gif_food = f"https://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&q={urllib.parse.quote(alegere)}&limit=1"
        # Trimitere mail
        msg_text = random.choice(mesaje_funny).format(alegere=alegere)
        mail_html = f"<h3>{msg_text}</h3><br><img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0MYyDa8S9ghzJra8/giphy.gif' width='300'>"
        
        if trimite_mail(query_params["de_la"], "Avem un câștigător! 🏆", [msg_text, mail_html]):
            st.balloons()
            st.success("Notificarea a plecat! Pregătește masa! 🥂")
            st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5bmZ6eGZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/artj92VpL0XG8/giphy.gif")
else:
    # --- VIZUALIZARE CREATOR ---
    st.title("📝 Planificator de Cină Magic")
    
    with st.sidebar:
        st.header("Profilul Tău")
        nume_meu = st.text_input("Numele tău *", "Irina")
        email_meu = st.text_input("E-mailul tău *", "ciolac.roxana.irina@gmail.com")
        
    st.subheader("👨‍👩‍ Respondent")
    nume_el = st.text_input("Nume respondent", "Florin")
    email_el = st.text_input("E-mail respondent (opțional)")

    st.subheader("🍴 Opțiuni de Meniu")
    
    if 'num_opt' not in st.session_state:
        st.session_state.num_opt = 3

    optiuni_list = []
    for i in range(st.session_state.num_opt):
        opt = st.text_input(f"Opțiunea {i+1}", key=f"opt_{i}")
        if opt: optiuni_list.append(opt)

    if st.button("➕ Mai am o idee!"):
        st.session_state.num_opt += 1
        st.rerun()

    st.divider()
    col1, col2 = st.columns(2)
    
    opt_str = ",".join(optiuni_list)
    base_url = "https://idei-de-cina.streamlit.app/" # Schimbă cu linkul tău real!
    params = {"de_la": email_meu, "opt": opt_str, "nume_exp": nume_meu}
    link_final = f"{base_url}?{urllib.parse.urlencode(params)}"

    with col1:
        if st.button("🔗 Generează Link"):
            if email_meu and nume_meu:
                st.code(link_final)
            else: st.error("Completează numele și mailul!")

    with col2:
        if st.button("📧 Trimite pe Mail"):
            if not email_el:
                st.warning("⚠️ Completează mailul respondentului!")
            else:
                sub = f"Mesaj special de la {nume_meu} ❤️"
                corp = f"Bună {nume_el}! Intră aici să alegi cina: {link_final}"
                if trimite_mail(email_el, sub, corp):
                    st.success("Zburat-a mailul! 🕊️")
