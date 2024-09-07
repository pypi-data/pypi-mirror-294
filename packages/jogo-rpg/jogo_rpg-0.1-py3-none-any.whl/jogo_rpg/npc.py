
from random import randint

lista_npcs = []

def criar_npc(level):

    novo_npc = {
        "nome" : f"Monstro #{level}",
        "level" : level,
        "dano" : 5 * level,
        "hp" : 100 * level,
        "exp" : 7 * level,
        "hp_max" : 100 * level,
    }
    
    return novo_npc

def gerar_npcs(n_npcs):
    for x in range(n_npcs):
        npc = criar_npc(x + 1)
        lista_npcs.append(npc)

def exibir_npcs():
    for npc in lista_npcs:
       exibir_npc(npc)


def exibir_npc(npc):
    print(f"Nome: {npc['nome']} // Level: {npc['level']} // Dano: {npc['dano']} // HP: {npc['hp']} // EXP: {npc['exp']}")

def reset_npc(npc):
    npc['hp'] = npc['hp_max']