import sqlite3
import datetime
import smtplib
from email.message import EmailMessage

# Caminho do banco
DB_PATH = './banco/projeto_bradesco.db'

# Configurações do Mailtrap SMTP
SMTP_HOST = 'sandbox.smtp.mailtrap.io'
SMTP_PORT = 587
SMTP_USER = ''
SMTP_PASS = ''
EMAIL_DESTINO = 'teste_prefeitura@exemplo.com'

class VerificadorEmail:
    def __init__(self, db_path):
        self.db_path = db_path

    def conectar_banco(self):
        con = sqlite3.connect(self.db_path)
        con.execute("PRAGMA foreign_keys = ON")
        return con
    
    def enviar_alerta(self, remetente):
        msg = EmailMessage()
        msg['Subject'] = 'Alerta de e-mail suspeito'
        msg['From'] = 'alerta@sistema_prefeitura.com'
        msg['To'] = EMAIL_DESTINO
        msg.set_content(f'Você recebeu um email suspeito: {remetente}')

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)

    def verificar_email(self, remetente: str):
        con = self.conectar_banco()
        cursor = con.cursor()

        cursor.execute("SELECT * FROM Email WHERE EmaCom = ?", (remetente,))
        resultado = cursor.fetchone()

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if resultado:
            print(f"[OK] Email autorizado: {remetente}")
            cursor.execute("""
                INSERT INTO LogHis (DatLog, CodStatus, Response, ObsLog)
                VALUES (?, ?, ?, ?)
            """, (now, 200, "Autorizado", f"E-mail {remetente} reconhecido."))
        else:
            print(f"[ALERTA] Email suspeito: {remetente}")
            cursor.execute("""
                INSERT INTO LogHis (DatLog, CodStatus, Response, ObsLog)
                VALUES (?, ?, ?, ?)
            """, (now, 403, None, f"E-mail {remetente} não reconhecido."))
            self.enviar_alerta(remetente)

        con.commit()
        cursor.close()
        con.close()


# Instanciando e usando a classe
verificador = VerificadorEmail(DB_PATH)

emails_recebidos = [
    "contato@empresa1.com",
    "fraude@naoexiste.com",
    "email_maluco@nao.com"
]

for email in emails_recebidos:
    verificador.verificar_email(email)
