from flask_mail import Message
from app.__init__ import mail # Importa a instância do Flask-Mail configurada

def send_confirmation_email(recipient_email, recipient_name, scheduled_time):
    """
    Função utilitária para enviar o e-mail de confirmação.
    """
    
    subject = f"Confirmação de Agendamento com {recipient_name}"
    
    # Corpo do e-mail em texto simples
    body = (
        f"Olá {recipient_name},\n\n"
        f"Seu agendamento está confirmado!\n"
        f"Horário: {scheduled_time}\n"
        f"Por favor, chegue no horário.\n\n"
        f"Atenciosamente,\n"
        f"A Equipe de Agendamentos."
    )
    
    # Cria o objeto Message
    msg = Message(subject, recipients=[recipient_email], body=body)
    
    # Envia o e-mail
    try:
        # A função mail.send() é bloqueante, mas para simplicidade, 
        # a usamos diretamente aqui. Em produção, considere filas de tarefas (como Celery).
        mail.send(msg)
        return True
    except Exception as e:
        print(f"ERRO AO ENVIAR EMAIL: {e}")
        # Em um projeto simples, podemos logar o erro e seguir
        return False