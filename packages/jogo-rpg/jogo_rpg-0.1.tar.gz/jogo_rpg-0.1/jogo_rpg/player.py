player = {
    "nome" : "Macauli",
    "level" : 1,
    "exp" : 0,
    "exp_max" : 30,
    "hp" : 100,
    "hp_max" : 100,
    "dano" : 25,
}
def level_up():
    if player['exp'] >= player['exp_max']:
        player['level'] += 1
        player['exp'] = 0
        player['exp_max'] = player['exp_max'] * 2
        player['hp_max'] += 20

def exibir_player():
    print(f"Nome: {player['nome']} // Level: {player['level']} // Dano: {player['dano']} // HP: {player['hp']}/{player['hp_max']} // EXP: {player['exp']}/{player['exp_max']}")
    

def reset_player():
    player['hp'] = player['hp_max']

