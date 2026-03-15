import streamlit as st
import yagmail
import urllib.parse

# --- CONFIGURARE SISTEM ---
# Pune aici parola galbenă de 16 caractere (fără spații)
EMAIL_SISTEM = "ciolac.roxana.irina@gmail.com"
PAROLA_SISTEM = "lphxidawqbukpmuk" 

def trimite_notificare(destinatar, alegere):
    try:
        yag = yagmail.SMTP(EMAIL_SISTEM, PAROLA_SISTEM)
        yag.send(
            to=destinatar,
            subject="Decizie Cină! 🥘",
            contents=f"Veste bună! S-a făcut alegerea: {alegere}. Spor la gătit! ❤️"
        )
        return True
    except Exception as e:
        st.error(f"Eroare tehnică la mail: {e}")
        return False

# --- LOGICA APLICATIEI ---
query_params = st.query_params

if "de_la" in query_params:
    # --- CE VEDE SOȚUL ---
    st.title("Ce mâncăm diseară? 👩‍🍳")
    email_sotie = query_params["de_la"]
    optiuni = query_params["opt"].split(",")
    
    st.write("Alege una dintre variantele de mai jos:")
    alegere = st.radio("Opțiuni:", optiuni)
    
    if st.button("Confirmă alegerea! 🚀"):
        if trimite_notificare(email_sotie, alegere):
            st.balloons()
            st.success("Gata! I-am trimis un mail soției tale.")
else:
    # --- CE VEZI TU ---
    st.title("Generator de Meniu 📝")
    email_tau = st.text_input("E-mailul tău pentru notificări", value="ciolac.roxana.irina@gmail.com")
    
    col1, col2 = st.columns(2)
    with col1:
        opt1 = st.text_input("Varianta 1", "Paste")
        opt2 = st.text_input("Varianta 2", "Pizza")
    with col2:
        opt3 = st.text_input("Varianta 3", "Salată")
        opt4 = st.text_input("Varianta 4", "Comandăm ceva")

    if st.button("Generează link pentru soț"):
        if email_tau:
            toate = [opt1, opt2, opt3, opt4]
            opt_str = ",".join([o for o in toate if o.strip()])
            
            # ATENȚIE: Aici pune link-ul tău de Streamlit după ce e live
            base_url = "https://idei-de-cina.streamlit.app/" 
            
            params = {"de_la": email_tau, "opt": opt_str}
            link_final = f"{base_url}?{urllib.parse.urlencode(params)}"
            
            st.success("Copiază link-ul de mai jos și trimite-l pe WhatsApp:")
            st.code(link_final)
        else:
            st.warning("Te rog pune e-mailul tău mai sus.")
