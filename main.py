import sqlite3
from obj import GerenciadorEmailRecebido

DB_PATH = './banco/projeto_bradesco.db'
EMAIL_DESTINO = 'gabriel.teste001@outlook.com'
EMAIL_USUARIO = 'gabrielteste128@gmail.com'
SENHA_APP = 'clge ijhd bkkd qrit'

def exibir_logs():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("SELECT DatLog, CodStatus, Response, ObsLog FROM LogHis ORDER BY DatLog DESC")
    logs = cursor.fetchall()

    print("\n===== HISTÓRICO DE LOGS =====")
    for log in logs:
        datalog, status, response, obs = log
        print(f"[{datalog}] Status: {status} | Resp: {response} | Obs: {obs}")
    
    cursor.close()
    con.close()

def exibir_logs_por_data(data: str):
    """
    Exibe logs de uma data específica (formato: YYYY-MM-DD)
    """
    con = sqlite3.connect(DB_PATH)
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

def exibir_logs_por_remetente(remetente: str):
    """
    Exibe logs relacionados a um remetente específico.
    """
    con = sqlite3.connect(DB_PATH)
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

def menu_interativo():
    while True:
        print("\n--- MENU ---")
        print("1. Verificar novos e-mails")
        print("2. Exibir todos os logs")
        print("3. Filtrar logs por data")
        print("4. Filtrar logs por remetente")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            gerenciador = GerenciadorEmailRecebido(EMAIL_USUARIO, SENHA_APP, DB_PATH, EMAIL_DESTINO)
            gerenciador.processar_emails_nao_lidos()
        elif escolha == "2":
            exibir_logs()
        elif escolha == "3":
            data = input("Digite a data no formato AAAA-MM-DD: ")
            exibir_logs_por_data(data)
        elif escolha == "4":
            remetente = input("Digite o e-mail do remetente: ")
            exibir_logs_por_remetente(remetente)
        elif escolha == "5":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu_interativo()

#emails_recebidos = [
    #"contato@empresa1.com",
    #"fraude@naoexiste.com",
    #"email_maluco@nao.com"
