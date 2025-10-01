from datetime import datetime, timedelta
from app.database import repository

DISPONIBILIDADE_DIARIA = {
    'start': 9,
    'end': 17,
    'interval': 30
}

def check_availability(date_str, duration=DISPONIBILIDADE_DIARIA['interval']):
    start_date = datetime.strptime(date_str, '%Y-%m-%d')
    end_date = start_date + timedelta(days=7) 

    print(f"[DEBUG] Buscando agendamentos entre {start_date} e {end_date}")
    ocupados = repository.get_all_agendamentos_in_period(start_date, end_date)
    print(f"[DEBUG] Agendamentos ocupados: {ocupados}")
    
    ocupados_horarios = set()
    for item in ocupados:
        hora_inicio = item['horario']
        ocupados_horarios.add(hora_inicio)
        if item['duracao'] > DISPONIBILIDADE_DIARIA['interval']:
             ocupados_horarios.add(hora_inicio + timedelta(minutes=DISPONIBILIDADE_DIARIA['interval']))
    
    horarios_disponiveis = []
    current_date = start_date
    while current_date < end_date:
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
    
    print(f"[DEBUG] Total de horários disponíveis: {len(horarios_disponiveis)}")
    return horarios_disponiveis

def process_new_agendamento(nome, email, horario_str, duracao=DISPONIBILIDADE_DIARIA['interval']):
    print(f"\n[DEBUG] === INICIANDO AGENDAMENTO ===")
    print(f"[DEBUG] Nome: {nome}, Email: {email}, Horário: {horario_str}")
    
    try:
        horario = datetime.fromisoformat(horario_str)
        print(f"[DEBUG] Horário convertido: {horario}")
    except ValueError as e:
        print(f"[DEBUG] ERRO ao converter horário: {e}")
        return False, "Formato de horário inválido."
    
    disponiveis = check_availability(horario.strftime('%Y-%m-%d'))
    
    print(f"[DEBUG] Horário solicitado (ISO): {horario_str}")
    print(f"[DEBUG] Horário está na lista? {horario_str in disponiveis}")
    print(f"[DEBUG] Primeiros 3 disponíveis: {disponiveis[:3] if disponiveis else 'Nenhum'}")
    
    if horario_str not in disponiveis:
        print(f"[DEBUG] FALHA: Horário não encontrado")
        return False, f"Horário indisponível. Total de slots livres: {len(disponiveis)}"
    
    print(f"[DEBUG] Salvando no banco...")
    data = {
        'nome': nome,
        'email': email,
        'horario': horario,
        'duracao': duracao
    }
    
    try:
        repository.save_new_agendamento(data)
        print(f"[DEBUG] ✓ Salvo com sucesso!")
    except Exception as e:
        print(f"[DEBUG] ✗ ERRO ao salvar: {e}")
        return False, f"Erro ao salvar: {str(e)}"
    
    return True, "Agendamento realizado com sucesso."