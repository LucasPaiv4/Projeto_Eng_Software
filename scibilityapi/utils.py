from django.core.mail import send_mail

def enviar_email_de_interesse(email_destino, nome_projeto, nome_interessado, email_interessado):
    assunto = f'Novo interesse em seu projeto: {nome_projeto}'
    mensagem = f'Olá, \n\nHá um novo interesse em seu projeto "{nome_projeto}" demonstrado por {nome_interessado}, email do interessado {email_interessado}.'
    send_mail(
        assunto,
        mensagem,
        'scibility@outlook.com.br',  # Email de origem
        [email_destino],  # Lista de emails de destino
        fail_silently=False,
    )
