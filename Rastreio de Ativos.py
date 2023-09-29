import yfinance as yf
import smtplib
import schedule
import time

# cadastro de e-mail para notificações
SEU_EMAIL = 'seu_email@gmail.com'
SUA_SENHA = 'sua_senha'
EMAIL_DESTINO = 'destinatario_email@gmail.com'
ASSUNTO = 'Rastreamento de Ativo'
MENSAGEM_TEMPLATE = """\
Olá,segue arquivo
Nome: {nome}
Preço atual ({moeda}): {preco_atual}
Data da última atualização: {data_atualizacao}
Atenciosamente,
Seu Bot de Rastreamento de Ativos
"""

def enviar_email(ticker, nome, preco_atual, moeda, data_atualizacao):
    mensagem = MENSAGEM_TEMPLATE.format(
        ticker=ticker,
        nome=nome,
        preco_atual=preco_atual,
        moeda=moeda,
        data_atualizacao=data_atualizacao
    )

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SEU_EMAIL, SUA_SENHA)
        server.sendmail(SEU_EMAIL, EMAIL_DESTINO, mensagem)
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def rastrear_ativo(ticker):
    try:
        ativo = yf.Ticker(ticker)
        info = ativo.info
        nome = info['longName']
        preco_atual = info['regularMarketPrice']
        moeda = info['currency']
        data_atualizacao = info['regularMarketTime']

        print(f"Nome: {nome}")
        print(f"Ticker: {ticker}")
        print(f"Preço atual ({moeda}): {preco_atual}")
        print(f"Data da última atualização: {data_atualizacao}")

        enviar_email(ticker, nome, preco_atual, moeda, data_atualizacao)
    except Exception as e:
        print(f"Erro ao rastrear o ativo {ticker}: {e}")

if __name__ == "__main__":
    ativo_ticker = input("Digite o ticker do ativo que deseja rastrear: ")

    # Rastrear o ativo imediatamente
    rastrear_ativo(ativo_ticker)

    # Agendar rastreamento de ativo a cada 6 horas (pode ser alterado conforme necessário)
    schedule.every(6).hours.do(rastrear_ativo, ativo_ticker)

    while True:
        schedule.run_pending()
        time.sleep(1)
