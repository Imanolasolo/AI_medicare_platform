import streamlit as st
from modules.authentication.login import login_user
from modules.authentication.manage_users import manage_users
from modules.consultation.consultation import consultation_page
from modules.hospitalization.hospitalization import hospitalization_page
from modules.operation_rooms.operation_rooms import operating_rooms_page
from modules.emergency.emergency import emergency_page
from modules.ICU.icu import icu_page
from modules.authentication.logout import logout_user  # Asegúrate de tener logout.py
import base64
from dotenv import load_dotenv
import fitz  # PyMuPDF
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI 
from htmlTemplates import css, bot_template, user_template
import os

# Diccionarios de traducción
translations = {
    "es": {
        "ai_medicare_subheader": ":orange[BCS] :blue[AI Medicare], tu sistema de gestión hospitalaria",
        "ai_medicare_desc": "Gestiona tu institución de salud con nuestra plataforma personalizable basada en IA",
        "chat_expander": " Chatea con nosotros",
        "chat_desc": "AI Medicare es una plataforma integral para la gestión de instituciones de salud usando tecnología IA.",
        "chat_prompt": "<h5><br>Pregunta lo que quieras sobre AI Medicare, ¡no te preocupes por el idioma, somos multiidiomáticos!:</h5>",
        "chat_placeholder": "Cuéntanos quién eres y a qué te dedicas para poder ayudarte mejor...",
        "instructions_expander": "Instrucciones para usar la app AI Medicare",
        "instructions": '''
            1. Inserta admin en el área de Usuario con la contraseña :red[Ilargietaeguzki1.].
            2. Cuando estés en la página de inicio de sesión, usa las opciones del selector para gestionar usuarios.
            3. Para cerrar sesión y cambiar de usuario, usa el área del selector en la barra lateral y selecciona :blue[logout], luego pulsa el botón :red[logout] en el área principal.
            ''',
        "translate_spanish": "Español",
        "translate_english": "English",
        "contact_button": "Contactar en caso de problemas",
        "select_module": "Selecciona módulo",
        "hospital_management_system": "Sistema de Gestión Hospitalaria"
    },
    "en": {
        "ai_medicare_subheader": ":orange[BCS] :blue[AI Medicare], your hospital management system",
        "ai_medicare_desc": "Manage your health institution with our fully customizable AI based platform",
        "chat_expander": " Chat with us",
        "chat_desc": "AI Medicare is a comprehensive platform for managing healthcare institutions using AI technology.",
        "chat_prompt": "<h5><br>Ask anything you want about AI Medicare, don’t worry about language we are multiidiomatic!:</h5>",
        "chat_placeholder": "Tell us who you are and what you do and we will help you better...",
        "instructions_expander": "Instructions to use the AI Medicare app",
        "instructions": '''
            1. Insert admin in Username area with :red[Ilargietaeguzki1.] password.
            2. When in login page, use the options in the selector to manage users at your very own
            3. To logout and change users use the selector area in the sidebar and check in :blue[logout], after it push the :red[logout] button in the dashboard area.
            ''',
        "translate_spanish": "Español",
        "translate_english": "English",
        "contact_button": "Contact in case of Troubleshooting",
        "select_module": "Select Module",
        "hospital_management_system": "Hospital Management System"
    }
}

def t(key):
    lang = st.session_state.get("language", "en")
    return translations[lang].get(key, key)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_pdf_text(pdf_list):
    text = ""
    for pdf_path in pdf_list:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    if not text_chunks:
        st.warning("Please upload the textual PDF file - this is PDF files of image")
        return None
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPEN_AI_APIKEY"])
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vector_store):
    llm = ChatOpenAI(openai_api_key=st.secrets["OPEN_AI_APIKEY"])
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userInput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, msg in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)
    st.session_state.chat_history = []  # Reset chat history after each response

def main():
    load_dotenv()
    st.set_page_config(page_title="AI Medicare Platform", page_icon="hospital", layout="wide")
    st.write(css, unsafe_allow_html=True)

    img_base64 = get_base64_of_bin_file('background.jpg')

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url('data:image/jpeg;base64,{img_base64}') no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "pdf_text" not in st.session_state:
        st.session_state.pdf_text = ""

    sample_pdf_path = os.path.join(os.getcwd(), "Base_conocimiento_Medicare.pdf")
    st.session_state.pdf_files = [sample_pdf_path]

    raw_text = get_pdf_text(st.session_state.pdf_files)
    st.session_state.pdf_text = raw_text
    text_chunks = get_text_chunks(raw_text)
    vector_store = get_vector_store(text_chunks)
    st.session_state.conversation = get_conversation_chain(vector_store)

    # Inicializar idioma si no existe
    if "language" not in st.session_state:
        st.session_state.language = "en"

    col1, col2, col3 = st.columns([1, 4, 2])
    with col1:
        st.image('AImedicare_logo.png', width=150)
    with col2:
        st.subheader(t("ai_medicare_subheader"))
        st.write(t("ai_medicare_desc"))
        
        with st.expander(t("chat_expander")):
            st.write(t("chat_desc"))
            st.write(t("chat_prompt"), unsafe_allow_html=True)
            user_question = st.text_input(label="", placeholder=t("chat_placeholder"))
            if user_question:
                handle_userInput(user_question)
    with col3:
        with st.expander(t("instructions_expander")):
            st.markdown(t("instructions"))

        # Botones de idioma debajo del expander
        col_lang1, col_lang2 = st.columns(2)
        with col_lang1:
            if st.button(t("translate_spanish"), key="lang_es"):
                st.session_state.language = "es"
                st.rerun()
        with col_lang2:
            if st.button(t("translate_english"), key="lang_en"):
                st.session_state.language = "en"
                st.rerun()

    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.session_state.page = 'Login'
    elif 'page' not in st.session_state or st.session_state.page not in ["Manage Users", "Consultations", "Hospitalization", "Operating Rooms", "Emergency", "ICU"]:
        st.session_state.page = 'Consultations'

    if st.session_state.page == 'Login':
        login_user()
    else:
        role = st.session_state.role
        st.sidebar.title(t("hospital_management_system"))

        if role == "admin":
            modules = ["Manage Users", "Consultations", "Hospitalization", "Operating Rooms", "Emergency", "ICU"]
        elif role == "staff":
            modules = ["Consultations"]
        elif role == "doctor":
            modules = ["Consultations", "Hospitalization", "Operating Rooms"]
        elif role == "nurse":
            modules = ["ICU", "Operating Rooms"]
        else:
            modules = []

        choice = st.sidebar.selectbox(t("select_module"), modules + ["Logout"], index=modules.index(st.session_state.page) if st.session_state.page in modules else 0)

        if choice == "Logout":
            logout_user()
        elif choice == "Manage Users":
            manage_users()
        elif choice == "Consultations":
            consultation_page()
        elif choice == "Hospitalization":
            hospitalization_page()
        elif choice == "Operating Rooms":
            operating_rooms_page()
        elif choice == "Emergency":
            emergency_page()
        elif choice == "ICU":
            icu_page()

    
    whatsapp_message = "I have issues with AI_Medicare platform, please help me"
    whatsapp_number = "+5930993513082"
    whatsapp_link = f"https://wa.me/{whatsapp_number}?text={whatsapp_message.replace(' ', '%20')}"
    whatsapp_button = f"""
    <a href="{whatsapp_link}" target="_blank">
        <button style="background-color: #25D366; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
            {t("contact_button")}
        </button>
    </a>
    """
    st.markdown(whatsapp_button, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
