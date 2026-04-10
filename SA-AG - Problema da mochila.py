import random
import math
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURAÇÕES E LEITURA ---
CAPACIDADE_MAX = 28
ITER = 1000

def carregar_dados(caminho):
    pesos, valores = [], []
    with open(caminho, 'r') as f:
        linhas = f.readlines()
        for linha in linhas[1:]:
            if linha.strip():
                v_str, p_str = linha.strip().split(',')
                valores.append(int(v_str))
                pesos.append(int(p_str))
    return pesos, valores

# --- 2. FUNÇÃO DE FITNESS ---
def calcular_fitness(estado, p, v, cap):
    peso_total = sum(e * p_i for e, p_i in zip(estado, p))
    if peso_total > cap:
        return 0
    return sum(e * v_i for e, v_i in zip(estado, v))

# --- 3. TÊMPERA SIMULADA (SA) ---
def tempera_simulada(p, v, cap, t=80.0, max_iteracoes=1000):
    n = len(p)
    atual = [random.randint(0, 1) for _ in range(n)]
    fit_atual = calcular_fitness(atual, p, v, cap)
    
    melhor_global = list(atual)
    melhor_fitness = fit_atual

    for _ in range(max_iteracoes):
        proximo = list(atual)
        idx = random.randint(0, n - 1)
        proximo[idx] = 1 - proximo[idx]
        
        fit_proximo = calcular_fitness(proximo, p, v, cap)
        delta_e = fit_proximo - fit_atual
        
        if delta_e > 0 or (t > 0 and random.random() < math.exp(delta_e / t)):
            atual = proximo
            fit_atual = fit_proximo
            if fit_atual > melhor_fitness:
                melhor_fitness = fit_atual
                melhor_global = list(atual)
        
        t *= 0.999
    return melhor_fitness

# --- 4. ALGORITMO GENÉTICO (AG) ---
def algoritmo_genetico(p, v, cap, tamanho_pop=50, geracoes=100):
    n = len(p)
    populacao = [[random.randint(0, 1) for _ in range(n)] for _ in range(tamanho_pop)]
    melhor_fitness_global = 0
    
    for _ in range(geracoes):
        fitness = [calcular_fitness(ind, p, v, cap) for ind in populacao]
        
        # Atualiza melhor global
        max_fit_gen = max(fitness)
        if max_fit_gen > melhor_fitness_global:
            melhor_fitness_global = max_fit_gen
            
        # Nova geração
        nova_pop = []
        # Adiciona 1 para evitar peso zero na escolha aleatória
        pesos_selecao = [f + 1 for f in fitness]
        
        for _ in range(tamanho_pop // 2):
            p1 = random.choices(populacao, weights=pesos_selecao, k=1)[0]
            p2 = random.choices(populacao, weights=pesos_selecao, k=1)[0]
            
            ponto = random.randint(1, n - 1)
            f1, f2 = p1[:ponto] + p2[ponto:], p2[:ponto] + p1[ponto:]
            
            for filho in [f1, f2]:
                if random.random() < 0.2: # Mutação
                    idx = random.randint(0, n - 1)
                    filho[idx] = 1 - filho[idx]
                nova_pop.append(filho)
        populacao = nova_pop
        
    return melhor_fitness_global

# --- 5. EXECUÇÃO ---
if __name__ == "__main__":
    pesos, valores = carregar_dados('dados_mochila.txt')

    res_sa = [tempera_simulada(pesos, valores, CAPACIDADE_MAX) for _ in range(ITER)]
    res_ag = [algoritmo_genetico(pesos, valores, CAPACIDADE_MAX) for _ in range(ITER)]

    print(f"\n--- RESULTADOS FINAIS ---")
    print(f"Melhor SA: {max(res_sa)}")
    print(f"Melhor AG: {max(res_ag)}")

    # Plotagem
    plt.hist(res_sa, bins=20, alpha=0.6, label='SA - Têmpera Simulada', color='blue')
    plt.hist(res_ag, bins=20, alpha=0.6, label='AG - Algoritmo Genético', color='orange')
    plt.title("Distribuição de Fitness")
    plt.legend()
    plt.show()