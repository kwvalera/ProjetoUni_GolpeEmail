import sqlite3
import datetime

# Caminho do banco
DB_PATH = './banco/projeto_bradesco.db'

class VerificadorEmail:
    def __init__(self, db_path):
        self.db_path = db_path

    def conectar_banco(self):
        con = sqlite3.connect(self.db_path)
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def verificar_email(self, remetente: str):
        con = self.conectar_banco()
        cursor = con.cursor()

        cursor.execute("SELECT * FROM email WHERE EmaCom = ?", (remetente,))
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

        con.commit()
        cursor.close()
        con.close()


# Instanciando e usando a classe
verificador = VerificadorEmail(DB_PATH)

emails_recebidos = [
    "contato@empresa1.com",
    "fraude@naoexiste.com"
]

for email in emails_recebidos:
    verificador.verificar_email(email)
