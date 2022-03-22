import tkinter as tk
from tkinter import messagebox
from backend_functions import *
from random import uniform, randint


max_action = []
strat_form = []
frame_profile_list = []
frame_calcul_list = []
frame_simu_list = []
input_pq = [None, None]
nash_simulation = [None, None]
score = [0, 0]
score_mixte = [0, 0]


# Delete old frame when input new data
def deleteFrames(frame_list):
    # Delete old frames
    if len(frame_list) != 0:
        for elem in frame_list:
            try:
                frame = main_window.nametowidget(elem)
                frame.destroy()
            except KeyError:
                pass
    return []


# For 2 players: Trigger to generate entries to input strategic forms
def createFormTwoPlayers():
    global frame_profile_list, frame_calcul_list, frame_simu_list
    global max_action
    assert len(max_action) == 2, "Only 2 players are accepted."

    # Delete all frames on the previous executions
    frame_profile_list = deleteFrames(frame_profile_list)
    frame_calcul_list = deleteFrames(frame_calcul_list)
    frame_simu_list = deleteFrames(frame_simu_list)

    for i in range(max_action[0]):
        for j in range(max_action[1]):
            name_frame = "frame{}-{}".format(i,j)
            frame_profile_list.append(name_frame)
            frame_form = tk.Frame(name=name_frame, master=main_window, relief=tk.RAISED, borderwidth=1)
            frame_form.grid(row=2+i, column=j, padx=5, pady=5)
            entry = tk.Entry(name="number",master=frame_form, fg="black", bg="white", width=10)
            entry.pack()


# Petites fonctions pour convertir un liste d'index a un string selon les besoins
def convertListToStringForFrame(l):
    assert isinstance(l, list), "Must convert a list."
    return str(l).replace("[", "").replace("]", "").replace(" ", "").replace(",", "-")

# Petites fonctions pour convertir un liste d'index a un string selon les besoins
def convertListToStringToPrint(l):
    assert isinstance(l, list), "Must convert a list."
    l = [str(elem) for elem in l]
    return (", ".join(l))



# For more than 2 players: Trigger to generate entries to input strategic forms
def createFormMultiplePlayers():
    global frame_profile_list, frame_calcul_list, frame_simu_list
    global max_action
    assert len(max_action) > 2, "This function is used only on more than 2 players."

    # Delete all frames on the previous executions
    # Delete all frames on the previous executions
    frame_profile_list = deleteFrames(frame_profile_list)
    frame_calcul_list = deleteFrames(frame_calcul_list)
    frame_simu_list = deleteFrames(frame_simu_list)

    all_index_profile = generateIndex(max_action)
    for num_profile, elem in enumerate(all_index_profile):
        name_frame = "frame{}".format(convertListToStringForFrame(elem))
        frame_profile_list.append(name_frame)
        frame_form = tk.Frame(name=name_frame, master=main_window, relief=tk.RAISED, borderwidth=1)
        frame_form.grid(row=2+(num_profile%4), column=int(num_profile/4), padx=10, pady=5)
        text = tk.Label(name="text", master=frame_form, text= "{}".format(convertListToStringForFrame(elem)))
        entry = tk.Entry(name="number",master=frame_form, fg="black", bg="white", width=10)
        text.pack()
        entry.pack()


# Déclencheur de bouton pour obtenir de max_action et créer les Entries pour forme stratégique
def generateMatrix():
    global max_action

    try:
        string_max_action = entry_actions_per_player.get()
        string_max_action = string_max_action.replace(" ", "")
        max_action = string_max_action.split(",")
        max_action = [int(elem) for elem in max_action]
        if len(max_action) < 2:
            messagebox.showerror("Erreur !", "Il faut avoir au moins 2 joueurs.")
            max_action = []
            return
        for elem in max_action:
            if elem < 2:
                messagebox.showerror("Erreur !", "Chaque joueur doivent avoir au moins 2 actions.")
                max_action = []
                return
    # Exception: Valeurs d'entrées ne sont pas integer
    except ValueError:
        messagebox.showerror("Erreur !", "Format d'entrées incorrect.")
        max_action = []
        return

    # S'il y a trop d'actions (donc l'écran ne peut pas les afficher)
    total_actions = 1
    for elem in max_action:
        total_actions *= elem
    if total_actions > 50:
        messagebox.showwarning("Avertissement !", "Trop d'actions pour afficher à l'écran.")
        max_action = []
        return
    
    if len(max_action) == 2:
        createFormTwoPlayers()
    if len(max_action) > 2:
        createFormMultiplePlayers()

# Récupérer des données d'entrées
def getData():
    global max_action, strat_form, frame_profile_list

    strat_form = []
    all_index_profile = generateIndex(max_action)

    for idx_profile in range(len(all_index_profile)):
        entry_profile = main_window.nametowidget("{}.number".format(frame_profile_list[idx_profile]))
        string_data_profile = entry_profile.get()
        string_data_profile = string_data_profile.replace(" ", "")
        data_profile = string_data_profile.split(",")

        try:
            data_profile = [float(elem) for elem in data_profile]
        except ValueError:
            messagebox.showerror("Erreur !", "Format d'entrées incorrect.")
            return
        if len(data_profile) != len(max_action):
            messagebox.showerror("Erreur !", "Longueur de chaque profil doit correspondre au nombre de joueurs.")
            return
        
        strat_form.append(data_profile)


def calcul():

    global max_action
    global frame_calcul_list, frame_calcul_list, frame_simu_list

    # Delete old frame from previous executions
    frame_calcul_list = deleteFrames(frame_calcul_list)
    frame_simu_list = deleteFrames(frame_simu_list)

    
    if len(max_action) == 0:
        messagebox.showerror("Erreur !", "Il faut d'abord remplir le nombre d'actions et appuyer sur \"OK\", puis remplir le forme stratégique.")
        return
    
    getData()
    if strat_form == None:
        return
    
    is_somme_nulle = isSommeNulle(max_action, strat_form)
    nash_pur = findNashPur(max_action, strat_form)
    dominated = findDominated(max_action, strat_form)
    dominant = findDominant(max_action, strat_form)
    nash_mixte = None
    if len(max_action) == 2 and max_action[0] == 2 and max_action[1] == 2:
        nash_mixte = findNashMixte(max_action, strat_form)
        string_nash_mixte = [None for idx in range(len(nash_mixte))]
        for player in range(len(nash_mixte)):
            # -1 : Nash Mixte dans [0,1]
            if nash_mixte[player] == -1:
                string_nash_mixte[player] = "[0, 1]"
            # -2 : Pas de Nash Mixte
            elif nash_mixte[player] == -2:
                string_nash_mixte[player] = "Pas de Nash Mixte"
            # 1 < mixte < 2 : Nash Mixte dans [0, mixte-1]
            elif (1 < nash_mixte[player]) and ( nash_mixte[player] < 2):
                string_nash_mixte[player] = "[0, {:.6f}]".format(nash_mixte[player]-1)
            # -1 < mixte < 0 : Nash Mixte dans [-mixte, 1]
            elif (-1 < nash_mixte[player]) and ( nash_mixte[player] < 0):
                string_nash_mixte[player] = "[{:.6f}, 1]".format(-nash_mixte[player])
            # else, on a du Nash mixte "normal"
            else:
                string_nash_mixte[player] = "{:.6f}".format(nash_mixte[player])


    # Print results on the screen
    # Is Somme Nulle
    name_is_somme_nulle = "frame_somme_nulle"
    frame_is_somme_nulle = tk.Frame(name=name_is_somme_nulle, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_is_somme_nulle.grid(row=main_window.grid_size()[1], column=0, columnspan=5, padx=15, pady=5)
    frame_calcul_list.append(name_is_somme_nulle)
    if is_somme_nulle == True:
        text_is_somme_nulle = tk.Label(master=frame_is_somme_nulle, text= "Ce jeux est à somme nulle.", font="bold")
        text_is_somme_nulle.pack()
    elif is_somme_nulle == False:
        text_is_somme_nulle = tk.Label(master=frame_is_somme_nulle, text= "Ce jeux n'est pas à somme nulle.", font="bold")
        text_is_somme_nulle.pack()
    
    # Nash Pur
    name_nash_pur = "frame_nash_pur"
    frame_nash_pur = tk.Frame(name=name_nash_pur, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_nash_pur.grid(row=main_window.grid_size()[1], column=0, columnspan=5, padx=15, pady=5)
    frame_calcul_list.append(name_nash_pur)
    if len(nash_pur) != 0:
        text_nash_pur = tk.Label(master=frame_nash_pur, text= "Profils d'équilibre Nash Pur: {}.".format(convertListToStringToPrint(nash_pur)), font="bold")
        text_nash_pur.pack()
    elif len(nash_pur) == 0:
        text_nash_pur = tk.Label(master=frame_nash_pur, text= "Il n'y a pas d'équilibre Nash Pur.", font="bold")
        text_nash_pur.pack()

    # Dominant et dominé
    name_domination = "frame_domination"
    frame_domination = tk.Frame(name=name_domination, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_domination.grid(row=main_window.grid_size()[1], column=0, columnspan=5, padx=15, pady=5)
    frame_calcul_list.append(name_domination)

    # Montrer les stratégies dominées
    for player, elem in enumerate(dominated):
        if not elem:
            text_dominated = tk.Label(master=frame_domination, text= "Joueur {} : Pas de stratégies dominées.".format(player), font="bold")
            text_dominated.pack()
        else:
            text_dominated = tk.Label(master=frame_domination, text= "Joueur {} : Stratégies dominées : {}".format(player, convertListToStringToPrint(dominated[player])), font="bold")
            text_dominated.pack()

    # Montrer les stratégies dominantes
    for player, elem in enumerate(dominant):
        if not elem:
            text_dominant = tk.Label(master=frame_domination, text= "Joueur {} : Pas de stratégies dominantes.".format(player), font="bold")
            text_dominant.pack()
        else:
            text_dominant = tk.Label(master=frame_domination, text= "Joueur {} : Stratégies dominantes : {}".format(player, convertListToStringToPrint(dominant[player])), font="bold")
            text_dominant.pack()

    # Nash mixte
    if nash_mixte != None:
        name_nash_mixte = "frame_nash_mixte"
        frame_nash_mixte = tk.Frame(name=name_nash_mixte, master=main_window, relief=tk.RAISED, borderwidth=1)
        frame_nash_mixte.grid(row=main_window.grid_size()[1], column=0, columnspan=5, padx=5, pady=15)
        frame_calcul_list.append(name_nash_mixte)

        p1_mixte = string_nash_mixte[0]
        p2_mixte = string_nash_mixte[1]
        text_nash_mixte = tk.Label(master=frame_nash_mixte, text= "Nash mixte : p : {}      q : {}".format(p1_mixte, p2_mixte), font="bold")
        text_nash_mixte.pack()


# Recuperer p et q fourni par l'utilisateur
# Si p=2 ou q=2 --> Jouer la strategie mixte
def getPQ():
    global input_pq

    entry_p = main_window.nametowidget("frame_entry_player_one.number")
    entry_q = main_window.nametowidget("frame_entry_player_two.number")
    string_p = entry_p.get()
    string_q = entry_q.get()


    # Si p ou q n'est pas rempli --> p_mixte ou q_mixte
    if not string_p:
        p_input = 2
    # string_p n'est pas vide
    else:
        try:
            p_input = float(string_p)
        except ValueError:
            messagebox.showerror("Erreur !", "Format d'entrées incorrect.")
            input_pq = [None, None]
            return
        if p_input<0 or p_input>1:
            messagebox.showerror("Erreur !", "Les probs doivent être entre 0 et 1.")
            input_pq = [None, None]
            return
    
    # string_q n'est pas vide
    if not string_q:
        q_input = 2
    else:
        try:
            q_input = float(string_q)
        except ValueError:
            messagebox.showerror("Erreur !", "Format d'entrées incorrect.")
            input_pq = [None, None]
            return
        if q_input<0 or q_input>1:
            messagebox.showerror("Erreur !", "Les probs doivent être entre 0 et 1.")
            input_pq = [None, None]
            return
    input_pq = [p_input, q_input]


# Calculer le Nash mixte pour la simulation
def getNashMixteForSimulation():
    global max_action, strat_form

    nash_mixte = findNashMixte(max_action, strat_form)
    nash_simulation = [None, None] # Liste final pour la simulation, il faut aborder les cas d'exceptions
    for player in range(len(nash_mixte)):
        # mixte = -1 --> N'importe quelle strategie
        if nash_mixte[player] == -1:
            nash_simulation[player] = uniform(0, 1)

        # mixte = -2 --> Pas de Nash Mixte
        # Verifier s'il y a d'un Nash Pur par elimination de strategie
        elif nash_mixte[player] == -2:
            dominant_strict = findDominantStrict(max_action, strat_form)
            # Le joueur actuel n'a pas de strategie dominante stricte
            if dominant_strict[player] == None:
                continue
            other_player = 1 - player
            # On a pas de Nash Pur par elimination de strategie
            if nash_mixte[other_player] != -2:
                # Si dominant = 0 --> action 0 est dominante, donc la prob de choisir 0 c'est 1
                # Si domiant = 1 --> action 1 est dominante, donc la prob de choisir 0 c'est 0
                nash_simulation[player] = 1 - dominant_strict[player]
                nash_simulation[other_player] = uniform(0, 1)
            # On a de Nash Pur par elimination de strategie
            elif nash_mixte[other_player] == -2:
                nash_simulation[player] = 1 - dominant_strict[player]
                profile_dominant = collectProfiles(dominant_strict[player], player, max_action, strat_form)
                if profile_dominant[0][other_player] > profile_dominant[1][other_player]:
                    nash_simulation[other_player] = 1 # Action=0 --> prob=1
                elif profile_dominant[1][other_player] > profile_dominant[0][other_player]:
                    nash_simulation[other_player] = 0 # Action=1 --> prob=0
            
        # 1 < mixte < 2 --> equilibre dans [0, mixte-1]
        elif nash_mixte[player] > 1 and nash_mixte[player] < 2:
            nash_simulation[player] = uniform(0, nash_mixte[player]-1)
        
        # -1 < mixte < 0 --> equilibre dans [-mixte, 1]
        elif nash_mixte[player] > -1 and nash_mixte[player] < 0:
            nash_simulation[player] = uniform(-nash_mixte[player], 1)

        # Cas normal
        else:
            nash_simulation[player] = nash_mixte[player]
    return nash_simulation


# Jouer un coup
def playOneGame(p_input, q_input):
    global strat_form
    assert len(strat_form) == 4, "Il faut avoir 2 joueurs."

    # Generer deux nombres aleatoire
    random_one = uniform(0, 1)
    random_two = uniform(0, 1)

    # Joueur 1 joue
    if (random_one < p_input):
        play_one = 0
    elif (random_one == p_input):
        play_one = randint(0, 1)
    else:
        play_one = 1
    
    # Joueur 2 joue
    if (random_two < q_input):
        play_two = 0
    elif (random_two == q_input):
        play_two = randint(0, 1)
    else:
        play_two = 1
    
    return [play_one, play_two]

# Jouer le jeux pas a pas
def play():
    global max_action, input_pq, score, score_mixte, strat_form, nash_simulation, frame_simu_list

    p_old = input_pq[0]
    q_old = input_pq[1]
    
    # Recuperer les entrees p q depuis utilisateur
    getPQ()
    if input_pq == [None, None]:
        return

    new_nash_simulation = getNashMixteForSimulation()
    for player in range(len(input_pq)):
        if input_pq[player] == 2:
            input_pq[player] = new_nash_simulation[player]

    p_input = input_pq[0]
    q_input = input_pq[1]


    # Jouer un coup
    play_one, play_two = playOneGame(p_input, q_input)
    gain = getElemFromIndex([play_one, play_two], max_action, strat_form)

    # Verifier si c'est la meme configuration strat_form et p q
    # Si oui, on continue le jeux en utilisant la score et p_mixte, q_mixte precedente
    if (p_old == p_input) and (q_old == q_input):

        # Jouer un coup selon la strategie mixte
        play_mixte_one, play_mixte_two = playOneGame(nash_simulation[0], nash_simulation[1])
        gain_mixte = getElemFromIndex([play_mixte_one, play_mixte_two], max_action, strat_form)

        score[0] += gain[0]
        score[1] += gain[1]
        score_mixte[0] += gain_mixte[0]
        score_mixte[1] += gain_mixte[1]

    # Sinon, on redemarrer le jeux avec la score [0, 0]
    else:
        # Jouer un coup selon la strategie mixte
        nash_simulation = list(new_nash_simulation)
        play_mixte_one, play_mixte_two = playOneGame(nash_simulation[0], nash_simulation[1])
        gain_mixte = getElemFromIndex([play_mixte_one, play_mixte_two], max_action, strat_form)

        score[0] = gain[0]
        score[1] = gain[1]
        score_mixte[0] = gain_mixte[0]
        score_mixte[1] = gain_mixte[1]

    list_frame_simulation = set(["frame_text_gain_mixte", "frame_text_gain_mixte_player_one", "frame_text_gain_mixte_player_two", "frame_text_gain_utilisateur", "frame_text_gain_uti_one", "frame_text_gain_uti_two"])
    if set(list_frame_simulation) <= set(frame_simu_list):
        text_gain_mixte_player_one = main_window.nametowidget("frame_text_gain_mixte_player_one.number")
        text_gain_mixte_player_two = main_window.nametowidget("frame_text_gain_mixte_player_two.number")
        text_gain_uti_one = main_window.nametowidget("frame_text_gain_uti_one.number")
        text_gain_uti_two = main_window.nametowidget("frame_text_gain_uti_two.number")

        text_gain_mixte_player_one.config(text="{}".format(score_mixte[0]))
        text_gain_mixte_player_two.config(text="{}".format(score_mixte[1]))
        text_gain_uti_one.config(text="{}".format(score[0]))
        text_gain_uti_two.config(text="{}".format(score[1]))

    else:
        row_simulation_mixte = main_window.grid_size()[1]
        # Frame texte : Gain Nash Mixte
        name_frame_text_gain_mixte = "frame_text_gain_mixte"
        frame_text_gain_mixte = tk.Frame(name=name_frame_text_gain_mixte, master=main_window, relief=tk.FLAT, borderwidth=1)
        frame_text_gain_mixte.grid(row=row_simulation_mixte, column=0, padx=5, pady=5)
        frame_simu_list.append(name_frame_text_gain_mixte)
        text_gain_mixte = tk.Label(master=frame_text_gain_mixte, text= "Gain Mixte")
        text_gain_mixte.pack()

        # Frame texte : Gain Mixte pour joueur 1
        name_frame_text_gain_mixte_player_one = "frame_text_gain_mixte_player_one"
        frame_text_gain_mixte_player_one = tk.Frame(name=name_frame_text_gain_mixte_player_one, master=main_window, relief=tk.RAISED, borderwidth=1)
        frame_text_gain_mixte_player_one.grid(row=row_simulation_mixte, column=1, padx=5, pady=5)
        frame_simu_list.append(name_frame_text_gain_mixte_player_one)
        text_gain_mixte_player_one = tk.Label(name="number", master=frame_text_gain_mixte_player_one, text= "{}".format(score_mixte[0]))
        text_gain_mixte_player_one.pack()

        # Frame texte : Gain Mixte pour joueur 2
        name_frame_text_gain_mixte_player_two = "frame_text_gain_mixte_player_two"
        frame_text_gain_mixte_player_two = tk.Frame(name=name_frame_text_gain_mixte_player_two, master=main_window, relief=tk.RAISED, borderwidth=1)
        frame_text_gain_mixte_player_two.grid(row=row_simulation_mixte, column=5, padx=5, pady=5)
        frame_simu_list.append(name_frame_text_gain_mixte_player_two)
        text_gain_mixte_player_two = tk.Label(name="number", master=frame_text_gain_mixte_player_two, text= "{}".format(score_mixte[1]))
        text_gain_mixte_player_two.pack()



        row_simulation_utilisateur = main_window.grid_size()[1]
        # Frame texte : Gain Utilisateur
        name_frame_text_gain_utilisateur = "frame_text_gain_utilisateur"
        frame_text_gain_utilisateur = tk.Frame(name=name_frame_text_gain_utilisateur, master=main_window, relief=tk.FLAT, borderwidth=1)
        frame_text_gain_utilisateur.grid(row=row_simulation_utilisateur, column=0, padx=5, pady=5)
        frame_simu_list.append(name_frame_text_gain_utilisateur)
        frame_text_gain_utilisateur = tk.Label(master=frame_text_gain_utilisateur, text= "Gain d'entrees d'utilisateur")
        frame_text_gain_utilisateur.pack()

        # Frame texte : Gain Utilisateur pour joueur 1
        name_frame_text_gain_uti_one = "frame_text_gain_uti_one"
        frame_text_gain_uti_one = tk.Frame(name=name_frame_text_gain_uti_one, master=main_window, relief=tk.RAISED, borderwidth=1)
        frame_text_gain_uti_one.grid(row=row_simulation_utilisateur, column=1, padx=5, pady=5)
        frame_simu_list.append(name_frame_text_gain_uti_one)
        text_gain_uti_one = tk.Label(name="number", master=frame_text_gain_uti_one, text= "{}".format(score[0]))
        text_gain_uti_one.pack()

        # Frame texte : Gain Utilisateur pour joueur 2
        name_frame_text_gain_uti_two = "frame_text_gain_uti_two"
        frame_text_gain_uti_two = tk.Frame(name=name_frame_text_gain_uti_two, master=main_window, relief=tk.RAISED, borderwidth=1)
        frame_text_gain_uti_two.grid(row=row_simulation_utilisateur, column=5, padx=5, pady=5)
        frame_simu_list.append(frame_text_gain_uti_two)
        text_gain_uti_two = tk.Label(name="number", master=frame_text_gain_uti_two, text= "{}".format(score[1]))
        text_gain_uti_two.pack()


# Simuler le jeux sur 1000 iterations
def simulate():
    global max_action, input_pq, strat_form, frame_simu_list, nash_simulation
    
    # Recuperer les entrees p q depuis utilisateur
    getPQ()
    if input_pq == [None, None]:
        return


    nash_simulation = getNashMixteForSimulation()
    for player in range(len(input_pq)):
        if input_pq[player] == 2:
            input_pq[player] = nash_simulation[player]

    p_input = input_pq[0]
    q_input = input_pq[1]

    # Jouer le jeux sur 1000 coup
    score_game = [0, 0]
    score_game_mixte = [0, 0]
    for game in range(1000):
        # Jouer un coup
        play_one, play_two = playOneGame(p_input, q_input)
        gain = getElemFromIndex([play_one, play_two], max_action, strat_form)

        # Jouer un coup selon la strategie mixte
        play_mixte_one, play_mixte_two = playOneGame(nash_simulation[0], nash_simulation[1])
        gain_mixte = getElemFromIndex([play_mixte_one, play_mixte_two], max_action, strat_form)

        score_game[0] += gain[0]
        score_game[1] += gain[1]
        score_game_mixte[0] += gain_mixte[0]
        score_game_mixte[1] += gain_mixte[1]


    list_frame_simulation = set(["frame_text_gain_mixte", "frame_text_gain_mixte_player_one", "frame_text_gain_mixte_player_two", "frame_text_gain_utilisateur", "frame_text_gain_uti_one", "frame_text_gain_uti_two"])
    if set(list_frame_simulation) <= set(frame_simu_list):
        text_gain_mixte_player_one = main_window.nametowidget("frame_text_gain_mixte_player_one.number")
        text_gain_mixte_player_two = main_window.nametowidget("frame_text_gain_mixte_player_two.number")
        text_gain_uti_one = main_window.nametowidget("frame_text_gain_uti_one.number")
        text_gain_uti_two = main_window.nametowidget("frame_text_gain_uti_two.number")

        text_gain_mixte_player_one.config(text="{}".format(score_game_mixte[0]))
        text_gain_mixte_player_two.config(text="{}".format(score_game_mixte[1]))
        text_gain_uti_one.config(text="{}".format(score_game[0]))
        text_gain_uti_two.config(text="{}".format(score_game[1]))

    else:
        row_simulation_mixte = main_window.grid_size()[1]
        # Frame texte : Gain Nash Mixte
        name_frame_text_gain_mixte = "frame_text_gain_mixte"
        frame_text_gain_mixte = tk.Frame(name=name_frame_text_gain_mixte, master=main_window, relief=tk.FLAT, borderwidth=1)
        frame_text_gain_mixte.grid(row=row_simulation_mixte, column=0, padx=5, pady=5)
        frame_simu_list.append(name_frame_text_gain_mixte)
        text_gain_mixte = tk.Label(master=frame_text_gain_mixte, text= "Gain Mixte")
        text_gain_mixte.pack()

        # Frame texte : Gain Mixte pour joueur 1
        name_frame_text_gain_mixte_player_one = "frame_text_gain_mixte_player_one"
        frame_text_gain_mixte_player_one = tk.Frame(name=name_frame_text_gain_mixte_player_one, master=main_window, relief=tk.RAISED, borderwidth=1)
        frame_text_gain_mixte_player_one.grid(row=row_simulation_mixte, column=1, padx=5, pady=5)
        frame_simu_list.append(name_frame_text_gain_mixte_player_one)
        text_gain_mixte_player_one = tk.Label(name="number", master=frame_text_gain_mixte_player_one, text= "{}".format(score_game_mixte[0]))
        text_gain_mixte_player_one.pack()

        # Frame texte : Gain Mixte pour joueur 2
        name_frame_text_gain_mixte_player_two = "frame_text_gain_mixte_player_two"
        frame_text_gain_mixte_player_two = tk.Frame(name=name_frame_text_gain_mixte_player_two, master=main_window, relief=tk.RAISED, borderwidth=1)
        frame_text_gain_mixte_player_two.grid(row=row_simulation_mixte, column=5, padx=5, pady=5)
        frame_simu_list.append(name_frame_text_gain_mixte_player_two)
        text_gain_mixte_player_two = tk.Label(name="number", master=frame_text_gain_mixte_player_two, text= "{}".format(score_game_mixte[1]))
        text_gain_mixte_player_two.pack()



        row_simulation_utilisateur = main_window.grid_size()[1]
        # Frame texte : Gain Utilisateur
        name_frame_text_gain_utilisateur = "frame_text_gain_utilisateur"
        frame_text_gain_utilisateur = tk.Frame(name=name_frame_text_gain_utilisateur, master=main_window, relief=tk.FLAT, borderwidth=1)
        frame_text_gain_utilisateur.grid(row=row_simulation_utilisateur, column=0, padx=5, pady=5)
        frame_simu_list.append(name_frame_text_gain_utilisateur)
        frame_text_gain_utilisateur = tk.Label(master=frame_text_gain_utilisateur, text= "Gain d'entrees d'utilisateur")
        frame_text_gain_utilisateur.pack()

        # Frame texte : Gain Utilisateur pour joueur 1
        name_frame_text_gain_uti_one = "frame_text_gain_uti_one"
        frame_text_gain_uti_one = tk.Frame(name=name_frame_text_gain_uti_one, master=main_window, relief=tk.RAISED, borderwidth=1)
        frame_text_gain_uti_one.grid(row=row_simulation_utilisateur, column=1, padx=5, pady=5)
        frame_simu_list.append(name_frame_text_gain_uti_one)
        text_gain_uti_one = tk.Label(name="number", master=frame_text_gain_uti_one, text= "{}".format(score_game[0]))
        text_gain_uti_one.pack()

        # Frame texte : Gain Utilisateur pour joueur 2
        name_frame_text_gain_uti_two = "frame_text_gain_uti_two"
        frame_text_gain_uti_two = tk.Frame(name=name_frame_text_gain_uti_two, master=main_window, relief=tk.RAISED, borderwidth=1)
        frame_text_gain_uti_two.grid(row=row_simulation_utilisateur, column=5, padx=5, pady=5)
        frame_simu_list.append(frame_text_gain_uti_two)
        text_gain_uti_two = tk.Label(name="number", master=frame_text_gain_uti_two, text= "{}".format(score_game[1]))
        text_gain_uti_two.pack()

def doSimulation():
    global max_action, frame_calcul_list, frame_calcul_list, frame_simu_list

    # Delete old frame from previous executions
    frame_calcul_list = deleteFrames(frame_calcul_list)
    frame_simu_list = deleteFrames(frame_simu_list)

    if len(max_action) == 0:
        messagebox.showerror("Erreur !", "Il faut d'abord remplir le nombre d'actions et appuyer sur \"OK\", puis remplir le forme stratégique.")
        return


    getData()
    if strat_form == None:
        return
    # Vérifier si c'est le jeux de 2 joueurs, 2 actions par joueur
    if len(max_action) != 2 or max_action[0] != 2 or max_action[1] != 2 or len(strat_form) != 4:
        messagebox.showerror("Erreur !", "Simulation ne marche que sur le jeux de 2 joueurs, 2 actions par joueurs.")
        return
    
    nash_mixte = findNashMixte(max_action, strat_form)

    string_nash_mixte = [None for idx in range(len(nash_mixte))]
    dominant_strict = findDominantStrict(max_action, strat_form)

    # Recuperer des strings pour afficher a l'ecran
    for player in range(len(nash_mixte)):
        # -1 : Nash Mixte dans [0,1]
        if nash_mixte[player] == -1:
            string_nash_mixte[player] = "[0, 1]"
        # -2 : Pas de Nash Mixte
        elif nash_mixte[player] == -2:
            string_nash_mixte[player] = "None"
        # 1 < mixte < 2 : Nash Mixte dans [0, mixte-1]
        elif (1 < nash_mixte[player]) and ( nash_mixte[player] < 2):
            string_nash_mixte[player] = "[0, {:.6f}]".format(nash_mixte[player]-1)
        # -1 < mixte < 0 : Nash Mixte dans [-mixte, 1]
        elif (-1 < nash_mixte[player]) and ( nash_mixte[player] < 0):
            string_nash_mixte[player] = "[{:.6f}, 1]".format(-nash_mixte[player])
        # else, on a du Nash mixte "normal"
        else:
            string_nash_mixte[player] = "{:.6f}".format(nash_mixte[player])



    row_nash_mixte = main_window.grid_size()[1]
    # Frame texte : Nash Mixte
    name_frame_text_nash_mixte = "frame_text_nash_mixte"
    frame_text_nash_mixte = tk.Frame(name=name_frame_text_nash_mixte, master=main_window, relief=tk.FLAT, borderwidth=1)
    frame_text_nash_mixte.grid(row=row_nash_mixte, column=0, padx=5, pady=5)
    frame_simu_list.append(name_frame_text_nash_mixte)
    text_nash_mixte = tk.Label(master=frame_text_nash_mixte, text= "Nash Mixte")
    text_nash_mixte.pack()

    # Frame texte : Nash Mixte joueur 1
    name_frame_text_nash_player_one = "frame_text_nash_player_one"
    frame_text_nash_player_one = tk.Frame(name=name_frame_text_nash_player_one, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_text_nash_player_one.grid(row=row_nash_mixte, column=1, padx=5, pady=5)
    frame_simu_list.append(name_frame_text_nash_player_one)
    text_nash_player_one = tk.Label(master=frame_text_nash_player_one, text= "p = {}".format(string_nash_mixte[0]), font="bold")
    text_nash_player_one.pack()

    # Frame texte : Nash Mixte joueur 2
    name_frame_text_nash_player_two = "frame_text_nash_player_two"
    frame_text_nash_player_two = tk.Frame(name=name_frame_text_nash_player_two, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_text_nash_player_two.grid(row=row_nash_mixte, column=5, padx=5, pady=5)
    frame_simu_list.append(name_frame_text_nash_player_two)
    text_nash_player_two = tk.Label(master=frame_text_nash_player_two, text= "q = {}".format(string_nash_mixte[1]), font="bold")
    text_nash_player_two.pack()


    row_domination = main_window.grid_size()[1]
    # Frame texte : Domination stricte
    name_frame_text_domiation = "frame_text_domination"
    frame_text_domiation = tk.Frame(name=name_frame_text_domiation, master=main_window, relief=tk.FLAT, borderwidth=1)
    frame_text_domiation.grid(row=row_domination, column=0, padx=5, pady=5)
    frame_simu_list.append(name_frame_text_domiation)
    text_domiation = tk.Label(master=frame_text_domiation, text= "Action dominante stricte")
    text_domiation.pack()

    # Frame texte : Domination stricte joueur 1
    name_frame_text_domiation_player_one = "frame_text_domiation_player_one"
    frame_text_domiation_player_one = tk.Frame(name=name_frame_text_domiation_player_one, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_text_domiation_player_one.grid(row=row_domination, column=1, padx=5, pady=5)
    frame_simu_list.append(name_frame_text_domiation_player_one)
    text_domiation_player_one = tk.Label(master=frame_text_domiation_player_one, text= "{}".format(dominant_strict[0]), font="bold")
    text_domiation_player_one.pack()

    # Frame texte : Domination stricte joueur 2
    name_frame_text_domiation_player_two = "frame_text_domiation_player_two"
    frame_text_domiation_player_two = tk.Frame(name=name_frame_text_domiation_player_two, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_text_domiation_player_two.grid(row=row_domination, column=5, padx=5, pady=5)
    frame_simu_list.append(name_frame_text_domiation_player_two)
    text_domiation_player_two = tk.Label(master=frame_text_domiation_player_two, text= "{}".format(dominant_strict[1]), font="bold")
    text_domiation_player_two.pack()


    row_input = main_window.grid_size()[1]
    # Frame texte : Entrees d'utilisateur
    name_frame_text_input = "frame_text_input"
    frame_text_input = tk.Frame(name=name_frame_text_input, master=main_window, relief=tk.FLAT, borderwidth=1)
    frame_text_input.grid(row=row_input, column=0, padx=5, pady=5)
    frame_simu_list.append(name_frame_text_input)
    text_input = tk.Label(master=frame_text_input, text= "Entrées d'utilisateur")
    text_input.pack()

    # Frame d'entrees pour p du joueur 1
    name_frame_entry_player_one = "frame_entry_player_one"
    frame_entry_player_one = tk.Frame(name=name_frame_entry_player_one, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_entry_player_one.grid(row=row_input, column=1, padx=5, pady=5)
    frame_simu_list.append(name_frame_entry_player_one)
    entry_player_one = tk.Entry(name="number", master=frame_entry_player_one,fg="black", bg="white", width=10)
    entry_player_one.pack()

    # Frame d'entrees pour q du joueur 2
    name_frame_entry_player_two = "frame_entry_player_two"
    frame_entry_player_two = tk.Frame(name=name_frame_entry_player_two, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_entry_player_two.grid(row=row_input, column=5, padx=5, pady=5)
    frame_simu_list.append(name_frame_entry_player_two)
    entry_player_two = tk.Entry(name="number", master=frame_entry_player_two,fg="black", bg="white", width=10)
    entry_player_two.pack()


    # Button to generate strategic form input
    name_frame_button_play = "frame_button_play"
    frame_button_play = tk.Frame(name=name_frame_button_play, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_button_play.grid(row=row_domination, column=2, columnspan=3, padx=5, pady=5)
    frame_simu_list.append(name_frame_button_play)
    button_play = tk.Button(master=frame_button_play, text ="Jouer", command = play)
    button_play.pack()

    # Button to generate strategic form input
    name_frame_button_stimulate = "frame_button_stimulate"
    frame_button_stimulate = tk.Frame(name=name_frame_button_stimulate, master=main_window, relief=tk.RAISED, borderwidth=1)
    frame_button_stimulate.grid(row=row_input, column=2, columnspan=3, padx=5, pady=5)
    frame_simu_list.append(name_frame_button_stimulate)
    button_stimulate = tk.Button(master=frame_button_stimulate, text ="Simuler", command = simulate)
    button_stimulate.pack()


# Main window
main_window = tk.Tk()
main_window.title("Projet Théorie des Jeux - NGUYEN Van Lam")

# Text frame for max actions per player
frame_text_actions_per_player = tk.Frame(master=main_window, relief=tk.FLAT, borderwidth=1)
frame_text_actions_per_player.grid(row=0, column=0, columnspan=3, padx=5, pady=15)
text_actions_per_player = tk.Label(master=frame_text_actions_per_player, text= "Nombre d'actions pour chaque joueurs:\n(Par ex. 2,3,3,2)")
text_actions_per_player.pack()

# Entry field for max actions per player
frame_entry_actions_per_player = tk.Frame(master=main_window, relief=tk.RAISED, borderwidth=1)
frame_entry_actions_per_player.grid(row=0, column=3, padx=5, pady=15)
entry_actions_per_player = tk.Entry(master=frame_entry_actions_per_player,fg="black", bg="white", width=10)
entry_actions_per_player.bind("<Return>", (lambda event: generateMatrix()))
entry_actions_per_player.pack()

# Button to generate strategic form input
frame_button_action = tk.Frame(master=main_window, relief=tk.RAISED, borderwidth=1)
frame_button_action.grid(row=0, column=4, padx=5, pady=15)
button_actions_per_player = tk.Button(master=frame_button_action, text ="OK", command = generateMatrix)
button_actions_per_player.pack()

# Button to calculate the game (isSommeNulle, nashPur, nashMixte, Dominant...)
frame_button_calcul = tk.Frame(master=main_window, relief=tk.RAISED, borderwidth=1)
frame_button_calcul.grid(row=1, column=0, padx=5, pady=15)
button_calcul = tk.Button(master=frame_button_calcul, text ="Calculs", command = calcul)
button_calcul.pack()

# Button to simulate the game (for 2 players only)
frame_button_simulation = tk.Frame(master=main_window, relief=tk.RAISED, borderwidth=1)
frame_button_simulation.grid(row=1, column=1, padx=5, pady=15)
button_simulation = tk.Button(master=frame_button_simulation, text ="Simulation", command = doSimulation)
button_simulation.pack()

main_window.mainloop()