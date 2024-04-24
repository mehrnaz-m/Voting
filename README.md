# Preference Aggregation System
## Overview
This Python module, developed by Mehrnaz Miri, provides functionalities for preference aggregation using various voting and ranking methods. It includes algorithms for generating preference profiles, as well as implementing different voting rules such as Dictatorship, Scoring Rule, Plurality, Veto, Borda, Harmonic, Single Transferable Vote (STV), and Range Voting.

## Functions
1. `generate_preferences(values)`
    - Description: Generates a preference profile from numerical values provided as input.
      
3. `dictatorship(preferences, agent)`
    - Description: Implements the Dictatorship voting rule, where the winner is determined by the preference of a selected agent.
4. `scoring_rule(preferences, score_vector, tie_break)`
    - Description: Applies the Scoring Rule, assigning scores to alternatives based on agent preferences and a given score vector.
5. `plurality(preferences, tie_break)`
    - Description: Implements the Plurality voting rule, where the winner is the alternative with the most first-place votes.
6. `veto(preferences, tie_break)`
    - Description: Implements the Veto voting rule, where alternatives are assigned scores based on agent preferences, with the lowest-ranked alternative receiving a score of 0.
7. `borda(preferences, tie_break)`
    - Description: Applies the Borda voting rule, where each alternative receives a score based on its position in the preference list.
8. `harmonic(preferences, tie_break)`
    - Description: Implements the Harmonic voting rule, where alternatives are assigned scores inversely proportional to their rank in agent preferences.
9. `STV(preferences, tie_break)`
    - Description: Implements the Single Transferable Vote (STV) voting rule, eliminating alternatives with the least first-place votes in each round until a winner is determined.
10. `range_voting(values, tie_break)`
    - Description: Applies Range Voting, summing up numerical values associated with alternatives to determine the winner.

## Usage
- Import the module into your Python script or interactive environment.
- Utilize the provided functions with appropriate inputs to perform preference aggregation according to desired voting rules.
  
## Author
This module was written by Mehrnaz Miri.
