from datetime import datetime, timedelta
from app.database import repository

def check_availability(date_str):
    """Retorna todos os horários ocupados em um período de 7 dias a partir da data"""
    start_date = datetime.strptime(date_str, '%Y-%m-%d')
    end_date = start_date + timedelta(days=7) 

    ocupados = repository.get_all_agendamentos_in_period(start_date, end_date)
    
    # Retorna lista de horários ocupados com suas durações
    ocupados_detalhes = []
    for item in ocupados:
        ocupados_detalhes.append({
            'horario': item['horario'].isoformat() if isinstance(item['horario'], datetime) else item['horario'],
            'duracao': item['duracao']
        })
    
    return ocupados_detalhes

def is_horario_disponivel(horario_solicitado, duracao_solicitada):
    """Verifica se o horário está disponível considerando a duração"""
    ocupados = repository.get_all_agendamentos_in_period(
        horario_solicitado - timedelta(days=1),
        horario_solicitado + timedelta(days=1)
    )
    
    fim_solicitado = horario_solicitado + timedelta(minutes=duracao_solicitada)
    
    for item in ocupados:
        hora_ocupada = item['horario']
        fim_ocupado = hora_ocupada + timedelta(minutes=item['duracao'])
        
        # Verifica se há conflito de horários
        if (horario_solicitado < fim_ocupado and fim_solicitado > hora_ocupada):
            return False, f"Conflito com agendamento existente às {hora_ocupada.strftime('%d/%m/%Y %H:%M')}"
    
    return True, "Horário disponível"

def process_new_agendamento(nome, email, horario_str, duracao=30):
    try:
        horario = datetime.fromisoformat(horario_str)
    except ValueError:
        return False, "Formato de horário inválido. Use o formato ISO: YYYY-MM-DDTHH:MM:SS"
    
    # Valida duração mínima
    if duracao <= 0:
        return False, "Duração deve ser maior que zero."
    
    # Verifica disponibilidade
    disponivel, mensagem = is_horario_disponivel(horario, duracao)
    
    if not disponivel:
        return False, mensagem
    
    data = {
        'nome': nome,
        'email': email,
        'horario': horario,
        'duracao': duracao
    }
    
    try:
        repository.save_new_agendamento(data)
    except Exception as e:
        return False, f"Erro ao salvar agendamento: {str(e)}"
    
    return True, "Agendamento realizado com sucesso."