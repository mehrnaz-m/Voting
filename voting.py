# written by mehrnaz miri

def generate_preferences(values):

    """
    inputs a set of numerical values that the agents have for the different alternatives and outputs a preference profile.

    PARAMETERS
    -----------
    values: 
        The input values to the generate_preferences function is a worksheet corresponding to an xlsx file.

    RETURNS
    -----------
        The output (the return) of the generate_preferences function is a dictionary where the keys are the agents and the values are lists that correspond to the preference orderings of those agents.
    """

    preference_profile = {}  # creating an empty dictionary for preferences
    agent_number = 1

    for agents in values.iter_rows(min_row=1, values_only=True):

        alternative_valuations = list(agents)
        alternatives_with_valuation = list(zip(range(1, len(alternative_valuations) + 1), alternative_valuations))  # creating a list of alternatives with their valuation
        alternatives_with_valuation.sort(key=lambda x: (x[1], x[0]), reverse=True)  # sorting the previous list so that the most prefered is first, and so on
        preferences = [alternative[0] for alternative in alternatives_with_valuation]  # creating a list of alternatives only
        preference_profile[agent_number] = preferences   # putting the alternative in a list alongside with the agent number corresponding to it
        agent_number += 1

    return (preference_profile)


def dictatorship(preferences, agent):
    
    """
    An agent is selected, and the winner is the alternative that this agent ranks first.

    PARAMETERS
    -----------
    preferences: (dict)
        A preference profile represented by a dictionary.

    agent: (int)
        an integer corresponding to an agent.

    RETURNS
    -----------
    The return of the function is the winner.
    """

    try: 
        agent = int(agent)
        if agent not in preferences:  # error handling in case the inputted integer does not correspond to an agent
            raise KeyError("input agent is not in preferences")
        else:
            dictators_preference = preferences[agent]
            winner = dictators_preference[0]
            return (winner)
    except KeyError as ke:
        print(f"ERROR HAS OCCURED: {ke}")
    except Exception as exp:
        print(f"ERROR HAS OCCURED: {exp}")


def scoring_rule(preferences, score_vector, tie_break):
    
    """
    For every agent, the function assigns the highest score in the scoring vector to the most preferred alternative of the agent,
    the second highest score to the second most preferred alternative of the agent and so on,
    and the lowest score to the least preferred alternative of the agent. In the end, it returns the alternative with the highest total score,
    using the tie-breaking option to distinguish between alternatives with the same score.

    PARAMETERS
    -----------
    preferences: (dict)
        A preference profile represented by a dictionary.

    score_vector: (list)
        a score vector of length m, i.e., equal to the number of alternatives, i.e., a list of length m containing positive floating numbers.

    tie_break:
        an option for the tie-breaking among possible winners.
        We will consider the following three tie-breaking rules. Here, we assume that the alternatives are represented by integers.
            max: Among the possible winning alternatives, select the one with the highest number.
            min: Among the possible winning alternatives, select the one with the lowest number.
            agent : Among the possible winning alternatives, select the one that agent ranks the highest in his/her preference ordering. 

    RETURNS
    -----------
    it returns the alternative with the highest total score, using the tie-breaking option to distinguish between alternatives with the 
    same score.
    """

    try:  # error-handling code for the case when the length of the scoring vector is not m
        if len(score_vector) != len(preferences[1]):
            raise ValueError("Incorrect input")
    except Exception as exp:
        print(exp)
        return False
    
    else:
        score_vector.sort(reverse=True)  # sorting the score vector so that the highest score is first
        agent_preference_scores = {}  # an empty dictionary to keep track of each score for each alternative
        total_scores = {}  # an empty dictionary to add each new score to the previous
        for alternative in preferences[1]:
            total_scores[alternative] = 0
        for pref_list in preferences.values():
            score = 0
            for alternative in pref_list:
                agent_preference_scores[alternative] = score_vector[score]
                score += 1
                total_scores[alternative] += agent_preference_scores[alternative]

        highest_score = max(total_scores.values())  # determining the highest score

        # checking to see if there is a tie between the highest scores
        repetition = 0
        for score in total_scores.values():
            if score == highest_score:
                repetition += 1

        if repetition > 1:  # if there is a tie, applies tie breaking rules
            possible_winners = [alternative for alternative, score in total_scores.items() if score == highest_score]  # creates a list of possible winners
            if tie_break == "min":
                return min(possible_winners)
            if tie_break == "max":
                return max(possible_winners)
            else:
                try:  # error handling in case the input integer does not correspond to an agent
                    if int(tie_break) not in preferences.keys():
                        raise ValueError("Integer does not correspond to an agent")
                except Exception as exp:
                    print(f"ERROR HAS OCCURED: {exp}")
                    return False
                else:
                    pref = preferences[tie_break]  # creating a list of the input agents preferences
                    pref_index = []
                    for alternative in possible_winners:  # loops through the preference list to see if any of those preferences is one of the possible winners
                        if alternative in pref:  # if one of the possible winners, adds it to new list
                            pref_index.append(pref.index(alternative))
                    return pref[min(pref_index)]  # returns the possible winner with the highest score using min, as the list is not sorted by reverse
                
        else:  # if there isn't a tie, returns the alternative with the highest score
            return max(total_scores, key=total_scores.get)


def plurality(preferences, tie_break):
      
    """
    The winner is the alternative that appears the most times in the first position of the agents' preference orderings.

    PARAMETERS
    -----------
    preferences: (dict)
        A preference profile represented by a dictionary.

    tie_break:
        an option for the tie-breaking among possible winners.
        We will consider the following three tie-breaking rules. Here, we assume that the alternatives are represented by integers.
            max: Among the possible winning alternatives, select the one with the highest number.
            min: Among the possible winning alternatives, select the one with the lowest number.
            agent : Among the possible winning alternatives, select the one that agent ranks the highest in his/her preference ordering. 

    RETURNS
    -----------
    it returns the winner of the Plurality rule, using the tie-breaking option to distinguish between possible winners.
    """

    first_count = {}  # an empty list to keep track of how many times an alternative was in first place for each agent

    for pref_list in preferences.values():
        first_preference = pref_list[0]
        if first_preference not in first_count:
            first_count[first_preference] = 1
        else:
            first_count[first_preference] += 1

    max_score = max(first_count.values())
    possible_winners = [alternative for alternative, score in first_count.items() if score == max_score]  # creating a list of possible winners

    if len(possible_winners) == 1:
        return possible_winners[0]
    
    else:  # if there is a tie, apply tie breaking rules
        if tie_break == "min":
            return min(possible_winners)
        elif tie_break == "max":
            return max(possible_winners)
        else:
            try:  # error handling in case input number does not correspond to an agent
                if int(tie_break) not in preferences.keys():
                    raise ValueError("Integer does not correspond to an agent")
            except Exception as exp:
                print(f"ERROR HAS OCCURED: {exp}")
                return False
            else:
                pref = preferences[tie_break]  # creating a list of the input agents preferences
                pref_index = []
                for alternative in possible_winners:  # loops through the preference list to see if any of those preferences is one of the possible winners
                    if alternative in pref:  # if one of the possible winners, adds it to new list
                        pref_index.append(pref.index(alternative))
                return pref[min(pref_index)]   # returns the possible winner with the highest score using min, as the list is not sorted by reverse
        

def veto(preferences, tie_break):

    """
    Every agent assigns 0 points to the alternative that they rank in the last place of their preference orderings, 
    and 1 point to every other alternative. The winner is the alternative with the most number of points.

    PARAMETERS
    -----------
    preferences: (dict)
        A preference profile represented by a dictionary.

    tie_break:
        an option for the tie-breaking among possible winners.
        We will consider the following three tie-breaking rules. Here, we assume that the alternatives are represented by integers.
            max: Among the possible winning alternatives, select the one with the highest number.
            min: Among the possible winning alternatives, select the one with the lowest number.
            agent : Among the possible winning alternatives, select the one that agent ranks the highest in his/her preference ordering. 

    RETURNS
    -----------
    it returns the winner of the veto rule, using the tie-breaking option to distinguish between possible winners.
    """

    scores = {}  # creating an empty list to keep track of scores
    
    for pref_list in preferences.values():
        last_ranked = pref_list[-1]
        if last_ranked not in scores:  # initializing the last ranked
            scores[last_ranked] = 0
        else:
            scores[last_ranked] += 0  # last rank getting a score of 0

        for alternative in pref_list[:-1]:  # iterating through the list, without considering the last ranked
            if alternative not in scores:  # initializing the other alternatives
                scores[alternative] = 1
            else:
                scores[alternative] += 1  # adding one score
                
    max_score = max(scores.values())
    possible_winners = [alternative for alternative, score in scores.items() if score == max_score]  # creating a list of possible winners

    if len(possible_winners) == 1:  # if there isn't a tie, return the only item in the list of possible winners
        return possible_winners[0]
    
    else:  # in case of tie, tie breaking rules apply
        if tie_break == "min":
            return min(possible_winners)
        elif tie_break == "max":
            return max(possible_winners)
        else:
            try:
                if int(tie_break) not in preferences.keys():
                    raise ValueError("Alternative does not correspond to an agent")
            except Exception as exp:
                print(f"ERROR HAS OCCURED: {exp}")
                return False
            else:
                pref = preferences[tie_break]
                pref_index = []
                for alternative in possible_winners:
                    if alternative in pref:
                        pref_index.append(pref.index(alternative))
                return pref[min(pref_index)]
            

def borda(preferences, tie_break):

    """
    Every agent assigns a score of 0 to the their least-preferred alternative (the one at the bottom of the preference ranking),
    a score of 1 to the second least-preferred alternative, ... , and a score of m - 1 to their favourite alternative.
    In other words, the alternative ranked at position j receives a score of m - j. The winner is the alternative with the highest score.

    PARAMETERS
    -----------
    preferences: (dict)
        A preference profile represented by a dictionary.

    tie_break:
        an option for the tie-breaking among possible winners.
        We will consider the following three tie-breaking rules. Here, we assume that the alternatives are represented by integers.
            max: Among the possible winning alternatives, select the one with the highest number.
            min: Among the possible winning alternatives, select the one with the lowest number.
            agent : Among the possible winning alternatives, select the one that agent ranks the highest in his/her preference ordering. 

    RETURNS
    -----------
    it returns the winner of the borda rule, using the tie-breaking option to distinguish between possible winners.
    """

    scores = {}  # creating an empty list of scores for each iteration
    total_scores = {}  # creating a list to keep track of the scores

    for pref_list in preferences.values():
        length = len(pref_list)
        for n in range(-1, -length-1, -1):  # going through the alternatives in the preference list -1 by -1, basically in reverse, creating a recrusion loop
            if n == -1:
                scores[pref_list[n]] = 0  # if it's the least favored, gets a score of 0
                total_scores[pref_list[n]] = total_scores.get(pref_list[n], 0) + scores[pref_list[n]]  # adds it to previously attained scores for that alternative
            else:
                scores[pref_list[n]] = scores[pref_list[n+1]] + 1
                total_scores[pref_list[n]] = scores[pref_list[n]] + total_scores.get(pref_list[n], 0)

    max_score = max(total_scores.values())
    possible_winners = [alternative for alternative, score in total_scores.items() if score == max_score]

    if len(possible_winners) == 1:
        return possible_winners[0]
    
    else:
        if tie_break == "min":
            return min(possible_winners)
        elif tie_break == "max":
            return max(possible_winners)
        else:
            try:
                if int(tie_break) not in preferences.keys():
                    raise ValueError("Alternative does not correspond to an agent")
            except Exception as exp:
                print(f"ERROR HAS OCCURED: {exp}")
                return False
            else:
                pref = preferences[tie_break]
                pref_index = []
                for alternative in possible_winners:
                    if alternative in pref:
                        pref_index.append(pref.index(alternative))
                return pref[min(pref_index)]
        
        
def harmonic(preferences, tie_break):
    
    """
    Every agent assigns a score of 1/m to the their least-preferred alternative (the one at the bottom of the preference ranking),
    a score of 1/(m-1) to the second least-preferred alternative, ... , and a score of 1 to their favourite alternative.
    In other words, the alternative ranked at position j receives a score of 1/j . The winner is the alternative with the highest score.

    PARAMETERS
    -----------
    preferences: (dict)
        A preference profile represented by a dictionary.

    tie_break:
        an option for the tie-breaking among possible winners.
        We will consider the following three tie-breaking rules. Here, we assume that the alternatives are represented by integers.
            max: Among the possible winning alternatives, select the one with the highest number.
            min: Among the possible winning alternatives, select the one with the lowest number.
            agent : Among the possible winning alternatives, select the one that agent ranks the highest in his/her preference ordering. 

    RETURNS
    -----------
    it returns the winner of the harmonic rule, using the tie-breaking option to distinguish between possible winners.
    """

    scores = {}  # creates a list of scores for each iteration
    total_scores = {}  # creating a list to keep track of scores

    for pref_list in preferences.values():
        length = len(pref_list)
        for n in range(0, length):  # loops through the preferences of each agent
            scores[pref_list[n]] = 1/(n+1)
            total_scores[pref_list[n]] = scores[pref_list[n]] + total_scores.get(pref_list[n], 0)  # adds the newly attained score to the previous ones for that alternative
            
    max_score = max(total_scores.values())
    possible_winners = [alternative for alternative, score in total_scores.items() if score == max_score]

    if len(possible_winners) == 1:
        return possible_winners[0]
    
    else:
        if tie_break == "min":
            return min(possible_winners)
        elif tie_break == "max":
            return max(possible_winners)
        else:
            try:
                if int(tie_break) not in preferences.keys():
                    raise ValueError("Alternative does not correspond to an agent")
            except Exception as exp:
                print(f"ERROR HAS OCCURED: {exp}")
                return False
            else:
                pref = preferences[tie_break]
                pref_index = []
                for alternative in possible_winners:
                    if alternative in pref:
                        pref_index.append(pref.index(alternative))
                return pref[min(pref_index)]


def STV(preferences, tie_break):
 
    """
    The voting rule works in rounds. In each round, the alternatives that appear
    the least frequently in the first position of agents' rankings are removed, and the process is repeated. When the final set of alternatives
    is removed (one or possibly more), then this last set is the set of possible winners.

    PARAMETERS
    -----------
    preferences: (dict)
        A preference profile represented by a dictionary.

    tie_break:
        an option for the tie-breaking among possible winners.
        We will consider the following three tie-breaking rules. Here, we assume that the alternatives are represented by integers.
            max: Among the possible winning alternatives, select the one with the highest number.
            min: Among the possible winning alternatives, select the one with the lowest number.
            agent : Among the possible winning alternatives, select the one that agent ranks the highest in his/her preference ordering. 

    RETURNS
    -----------
    it returns the winner of the Single Transferable Vote rule, using the tie-breaking option to distinguish between possible winners.
    """

    count = {}  # creating a list to keep track of how many times an alternative is least frequently the first

    for pref_list in preferences.values():
        for alternative in pref_list:
            if alternative not in count:
                count[alternative] = 0  # initializes the count list for each alternative

    for pref_list in preferences.values():  # creates a loop to count how many times each alternative has been in the first place
        first_ranked = pref_list[0]
        if first_ranked not in count:
            count[first_ranked] = 1
        else:
            count[first_ranked] += 1

    while min(count.values()) != max(count.values()):  # creates a loop that will go on until there are only alternatives with the highest score remaining
        least_frequent = min(count.values())
        removed = []  # creates a list of least frequent alternatives
        for alternative, alt_count in count.items():
            if alt_count == least_frequent:
                removed.append(alternative)  # adds the least frequent alternative to the to be removed list
        for pref_list in preferences.values():
            for least_alternative in removed:
                if least_alternative in pref_list:  # finds the least frequent alternative in the pref list and removes it
                    while least_alternative in pref_list:
                        pref_list.remove(least_alternative)
                    if pref_list:  # after removing, adds one score to the next first place
                        count[pref_list[0]] += 1
        for alternative in removed:  # removes the least frequent alternative from the count dictionary as well
            del count[alternative]

    possible_winners = list(count.keys())  # creates a list of possible winners

    if len(possible_winners) == 1:
        return possible_winners[0]

    else:
        if tie_break == "min":
            return min(possible_winners)
        elif tie_break == "max":
            return max(possible_winners)
        else:
            try:
                if int(tie_break) not in preferences.keys():
                    raise ValueError("Alternative does not correspond to an agent")
            except Exception as exp:
                print(f"ERROR HAS OCCURED: {exp}")
                return False
            else:
                pref = preferences[tie_break]
                pref_index = []
                for alternative in possible_winners:
                    if alternative in pref:
                        pref_index.append(pref.index(alternative))
                return pref[min(pref_index)]



def range_voting(values, tie_break):

    """
    Sums the numerical values in an xlsx file, and chooses the alternative with the maximum sum as the winner.

    PARAMETERS
    -----------
    values:
        a worksheet corresponding to an xlsx file

    tie_break:
        an option for the tie-breaking among possible winners.
        We will consider the following three tie-breaking rules. Here, we assume that the alternatives are represented by integers.
            max: Among the possible winning alternatives, select the one with the highest number.
            min: Among the possible winning alternatives, select the one with the lowest number.
            agent : Among the possible winning alternatives, select the one that agent ranks the highest in his/her preference ordering. 

    RETURNS
    -----------
    The function should return the alternative that has the maximum sum of valuations, i.e.,
    the maximum sum of numerical values in the xlsx file, using the tie-breaking option to distinguish between possible winners.
    """

    worksheet = values
    preferences = generate_preferences(values)  # turns the preference profile in the xlsx file into a dictionary
    max_val = 0
    agents_pref = []  # creates a list of the agents preferences valuations

    for row in worksheet.values:  # iterates through each row in the worksheet and adds it as a list to agents_pref
        agents_pref.append(list(row))

    length = len(agents_pref[0])
    valuation = [0]*length  # creates and initializes a new list with the length of l

    for alternative in range(length):  # iterates through each alternative and adds their values together
        for val in agents_pref:
            valuation[alternative] += val[alternative]

    max_val = max(valuation)
    possible_winners = [alternative + 1 for alternative in range(len(valuation)) if valuation[alternative] == max_val]  # creates a list of possible winners

    if len(possible_winners) == 1:  # check for ties in possible winners
        return possible_winners[0]

    else:  # applies tie breaking rules in case of a tie
        if tie_break == "min":
            return min(possible_winners)
        elif tie_break == "max":
            return max(possible_winners)
        else:
            try:
                if int(tie_break) not in preferences.keys():
                    raise ValueError("Alternative does not correspond to an agent")
            except Exception as exp:
                print(f"ERROR HAS OCCURED: {exp}")
                return False
            else:
                pref = preferences[tie_break]
                pref_index = []
                for alternative in possible_winners:
                    if alternative in pref:
                        pref_index.append(pref.index(alternative))
                return pref[min(pref_index)]
