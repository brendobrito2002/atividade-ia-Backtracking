disciplinas_professores = {
    "Cálculo para Computação I": "Marcius",
    "Introdução à Computação": "Ryan",
    "Introdução à Programação": "Luís, Renê",
    "Geometria Analítica": "Normando",
    "Lógica Matemática": "Gersonilo"
}

horarios = [
    "Segunda 18:30 - 20:10", "Segunda 20:10 - 21:50",
    "Terça 18:30 - 20:10", "Terça 20:10 - 21:50",
    "Quarta 18:30 - 20:10", "Quarta 20:10 - 21:50",
    "Quinta 18:30 - 20:10", "Quinta 20:10 - 21:50",
    "Sexta 18:30 - 20:10", "Sexta 20:10 - 21:50"
]

# Restricoes
MAX_INTRO_COMPUTACAO = 1  
MAX_CALCULO = 2  
MAX_LOGICA_MATEMATICA = 2  
MAX_GEOMETRIA_ANALITICA = 2  
MAX_INTRO_PROGRAMACAO = 3  

RESTRICOES = {
    'Introdução à Computação': MAX_INTRO_COMPUTACAO,
    'Introdução à Programação': MAX_INTRO_PROGRAMACAO,
    'Cálculo para Computação I': MAX_CALCULO,
    'Lógica Matemática': MAX_LOGICA_MATEMATICA,
    'Geometria Analítica': MAX_GEOMETRIA_ANALITICA
}

# Função para verificar se existe conflito de horário com os professores
def ha_conflito(professor_horarios, professor, horario):
    return horario in professor_horarios.get(professor, [])

# Função para verificar restrições de quantidade de aulas
def verifica_restricoes(grade, turma):
    contagem = {disciplina: 0 for disciplina in disciplinas_professores}
    for horario, (disciplina, _) in grade[turma].items():
        contagem[disciplina] += 1

    for disciplina, qtd in contagem.items():
        if disciplina == "Introdução à Computação" and qtd > MAX_INTRO_COMPUTACAO:
            return False
        elif disciplina == "Introdução à Programação" and qtd > MAX_INTRO_PROGRAMACAO:
            return False
        elif disciplina == "Cálculo para Computação I" and qtd > MAX_CALCULO:
            return False
        elif disciplina == "Lógica Matemática" and qtd > MAX_LOGICA_MATEMATICA:
            return False
        elif disciplina == "Geometria Analítica" and qtd > MAX_GEOMETRIA_ANALITICA:
            return False
    return True

# Função de alocação ajustada
def alocar_aulas(turma, horario_idx, grade, professor_horarios, intro_computacao_alocada):
    if turma == 3:  # Todas as turmas foram alocadas
        return True
    if horario_idx == len(horarios):  # Todos os horários foram testados
        return False

    proximo_horario = horarios[horario_idx]

    # Verificar se o próximo horário já foi alocado corretamente
    for disciplina, professores in disciplinas_professores.items():
        if disciplina == "Introdução à Computação" and intro_computacao_alocada:
            continue

        if isinstance(professores, list):  # Mais de um professor
            for professor in professores:
                if not ha_conflito(professor_horarios, professor, proximo_horario):
                    # Aloca a aula temporariamente
                    grade[turma][proximo_horario] = (disciplina, professor)
                    professor_horarios[professor].append(proximo_horario)

                    # Verifica restrições e chama recursivamente
                    if verifica_restricoes(grade, turma):
                        if disciplina == "Introdução à Computação":
                            if alocar_aulas(turma, horario_idx + 1, grade, professor_horarios, True):
                                return True
                        else:
                            if alocar_aulas(turma, horario_idx + 1, grade, professor_horarios, intro_computacao_alocada):
                                return True

                    # Desfaz a alocação (backtrack)
                    del grade[turma][proximo_horario]
                    professor_horarios[professor].remove(proximo_horario)
        else:  # Apenas um professor
            professor = professores
            if not ha_conflito(professor_horarios, professor, proximo_horario):
                # Aloca a aula temporariamente
                grade[turma][proximo_horario] = (disciplina, professor)
                professor_horarios[professor].append(proximo_horario)

                # Verifica restrições e chama recursivamente
                if verifica_restricoes(grade, turma):
                    if disciplina == "Introdução à Computação":
                        if alocar_aulas(turma, horario_idx + 1, grade, professor_horarios, True):
                            return True
                    else:
                        if alocar_aulas(turma, horario_idx + 1, grade, professor_horarios, intro_computacao_alocada):
                            return True

                # Desfaz a alocação (backtrack)
                del grade[turma][proximo_horario]
                professor_horarios[professor].remove(proximo_horario)

    # Tenta o próximo horário
    if alocar_aulas(turma, horario_idx + 1, grade, professor_horarios, intro_computacao_alocada):
        return True

    # Se todos os horários falharem, tenta a próxima turma
    return alocar_aulas(turma + 1, 0, grade, professor_horarios, intro_computacao_alocada)

# Função para alocar as aulas faltantes após a alocação inicial
def verificar_e_alocar_faltantes(grade, disciplinas_alocadas):
    for turma_idx, turma in enumerate(grade):
        contagem_dis = {disciplina: 0 for disciplina in RESTRICOES.keys()}

        # Conta as aulas alocadas para cada disciplina
        for horario, (disciplina, _) in turma.items():
            if disciplina in contagem_dis:
                contagem_dis[disciplina] += 1

        # Aloca as aulas faltantes, respeitando as restrições
        for horario in horarios:
            if horario not in turma:
                for disciplina, max_aulas in RESTRICOES.items():
                    if contagem_dis[disciplina] < max_aulas and disciplina not in disciplinas_alocadas[turma_idx]:
                        professores = disciplinas_professores[disciplina]
                        if isinstance(professores, list):
                            for professor in professores:
                                turma[horario] = (disciplina, professor)
                                contagem_dis[disciplina] += 1
                                disciplinas_alocadas[turma_idx].append(disciplina)
                                break
                        else:
                            professor = professores
                            turma[horario] = (disciplina, professor)
                            contagem_dis[disciplina] += 1
                            disciplinas_alocadas[turma_idx].append(disciplina)
                        break
    return grade, disciplinas_alocadas

# Função para ordenar os horários corretamente
def ordenar_horarios(horarios):
    dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    return sorted(horarios, key=lambda x: (dias_da_semana.index(x.split()[0]), x.split()[1], x.split()[2]))

# Função principal que inicializa o processo de alocação de aulas
def main():
    grade = [{}, {}, {}]
    professor_horarios = {professor: [] for lista in disciplinas_professores.values() for professor in (lista if isinstance(lista, list) else [lista])}
    disciplinas_alocadas = [[] for _ in range(len(grade))] 

    if alocar_aulas(0, 0, grade, professor_horarios, False):
        for i, turma in enumerate(grade):
            horarios_sorted = ordenar_horarios(list(turma.keys()))
            for horario in horarios_sorted:
                disciplina, professor = turma[horario]
    else:
        print("Não foi possível alocar as aulas sem conflitos.")

    # Verifica e aloca as disciplinas faltantes
    grade, disciplinas_alocadas = verificar_e_alocar_faltantes(grade, disciplinas_alocadas)

    # Exibe a alocação final das turmas
    for i, turma in enumerate(grade):
        print(f"\nTurma {i + 1}:")
        horarios_sorted = ordenar_horarios(list(turma.keys()))
        for horario in horarios_sorted:
            disciplina, professor = turma[horario]
            print(f"{horario}: {disciplina} ({', '.join(professor) if isinstance(professor, list) else professor})")

# Inicia o programa
if __name__ == "__main__":
    main()
