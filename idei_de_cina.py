import streamlit as st
import yagmail
import urllib.parse
import random
from supabase import create_client, Client

# --- CONFIGURARE SUPABASE ---
# Înlocuiește linia de mai jos cu URL-ul din tab-ul "General"
SUPABASE_URL = "https://okhjyjqfhbxrrzrtyjmd.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9raGp5anFmaGJ4cnJ6cnR5am1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2ODMwODMsImV4cCI6MjA4OTI1OTA4M30.BksYbesw-OGJGB50KHMZfVjnrQfg0mZ-2vX6kpXkTHQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIGURARE MAIL ---
EMAIL_SISTEM = "ciolac.roxana.irina@gmail.com"
PAROLA_SISTEM = "lphxidawqbukpmuk"

# GIF-urile tale preferate pentru început
COLECTIE_GIFS = [
    "https://media.giphy.com/media/XIBQ0Bz51uRnlsj77Y/giphy.gif",
    "https://media.giphy.com/media/LWiwqFwaR2RgzRauBj/giphy.gif",
    "https://media.giphy.com/media/hbJtVo1FCArG2MDBmi/giphy.gif"
]

def genereaza_sfat_nutritional(mancare):
    m = mancare.lower()
    if "pui" in m: return "Puiul e bogat în proteine! Încearcă să-l faci la grătar sau cuptior pentru o variantă mai light."
    if "paste" in m or "carbonara" in m: return "Pastele dau energie! Poți adăuga o salată mică lângă pentru fibre."
    if "cartofi" in m: return "Cartofii sunt sățioși. Dacă îi faci pai, încearcă să folosești o friteuză cu aer cald (AirFryer)."
    return "O alegere gustoasă! Nu uita să te hidratezi bine după masă. ❤️"

def trimite_mail(destinatar, subiect, continut):
    try:
        yag = yagmail.SMTP(EMAIL_SISTEM, PAROLA_SISTEM)
        yag.send(to=destinatar, subject=subiect, contents=continut)
        return True
    except: return False

# --- INTERFAȚA ---
st.set_page_config(page_title="Family Dinner", page_icon="👨‍👩‍👧‍👦")

p = st.query_params
cod_familie = "FamiliaCiolac" # Codul vostru fix

if "de_la" in p:
    # --- VIZUALIZARE RESPONDENT (Florin) ---
    if "trimis" not in st.session_state:
        st.image(random.choice(COLECTIE_GIFS), use_container_width=True)
        st.title(f"🥘 {p.get('nume_exp', 'Irina')} vrea să gătească!")
        
        optiuni = p["opt"].split(",")
        alegere = st.radio("Ce alegem pentru diseară?", optiuni)
        
        if st.button("Confirmă Alegerea 🚀"):
            sfat = genereaza_sfat_nutritional(alegere)
            # Salvare în Supabase
            try:
                supabase.table("cina_istoric").insert({
                    "familie_id": cod_familie,
                    "fel_mancare": alegere,
                    "ales_de": "Florin",
                    "nutritie_sfat": sfat
                }).execute()
            except: pass # Mergem mai departe chiar dacă baza de date are o eroare momentană

            # Trimite mail
            msg = f"Decizia a fost luată: **{alegere}**!<br>💡 <b>Sfat:</b> {sfat}"
            if trimite_mail(p["de_la"], "Avem meniul! 🍴", msg):
                st.session_state.trimis = True
                st.rerun()
    else:
        st.balloons()
        st.success("✅ Alegerea a plecat spre Irina! Poftă bună!")
else:
    # --- VIZUALIZARE CREATOR (Irina) ---
    st.title("👨‍👩‍👧‍👦 Family Dinner - Propune Cina")
    
    with st.sidebar:
        st.header("📜 Istoric Mese")
        try:
            res = supabase.table("cina_istoric").select("*").eq("familie_id", cod_familie).order("data", desc=True).limit(5).execute()
            for row in res.data:
                st.write(f"🍴 {row['data']}: {row['fel_mancare']}")
        except: st.write("Încă nu avem istoric salvat.")

    nume_meu = st.text_input("Numele tău", "Irina")
    email_meu = st.text_input("E-mailul tău", "adresa.ta@gmail.com")
    
    if 'n_opt' not in st.session_state: st.session_state.n_opt = 2
    
    opt_list = []
    for i in range(st.session_state.n_opt):
        o = st.text_input(f"Opțiunea {i+1}", key=f"o_{i}")
        if o: opt_list.append(o)
    
    if st.button("➕ Altă idee"):
        st.session_state.n_opt += 1
        st.rerun()

    if st.button("🔗 Generează Link"):
        p_link = {"de_la": email_meu, "opt": ",".join(opt_list), "nume_exp": nume_meu}
        link = f"https://idei-de-cina.streamlit.app/?{urllib.parse.urlencode(p_link)}"
        st.code(link)
