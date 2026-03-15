import streamlit as st
import yagmail
import urllib.parse

# --- CONFIGURARE SERVER EMAIL (Sistemul aplicației) ---
# Aici trebuie să rămână e-mailul tău DOAR ca "expeditor" (serverul care trimite)
EMAIL_SISTEM = "ciolac.roxana.irina@gmail.com"
PAROLA_SISTEM = "parola_ta_de_16_caractere"  # Parola de aplicație Google


def trimite_notificare(destinatar_notificare, alegere, nume_sot):
    try:
        yag = yagmail.SMTP(EMAIL_SISTEM, PAROLA_SISTEM)
        subiect = f"Decizie luată! {alegere} 🥘"
        mesaj = f"Bună! Soțul tău ({nume_sot}) a ales pentru diseară: {alegere}. Poftă bună!"

        yag.send(to=destinatar_notificare, subject=subiect, contents=mesaj)
        return True
    except Exception as e:
        return False


# --- LOGICA INTERFEȚEI ---
query_params = st.query_params

# Verificăm dacă cineva a intrat pe un link de respondent
if "de_la" in query_params:
    st.title("Alege pentru soția ta! ❤️")

    email_sotie = query_params["de_la"]
    optiuni = query_params["opt"].split(",")
    nume_sot = query_params.get("nume", "Soțul tău")

    st.write(f"Salut! Soția ta ți-a trimis aceste variante. Ce alegi?")
    alegere = st.radio("Meniul de azi:", optiuni)

    if st.button("Trimite alegerea! 🚀"):
        with st.spinner("Se trimite notificarea..."):
            if trimite_notificare(email_sotie, alegere, nume_sot):
                st.balloons()
                st.success("Gata! Ea a primit un e-mail cu alegerea ta.")
            else:
                st.error("A apărut o eroare la trimiterea e-mailului.")

else:
    # INTERFAȚA PENTRU ORICINE VREA SĂ GENEREZE UN LINK
    st.title("Planificator de Cină Universal 🍕")
    st.write("Completează datele de mai jos pentru a genera link-ul tău personalizat.")

    with st.expander("1. Datele tale (Cea care gătește/comandă)", expanded=True):
        email_tau = st.text_input("E-mailul tău (unde primești răspunsul)")
        nume_partener = st.text_input("Numele partenerului (opțional)")

    with st.expander("2. Opțiunile de cină", expanded=True):
        opt1 = st.text_input("Varianta A", "Sushi")
        opt2 = st.text_input("Varianta B", "Paste")
        opt3 = st.text_input("Varianta C", "Pizza")

    if st.button("Generează link-ul pentru el"):
        if not email_tau:
            st.warning("Te rugăm să introduci adresa ta de e-mail!")
        else:
            # Construim lista de opțiuni
            lista = [opt1, opt2, opt3]
            opt_str = ",".join([o for o in lista if o.strip()])

            # Link-ul tău public (după ce îl urci pe Streamlit Cloud)
            base_url = "https://cina-noastra.streamlit.app/"

            # Parametrii care "cară" informația în link
            params = {
                "de_la": email_tau,
                "opt": opt_str,
                "nume": nume_partener
            }
            link_final = f"{base_url}?{urllib.parse.urlencode(params)}"

            st.success("Link-ul a fost generat! Copiază-l și trimite-l pe WhatsApp:")
            st.code(link_final)