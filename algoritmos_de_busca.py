import random
import math

pesos = [4-12]
valores = [4, 5, 7-11, 13]
capacidade_max = 28

def calcular_fitness(estado):
    peso_total = sum(estado[i] * pesos[i] for i in range(len(estado)))
    if peso_total > capacidade_max:
        return 0  # Penaliza soluções que excedem a capacidade
    return sum(estado[i] * valores[i] for i in range(len(estado)))

def tempera_simulada():
    # Estado inicial aleatório
    atual = [random.randint(0, 1) for _ in range(len(pesos))]
    t = 1.0  # Temperatura inicial
    resfriamento = 0.995

    for i in range(1000):
        if t < 0.001: break
        
        proximo = list(atual)
        idx = random.randint(0, len(proximo) - 1)
        proximo[idx] = 1 - proximo[idx]
        
        delta_e = calcular_fitness(proximo) - calcular_fitness(atual)
        
        if delta_e > 0:
            atual = proximo
        else:
            probabilidade = math.exp(delta_e / t)
            if random.random() < probabilidade:
                atual = proximo
        
        t *= resfriamento
        
    return atual, calcular_fitness(atual)

solucao, valor = tempera_simulada()
print(f"Têmpera Simulada - Valor: {valor}, Itens: {solucao}")

def algoritmo_genetico(tamanho_pop=50, geracoes=100):
    # Inicializa população aleatória
    populacao = [[random.randint(0, 1) for _ in range(len(pesos))] for _ in range(tamanho_pop)]
    
    for gen in range(geracoes):
        # Avaliação de Fitness
        fitness = [calcular_fitness(ind) for ind in populacao]
        
        nova_pop = []
        for _ in range(tamanho_pop // 2):
            # Seleção por Roleta
            p1 = random.choices(populacao, weights=[f + 1 for f in fitness], k=1)
            p2 = random.choices(populacao, weights=[f + 1 for f in fitness], k=1)
            
            # Crossover (Ponto único)
            ponto = random.randint(1, len(pesos) - 1)
            filho1 = p1[:ponto] + p2[ponto:]
            filho2 = p2[:ponto] + p1[ponto:]
            
            # Mutação (baixa probabilidade)
            for f in [filho1, filho2]:
                if random.random() < 0.05:
                    idx = random.randint(0, len(pesos) - 1)
                    f[idx] = 1 - f[idx]
                nova_pop.append(f)
        
        populacao = nova_pop
    
    # Retorna o melhor da última geração
    melhor = max(populacao, key=calcular_fitness)
    return melhor, calcular_fitness(melhor)

solucao_ag, valor_ag = algoritmo_genetico()
print(f"Algoritmo Genético - Valor: {valor_ag}, Itens: {solucao_ag}")