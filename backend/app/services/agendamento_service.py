from datetime import datetime, timedelta
from app.database import repository

# Simulação da disponibilidade fixa (Disponível de 9h às 17h, de Seg a Sex)
DISPONIBILIDADE_DIARIA = {
    'start': 9,  # 9h
    'end': 17,   # 17h
    'interval': 30 # Blocos de 30 minutos
}

def check_availability(date_str, duration=DISPONIBILIDADE_DIARIA['interval']):
    # 1. Define o período de busca (por exemplo, 1 semana)
    start_date = datetime.strptime(date_str, '%Y-%m-%d')
    end_date = start_date + timedelta(days=7) 

    # 2. Pega todos os agendamentos ocupados do DB
    ocupados = repository.get_all_agendamentos_in_period(start_date, end_date)
    
    ocupados_horarios = set()
    for item in ocupados:
        hora_inicio = item['horario']
        # Adiciona o horário de início e o próximo bloco (se a duração for > 30)
        # Lógica simplificada:
        ocupados_horarios.add(hora_inicio)
        if item['duracao'] > DISPONIBILIDADE_DIARIA['interval']:
             ocupados_horarios.add(hora_inicio + timedelta(minutes=DISPONIBILIDADE_DIARIA['interval']))
    
    # 3. Gera todos os horários possíveis e filtra
    horarios_disponiveis = []
    current_date = start_date
    while current_date < end_date:
        # Verifica se é dia útil (Segunda=0 até Sexta=4)
        if 0 <= current_date.weekday() <= 4: 
            
            hora_inicio = datetime(current_date.year, current_date.month, current_date.day, 
                                   DISPONIBILIDADE_DIARIA['start'])
            hora_fim = datetime(current_date.year, current_date.month, current_date.day, 
                                 DISPONIBILIDADE_DIARIA['end'])
            
            while hora_inicio < hora_fim:
                if hora_inicio not in ocupados_horarios:
                    horarios_disponiveis.append(hora_inicio.isoformat())
                
                hora_inicio += timedelta(minutes=DISPONIBILIDADE_DIARIA['interval'])
                
        current_date += timedelta(days=1)
        
    return horarios_disponiveis

def process_new_agendamento(nome, email, horario_str, duracao=DISPONIBILIDADE_DIARIA['interval']):
    # 1. Valida o horário
    try:
        horario = datetime.fromisoformat(horario_str)
    except ValueError:
        return False, "Formato de horário inválido."
        
    # 2. Checa se já não foi ocupado por outra pessoa no meio tempo
    # Você precisaria refazer a checagem de disponibilidade mais específica aqui.
    disponiveis = check_availability(horario.strftime('%Y-%m-%d')) # Checa só para o dia
    
    if horario_str not in disponiveis:
        return False, "Horário indisponível ou já foi agendado."
        
    # 3. Salva no Repository
    data = {
        'nome': nome,
        'email': email,
        'horario': horario,
        'duracao': duracao
    }
    repository.save_new_agendamento(data)
    
    # 4. Envia confirmação (a ser implementado no controller)
    
    return True, "Agendamento realizado com sucesso."