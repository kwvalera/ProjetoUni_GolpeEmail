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

    def exibir_logs(self):
        con = self.conectar_banco()
        cursor = con.cursor()

        cursor.execute("SELECT DatLog, CodStatus, Response, ObsLog FROM LogHis ORDER BY DatLog DESC")
        logs = cursor.fetchall()

        print("\n===== HISTÓRICO DE LOGS =====")
        for log in logs:
            datalog, status, response, obs = log
            print(f"[{datalog}] Status: {status} | Resp: {response} | Obs: {obs}")
        
        cursor.close()
        con.close()

    def exibir_logs_por_status(self, status):
        con = self.conectar_banco()
        cursor = con.cursor()

        cursor.execute("""
            SELECT DatLog, CodStatus, Response, ObsLog 
            FROM LogHis
            WHERE CodStatus = ?
            ORDER BY DatLog DESC
        """, (status,))

        logs = cursor.fetchall()
        if logs:
            print(f"\n[LOGS - STATUS {status}]\n")
            for log in logs:
                print(f"Data: {log[0]} | Status: {log[1]} | Resposta: {log[2]} | Obs: {log[3]}")
        else:
            print(f"\nNenhum log encontrado com status {status}.")

        cursor.close()
        con.close()

    def exibir_logs_por_data(self, data: str):
        """
        Exibe logs de uma data específica (formato: YYYY-MM-DD)
        """
        con = self.conectar_banco()
        cursor = con.cursor()

        cursor.execute("""
            SELECT DatLog, CodStatus, Response, ObsLog
            FROM LogHis
            WHERE DATE(DatLog) = ?
            ORDER BY DatLog DESC
        """, (data,))

        logs = cursor.fetchall()
        if logs:
            print(f"\n[LOGS - DATA {data}]\n")
            for log in logs:
                print(f"Data: {log[0]} | Status: {log[1]} | Resposta: {log[2]} | Obs: {log[3]}")
        else:
            print(f"\nNenhum log encontrado na data {data}.")

        cursor.close()
        con.close()

    def exibir_logs_por_remetente(self, remetente: str):
        """
        Exibe logs relacionados a um remetente específico.
        """
        con = self.conectar_banco()
        cursor = con.cursor()

        busca = f"%{remetente}%"
        cursor.execute("""
            SELECT DatLog, CodStatus, Response, ObsLog
            FROM LogHis
            WHERE ObsLog LIKE ?
            ORDER BY DatLog DESC
        """, (busca,))

        logs = cursor.fetchall()
        if logs:
            print(f"\n[LOGS - REMETENTE {remetente}]\n")
            for log in logs:
                print(f"Data: {log[0]} | Status: {log[1]} | Resposta: {log[2]} | Obs: {log[3]}")
        else:
            print(f"\nNenhum log encontrado para o remetente: {remetente}")

        cursor.close()
        con.close()

def menu_interativo(verificador):
    while True:
        print("\n--- MENU ---")
        print("1. Exibir todos os logs")
        print("2. Filtrar logs por data")
        print("3. Filtrar logs por remetente")
        print("4. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            verificador.exibir_logs()
        elif escolha == "2":
            data = input("Digite a data no formato AAAA-MM-DD: ")
            verificador.exibir_logs_por_data(data)
        elif escolha == "3":
            remetente = input("Digite o e-mail do remetente: ")
            verificador.exibir_logs_por_remetente(remetente)
        elif escolha == "4":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")



# Instanciando e usando a classe
verificador = VerificadorEmail(DB_PATH)

emails_recebidos = [
    "contato@empresa1.com",
    "fraude@naoexiste.com",
    "email_maluco@nao.com"
]
if __name__ == "__main__":
    verificador = VerificadorEmail(DB_PATH)
    menu_interativo(verificador)

#for email in emails_recebidos:
    #verificador.verificar_email(email)

#verificador.exibir_logs()
#verificador.exibir_logs_por_status(403)
#verificador.exibir_logs_por_data("2025-06-04") 
#verificador.exibir_logs_por_remetente("fraude@naoexiste.com")
