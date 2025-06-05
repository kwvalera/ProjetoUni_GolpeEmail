import datetime
import sqlite3
import smtplib
import imaplib
import email
from email.utils import parseaddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class GerenciadorEmailRecebido:
    def __init__(self, email_usuario, senha_app, db_path, email_destino):
        self.imap_host = 'imap.gmail.com'
        self.email_usuario = email_usuario
        self.senha_app = senha_app
        self.db_path = db_path
        self.email_destino = email_destino
        self.verificador = VerificadorEmail(self.db_path, self.email_destino, self.email_usuario, self.senha_app)

    def conectar(self):
        try:
            mail = imaplib.IMAP4_SSL(self.imap_host)
            mail.login(self.email_usuario, self.senha_app)
            mail.select("inbox")
            return mail
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return None

    def extrair_remetente(self, msg):
        de = msg.get("From", "")
        return parseaddr(de)[1]  # retorna só o e-mail

    def processar_emails_nao_lidos(self):
        mail = self.conectar()
        if not mail:
            return

        try:
            status, mensagens = mail.search(None, "UNSEEN")  # busca apenas não lidos
            if status != "OK":
                print("Erro ao buscar emails não lidos.")
                return

            email_ids = mensagens[0].split()

            if not email_ids:
                print("Nenhum e-mail não lido encontrado.")
                return

            for eid in email_ids:
                status, dados = mail.fetch(eid, "(RFC822)")
                if status != "OK":
                    print(f"Erro ao buscar email ID {eid.decode()}")
                    continue

                for parte in dados:
                    if isinstance(parte, tuple):
                        msg = email.message_from_bytes(parte[1])
                        remetente = self.extrair_remetente(msg)
                        print(f"Verificando remetente: {remetente}")
                        self.verificador.verificar_email(remetente)

                # marca como lido explicitamente (opcional, já deve estar marcado ao buscar)
                mail.store(eid, '+FLAGS', '\\Seen')

        except Exception as e:
            print(f"Erro ao processar emails: {e}")
        finally:
            mail.logout()


class VerificadorEmail:
    def __init__(self, db_path, email_destino, email_usuario, senha_app):
        self.email_usuario = email_usuario
        self.senha_app = senha_app
        self.db_path = db_path
        self.email_destino = email_destino
        self.alerta = AlertaEmailSuspeito(self.email_usuario, self.senha_app, self.email_destino)

    def conectar_banco(self):
        con = sqlite3.connect(self.db_path)
        con.execute("PRAGMA foreign_keys = ON")
        return con

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
            self.alerta.enviar_alerta(remetente)

        con.commit()
        cursor.close()
        con.close()


class AlertaEmailSuspeito:
    def __init__(self, email_origem, senha_app, email_destino):
        self.email_origem = email_origem
        self.senha_app = senha_app
        self.email_destino = email_destino
        self.smtp_host = 'smtp.gmail.com'
        self.smtp_port = 587

    def enviar_alerta(self, remetente_suspeito):
        try:
            # Criar mensagem
            mensagem = MIMEMultipart()
            mensagem['From'] = self.email_origem
            mensagem['To'] = self.email_destino
            mensagem['Subject'] = "Alerta: E-mail suspeito detectado"

            corpo = f"O remetente '{remetente_suspeito}' foi identificado como suspeito."
            mensagem.attach(MIMEText(corpo, 'plain'))

            # Enviar e-mail via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as servidor:
                servidor.starttls()
                servidor.login(self.email_origem, self.senha_app)
                servidor.send_message(mensagem)
                print(f"Alerta enviado para {self.email_destino} sobre '{remetente_suspeito}'")
        except Exception as e:
            print(f"Erro ao enviar alerta: {e}")
