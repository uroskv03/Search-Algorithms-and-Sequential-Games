import random
import time


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_action(self, state, max_depth):
        pass


class RandomAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        return actions[random.randint(0, len(actions) - 1)]


class GreedyAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = None, None
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = new_state.get_score(state.get_on_move_chr())
            if (best_score is None and best_action is None) or score > best_score:
                best_action = action
                best_score = score
        return best_action


class MinimaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = -float('inf'), None
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = self.PlayerMin(self, new_state, max_depth-1)
            if score > best_score:
                best_action = action
                best_score = score
        return best_action

    def PlayerMin(self,state, max_depth):
        if max_depth == 0 or state.is_goal_state():
            x = state.get_on_move_chr()
            y = "B" if x == "A" else "A"
            return state.get_score(y) - state.get_score(x)

        actions = state.get_legal_actions()
        best_score = float('inf')
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = self.PlayerMax(self, new_state, max_depth-1)
            best_score = min(best_score,score)
        return best_score

    def PlayerMax(self,state, max_depth):
        if max_depth == 0 or state.is_goal_state():
            x = state.get_on_move_chr()
            y = "B" if x=="A" else "A"
            return state.get_score(x) - state.get_score(y)
        actions = state.get_legal_actions()
        best_score = -float('inf')
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = self.PlayerMin(self, new_state, max_depth-1)
            best_score = max(score,best_score)
        return best_score

class MinimaxABAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = -float('inf'), None
        alfa = -float('inf')
        beta = float('inf')
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = self.PlayerMin(self, new_state, max_depth-1, alfa, beta)
            if score > best_score:
                best_action = action
                best_score = score
            alfa = max(alfa, best_score)
        return best_action

    def PlayerMin(self,state, max_depth,alfa ,beta):
        if max_depth == 0 or state.is_goal_state():
            x = state.get_on_move_chr()
            y = "B" if x == "A" else "A"
            return state.get_score(y) - state.get_score(x)

        actions = state.get_legal_actions()
        best_score = float('inf')
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = self.PlayerMax(self, new_state, max_depth-1, alfa, beta)
            best_score = min(best_score,score)
            beta = min(beta, best_score)
            if beta <= alfa:
                break
        return best_score

    def PlayerMax(self,state, max_depth, alfa, beta ):
        if max_depth == 0 or state.is_goal_state():
            x = state.get_on_move_chr()
            y = "B" if x=="A" else "A"
            return state.get_score(x) - state.get_score(y)
        actions = state.get_legal_actions()
        best_score = -float('inf')
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = self.PlayerMin(self, new_state, max_depth-1, alfa, beta)
            best_score = max(score,best_score)
            alfa = max(alfa, best_score)
            if beta <= alfa:
                break
        return best_score

class MaxNAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = -float('inf'), None
        self.player_kinds = [chr(ord('A') + i) for i in range(state.get_num_of_players())]
        self.indx = self.player_kinds.index(state.get_on_move_chr())

        for action in actions:
            new_state = state.generate_successor_state(action)
            score = self.m(self, new_state, max_depth - 1)
            if score[self.indx] > best_score:
                best_action = action
                best_score = score[self.indx]
        return best_action

    def m(self, state, max_depth):
        if max_depth == 0 or state.is_goal_state():
            return tuple(state.get_score(p) for p in self.player_kinds)

        current_chr = state.get_on_move_chr()
        current_idx = self.player_kinds.index(current_chr)
        best = None
        for action in state.get_legal_actions():
            cur = self.m(self, state.generate_successor_state(action), max_depth - 1)

            if best is None or cur[current_idx] > best[current_idx]:
                best = cur

        return best