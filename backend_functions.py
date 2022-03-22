import numpy as np


# Return a profile based list of index
def getElemFromIndex(index_list, max_action, strat_form):
    assert len(max_action) == len(index_list), "The number of players must be consistent in max_action and index"
    # Loop through index list to calculate the corresponding profile
    num_profile = 0
    for idx in range(len(index_list)):
        assert index_list[idx] < max_action[idx], "Index must be smaller than maximum number of actions."
        
        multiplier = int(np.prod(max_action[idx+1:])) # On the last index, it returns 1, which is right and I dont have to handle the exception
        num_profile += index_list[idx] * multiplier
    return strat_form[num_profile]



# From an index of the strategic form (num_profile), return a list of index corresponding to a profile
def getIndex(num_profile, max_action):
    index_list = []
    for idx in range(len(max_action)):
        multiplier = int(np.prod(max_action[idx+1:]))
        profile_idx = int(num_profile / multiplier)
        num_profile -= profile_idx * multiplier
        index_list.append(profile_idx)
    return index_list


def isSommeNulle(max_action, strat_form):
    assert len(max_action) == len(strat_form[0]), "Number of players does not match"
    for profile in strat_form:
        if sum(profile) != 0:
            return False
    return True


# Check if a profile is Pure Nash Equilibrium
def isNashPur(num_profile, max_action, strat_form):
    index_list = getIndex(num_profile, max_action)
    current_profile = getElemFromIndex(index_list, max_action, strat_form)

    # Loop over each neighbor profile
    for player, max_action_per_player in enumerate(max_action):
        for action_idx in range(max_action_per_player):

            # Skip the current action of current player (duplicate)
            if (index_list[player] == action_idx):
                continue

            # Collect profile of the neighbor that the current profile wants to compare
            neighbor_index_list = list(index_list)
            neighbor_index_list[player] = action_idx
            profile_neighbor = getElemFromIndex(neighbor_index_list, max_action, strat_form)

            # Compare
            if profile_neighbor[player] > current_profile[player]:
                return False
    
    # Return True if find no better solution
    return True


# Find Nash pur of a strategic form
def findNashPur(max_action, strat_form):
    nashPur = []

    # Iterate over each profile to find Nash Pur
    for num_profile, elem in enumerate(strat_form):
        if isNashPur(num_profile, max_action, strat_form):
            index_profile = getIndex(num_profile, max_action)
            nashPur.append(index_profile)
    return nashPur


# Generate all possible index of a strategic form
def generateIndex(max_action):
    # Calculate the length of strategic form
    len_strat_form = 1
    for elem in max_action:
        len_strat_form *= elem
    
    # Create all possible profile index
    all_index_profile = []
    for num_profile in range(len_strat_form):
        idx_profile = getIndex(num_profile, max_action)
        all_index_profile.append(idx_profile)
    return all_index_profile


# Collect all profiles of a player along their action
def collectProfiles(action, player, max_action, strat_form):
    assert player <= len(max_action), "Number of player does not match."
    assert action <= max_action[player], "ACtion does not match."

    # Generate all possible profile index
    all_index_profile = generateIndex(max_action)

    # Find all profiles by fixing the action of the current player
    current_action_profile = []
    for idx_profile in all_index_profile:
        if idx_profile[player] == action:
            profile = getElemFromIndex(idx_profile, max_action, strat_form)
            current_action_profile.append(profile) # I can append idx_profile for index testing
    return current_action_profile


# Trouver les stratégies dominées
def findDominated(max_action, strat_form):
    # Initialize the list to save result
    # Length: Number of players
    dominated = [[] for i in range(len(max_action))]

    for player, max_action_per_player in enumerate(max_action):
        for action_idx in range(max_action_per_player):

            # Get all profiles for the current action of the current player
            current_action_profile = collectProfiles(action_idx, player, max_action, strat_form)

            # Get neighbor profiles by changing the current action (of the same player)
            for neighbor_action_idx in range(max_action_per_player):
                # Skip the current action (duplicate)
                if neighbor_action_idx == action_idx:
                    continue
                    
                neighbor_action_profile = collectProfiles(neighbor_action_idx, player, max_action, strat_form)
                flag_dominated = True
                flag_more = False # A flag to make sure there are AT LEAST one > or < in weakly domination

                # Compare the current action to neighbor action
                for idx, profile in enumerate(current_action_profile):
                    # Check for dominated condition
                    if current_action_profile[idx][player] > neighbor_action_profile[idx][player]:
                        flag_dominated = False
                        break
                    if current_action_profile[idx][player] < neighbor_action_profile[idx][player]:
                        flag_more = True
                
                if (flag_dominated == True) and (flag_more == True):
                    dominated[player].append(action_idx)
                    break # If find a dominating stragy, break the loop for the next "current action"

    return dominated


# Trouver les stratégies dominantes
def findDominant(max_action, strat_form):
    # Initialize the list to save result
    # Length: Number of players
    dominant = [[] for i in range(len(max_action))]
    for player, max_action_per_player in enumerate(max_action):
        for action_idx in range(max_action_per_player):

            # Get all profiles for the current action of the current player
            current_action_profile = collectProfiles(action_idx, player, max_action, strat_form)
            flag_dominant = True # Outside the "neighbor" loop

            # Get neighbor profiles by changing the current action (of the same player)
            for neighbor_action_idx in range(max_action_per_player):
                # Skip the current action (duplicate)
                if neighbor_action_idx == action_idx:
                    continue
                    
                neighbor_action_profile = collectProfiles(neighbor_action_idx, player, max_action, strat_form)
                flag_more = False # A flag to make sure there are AT LEAST one > or < in weakly domination

                # Compare the current action to neighbor action
                for idx, profile in enumerate(current_action_profile):
                    # Check for dominated condition
                    if current_action_profile[idx][player] < neighbor_action_profile[idx][player]:
                        flag_dominant = False
                        break
                    if current_action_profile[idx][player] > neighbor_action_profile[idx][player]:
                        flag_more = True
                
                # Breaking condition for the next "current action"
                if (flag_dominant == False) or (flag_more == False):
                    break
                
            if (flag_dominant == True) and (flag_more == True):
                dominant[player].append(action_idx)

    return dominant


# Trouver les stratégies dominantes strictes
def findDominantStrict(max_action, strat_form):
    # Initialize the list to save result
    # Length: Number of players
    dominant_strict = [None for i in range(len(max_action))]
    for player, max_action_per_player in enumerate(max_action):
        for action_idx in range(max_action_per_player):

            # Get all profiles for the current action of the current player
            current_action_profile = collectProfiles(action_idx, player, max_action, strat_form)
            flag_dominant_strict = True # Outside the "neighbor" loop

            # Get neighbor profiles by changing the current action (of the same player)
            for neighbor_action_idx in range(max_action_per_player):
                # Skip the current action (duplicate)
                if neighbor_action_idx == action_idx:
                    continue
                    
                neighbor_action_profile = collectProfiles(neighbor_action_idx, player, max_action, strat_form)

                # Compare the current action to neighbor action
                for idx, profile in enumerate(current_action_profile):
                    # Check for dominated condition
                    if current_action_profile[idx][player] <= neighbor_action_profile[idx][player]:
                        flag_dominant_strict = False
                        break
                
                # Breaking condition for the next "current action"
                if (flag_dominant_strict == False):
                    break
                
            if (flag_dominant_strict == True):
                dominant_strict[player] = action_idx
                break

    return dominant_strict


# Trouver Nash Mixte pour 2 joueurs, 2 actions par joueur
# Return value:
# p = -1 --> equilibre = [0, 1] # N'importe quelle valeur
# p = -2 --> Pas d'equilibre Nash
# 1 < p < 2 --> equilibre dans [0, p-1]
# -1 < p < 0 --> equilibre dans [-p, 1]
def findNashMixte(max_action, strat_form):
    assert len(max_action) == 2, "Only two players are allowed."
    assert (max_action[0] == 2) and (max_action[1] == 2), "Only two actions per player are allowed."
    assert len(strat_form) == 4, "Strategic form does not match."


    # Cas d'exception: On trouve une (des) stratégie dominante stricte
    dominant_strict = findDominantStrict(max_action, strat_form)

    for player, action_dominant in enumerate(dominant_strict):
        # Pas de domination stricte, continue
        if action_dominant == None:
            continue
        # S'il y a la domiance stricte
        else:
            # Trouver l'action dominante d'un joueur
            if player == 0:
                p_mixte = -2
            if player == 1:
                q_mixte = -2

            # Recuperer les profils de cette action dominante
            profile_dominant = collectProfiles(action_dominant, player, max_action, strat_form)
            assert len(profile_dominant) == 2, "Hmm... Something is not right."
            for other_player in range(len(max_action)):
                if other_player == player:
                    continue
                if profile_dominant[0][other_player] == profile_dominant[1][other_player]:
                    if other_player == 0:
                        p_mixte = -1
                    if other_player == 1:
                        q_mixte = -1
                elif profile_dominant[0][other_player] != profile_dominant[1][other_player]:
                    if other_player == 0:
                        p_mixte = -2
                    if other_player == 1:
                        q_mixte = -2
            return [p_mixte, q_mixte]


    # Calcul du Nash Mix, s'il y a ni domination stricte

    # Cas d'exception: p = 0/0 ou q = 0/0
    # p = 0/0 --> p in [0,1]
    numerator_p_mixte = strat_form[3][1] - strat_form[2][1]
    denominator_p_mixte = strat_form[0][1] - strat_form[2][1] - strat_form[1][1] + strat_form[3][1]
    if (numerator_p_mixte == 0) and (denominator_p_mixte == 0):
        p_mixte = -1
    else:
        # Sinon, calculer p_mixte
        p_mixte = numerator_p_mixte / denominator_p_mixte
    
    # q = 0/0 --> q in [0,1]
    numerator_q_mixte = strat_form[3][0] - strat_form[1][0]
    denominator_q_mixte = strat_form[0][0] - strat_form[2][0] - strat_form[1][0] + strat_form[3][0]
    if (numerator_q_mixte == 0) and (denominator_q_mixte == 0):
        q_mixte = -1
    else:
        # Sinon, calculer q_mixte
        q_mixte = numerator_q_mixte / denominator_q_mixte

    # Nash mix si p_mixte=1 et q_mixte dans (0,1)

    # Si p_mixte == 0 ou 1
    if (p_mixte == 0 or p_mixte == 1) and (q_mixte>0 and q_mixte<1):
        # Verifier si q_mixte est dans (0, q_mixte) ou (q_mixte, 1)
        # Si q > nombre
        if (numerator_q_mixte > 0) and (denominator_q_mixte > 0):
            if p_mixte == 0:
                q_mixte = q_mixte + 1
            elif p_mixte == 1:
                q_mixte = -q_mixte
        # Si q < nombre
        elif (numerator_q_mixte < 0) and (denominator_q_mixte < 0):
            if p_mixte == 0:
                q_mixte = -q_mixte
            elif p_mixte == 1:
                q_mixte = q_mixte + 1
        else:
            print(p_mixte, ", ", q_mixte)
            print("Uncatched exception 1")

    # Si q_mixte == 0 ou 1
    elif (q_mixte == 0 or q_mixte == 1) and (p_mixte>0 and p_mixte<1):
        # Verifier si p_mixte est dans (0, p_mixte) ou (p_mixte, 1)
        # Si p > nombre
        if (numerator_p_mixte > 0) and (denominator_p_mixte > 0):
            if q_mixte == 0:
                p_mixte = p_mixte + 1
            elif q_mixte == 1:
                p_mixte = -p_mixte
        # Si p < nombre
        elif (numerator_p_mixte < 0) and (denominator_p_mixte < 0):
            if q_mixte == 0:
                p_mixte = -p_mixte
            elif q_mixte == 1:
                p_mixte = p_mixte + 1
        else:
            print(p_mixte, ", ", q_mixte)
            print("Uncatched exception 2")

    return [p_mixte, q_mixte]