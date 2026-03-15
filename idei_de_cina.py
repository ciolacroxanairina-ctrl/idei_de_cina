import streamlit as st
import yagmail
import urllib.parse
import random

# --- CONFIGURARE SISTEM ---
EMAIL_SISTEM = "ciolac.roxana.irina@gmail.com"
PAROLA_SISTEM = "lphxidawqbukpmuk"

# --- MESAJE AMUZANTE ---
mesaje_funny = [
    "Decizia grea a fost luată: **{alegere}**! Să înceapă Jocurile Foamei! Fie ca bucătăria să nu fie distrusă! 🔥",
    "Victorie! S-a ales **{alegere}**. Sperăm că bucătarul e binedispus astăzi! 👨‍🍳",
    "Habemus Papam! Adică avem meniu: **{alegere}**. Să vină farfuriile! 🍽️",
    "Zarurile au fost aruncate! Diseară se mănâncă **{alegere}**. Poftă bună, dragilor! 🥂",
    "Alertă de deliciu! **{alegere}** a câștigat bătălia papilelor gustative! 🏆"
]

def trimite_mail(destinatar, subiect, continut):
    try:
        yag = yagmail.SMTP(EMAIL_SISTEM, PAROLA_SISTEM)
        yag.send(to=destinatar, subject=subiect, contents=continut)
        return True
    except:
        return False

# --- LOGICA INTERFATA ---
st.set_page_config(page_title="Dinner Roulette", page_icon="🥘")

# Stilizare culori
st.markdown("""
    <style>
    .stApp { background-color: #fffaf0; }
    h1 { color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

query_params = st.query_params

if "de_la" in query_params:
    # --- VIZUALIZARE RESPONDENT ---
    nume_exp = query_params.get("nume_exp", "Cineva drag")
    gen_exp = query_params.get("gen", "f")
    titlu_gen = "vrea să gătească" if gen_exp == "f" else "vrea să pregătească"
    
    st.title(f"🥘 Ce {titlu_gen} {nume_exp} diseară?")
    optiuni = query_params["opt"].split(",")
    
    alegere = st.radio("Alege varianta care îți face cel mai mult cu ochiul:", optiuni)
    
    if st.button("Confirmă Alegerea 🚀"):
        msg = random.choice(mesaje_funny).format(alegere=alegere)
        if trimite_mail(query_params["de_la"], "Decizia a fost luată! 🍴", msg):
            st.balloons()
            st.success("Alegerea a fost trimisă! Verifică dacă bucătăria e liberă. 😉")
            st.info(msg)
else:
    # --- VIZUALIZARE CREATOR ---
    st.title("📝 Planificator de Cină Magic")
    
    with st.sidebar:
        st.header("Profilul Tău")
        nume_meu = st.text_input("Numele tău *")
        gen = st.radio("Calitatea de:", ["Femeie", "Bărbat"])
        gen_cod = "f" if gen == "Femeie" else "m"
        email_meu = st.text_input("E-mailul tău (unde primești răspunsul) *")
        
    st.subheader("👨‍👩‍ servantul / Respondentul")
    nume_el = st.text_input("Nume respondent")
    email_el = st.text_input("E-mail respondent (opțional pentru trimitere directă)")

    st.subheader("🍴 Ce gătim diseară?")
    
    # Gestionare dinamică a opțiunilor
    if 'num_opt' not in st.session_state:
        st.session_state.num_opt = 3

    optiuni_input = []
    for i in range(st.session_state.num_opt):
        opt = st.text_input(f"Opțiunea {i+1}", key=f"opt_{i}")
        if opt: optiuni_input.append(opt)

    if st.button("➕ Adaugă alt fel de mâncare"):
        st.session_state.num_opt += 1
        st.rerun()

    col1, col2 = st.columns(2)
    
    # Generare Link
    with col1:
        if st.button("🔗 Generează Link"):
            if not email_meu or not nume_meu:
                st.error("Numele și Mail-ul tău sunt obligatorii!")
            else:
                opt_str = ",".join(optiuni_input)
                base_url = "https://idei-de-cina.streamlit.app/"
                params = {"de_la": email_meu, "opt": opt_str, "nume_exp": nume_meu, "gen": gen_cod}
                link_final = f"{base_url}?{urllib.parse.urlencode(params)}"
                st.code(link_final)

    # Trimite Mail
    with col2:
        if st.button("📧 Trimite pe Mail"):
            if not email_el:
                st.warning("⚠️ Pentru a trimite mail este obligatorie completarea casetei pentru mail respondent!")
            elif not email_meu or not nume_meu:
                st.error("Completează datele tale mai întâi!")
            else:
                opt_str = ",".join(optiuni_input)
                base_url = "https://idei-de-cina.streamlit.app/"
                params = {"de_la": email_meu, "opt": opt_str, "nume_exp": nume_meu, "gen": gen_cod}
                link_final = f"{base_url}?{urllib.parse.urlencode(params)}"
                
                subiect = f"Mesaj special de la {nume_meu} ❤️"
                corp = f"Bună {nume_el}! {nume_meu} te întreabă ce mâncați diseară. Alege aici: {link_final}"
                
                if trimite_mail(email_el, subiect, corp):
                    st.success(f"Mail-ul a plecat spre {nume_el}!")
                else:
                    st.error("Eroare la trimiterea mail-ului.")
