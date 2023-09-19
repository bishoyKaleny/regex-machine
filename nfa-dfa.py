from regex_nfa import NFA

class DFA(NFA):
    def __init__(self):
        super().__init__()

    def add_state(self, name, transitions=None, is_final=False):
        if transitions is not None:
            # Verify that it is a DFA transition
            if 'ε' in transitions:
                raise ValueError("DFA cannot have ε-transitions")

            for dests in transitions.values():
                if not isinstance(dests, str):
                    raise ValueError("DFA transitions must lead to a single state")

        super().add_state(name, transitions, is_final)
