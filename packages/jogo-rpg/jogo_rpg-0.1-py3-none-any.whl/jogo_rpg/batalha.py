from jogo_rpg.player import player, reset_player, level_up, exibir_player
from jogo_rpg.npc import reset_npc, exibir_npc, lista_npcs
def atacar_player(npc):
    player["hp"] -= npc["dano"]

def atacar_npc(npc):
    npc['hp'] -= player["dano"]


def exibir_info_batalha(npc):
    print(f"Player: {player['hp']} // {player['hp_max']}")
    print(f"NPC: {npc['nome']} // {npc['hp']}// {npc['hp_max']}")
    print("----------------------------\n")


def iniciar_batalha(npc):
    while player["hp"] > 0 and npc["hp"] > 0:
        atacar_npc(npc)
        atacar_player(npc)
        exibir_info_batalha(npc)
    if player['hp'] > 0:
        print(f"O {player['nome']} derrotou o {npc['nome']} e ganhou {npc['exp']} de EXP!")
        player['exp'] += npc['exp']
        exibir_player()
    else:
        print(f"O {npc['nome']} derrotou o {player['nome']}")
        exibir_npc(npc)


    level_up()
    reset_npc(npc)
    reset_player()