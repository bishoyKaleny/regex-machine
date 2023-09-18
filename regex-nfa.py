class NFA:
    """This class represents a Non-deterministic Finite Automaton (NFA)"""

    def __init__(self):
        """Initialize an NFA with an empty set of states, no start state, and no final states."""
        self.states = {}
        self.start_state = None
        self.final_states = set()

    def add_state(self, name, transitions=None, is_final=False):
        """
        Adds a state to the NFA.
        
        :param name: The name of the state to add
        :param transitions: A dictionary representing the transitions from the state
        :param is_final: A boolean indicating whether the state is a final state
        """
        self.states[name] = transitions or {}
        if is_final:
            self.final_states.add(name)

    def set_start_state(self, name):
        """Sets the start state of the NFA.
        
        :param name: The name of the start state
        """
        self.start_state = name

    def remove_final_state(self, name):
        """Removes a state from the set of final states.
        
        :param name: The name of the state to remove
        """
        self.final_states.discard(name)


class RegexToNFAConverter:
    """This class converts a regular expression to a Non-deterministic Finite Automaton (NFA)"""

    def __init__(self, regex):
        """Initialize the converter with a given regular expression and a stack to keep track of states during conversion."""
        self.regex = regex
        self.stack = []
        self.state_id = 0

    def new_state(self):
        """Creates a new state with a unique name based on the current state ID."""
        self.state_id += 1
        return f'q{self.state_id}'

    def convert(self):
        """Converts the regular expression to an NFA using Thompson's construction algorithm."""
        nfa = NFA()
        operators = []
        i = 0

        # Iterate through the characters in the regex string
        while i < len(self.regex):
            char = self.regex[i]

            # If character is alphanumeric, create new states and transitions
            if char.isalnum():
                s1, s2 = self.new_state(), self.new_state()
                nfa.add_state(s1, {char: {s2}})
                nfa.add_state(s2, is_final=True)
                self.stack.append((s1, {s2}))

            # If character is an operator or a parenthesis, add it to the operators stack
            elif char in ['*', '|', '(', '.']:
                operators.append(char)

            # If character is a closing parenthesis, pop and apply operators until an opening parenthesis is encountered
            elif char == ')':
                while operators[-1] != '(':
                    self._apply_operator(operators.pop(), nfa)
                operators.pop()
            i += 1

        # Apply any remaining operators in the stack
        while operators:
            self._apply_operator(operators.pop(), nfa)

        # Set the start and final states of the NFA
        start, ends = self.stack.pop()
        nfa.set_start_state(start)
        return nfa

    def _apply_operator(self, operator, nfa):
        """Applies an operator to the top elements of the stack to build the NFA.

        :param operator: The operator to apply ('*', '|', or '.')
        :param nfa: The NFA being built
        """
        if operator == '*':
            # Apply the Kleene star operation
            start, ends = self.stack.pop()
            new_start = self.new_state()
            nfa.add_state(new_start, {'ε': {start}}, is_final=True)
            for end in ends:
                nfa.states[end]['ε'] = nfa.states.get(end, {}).get('ε', set()) | {start}
            new_end = {new_start}.union(ends)
            self.stack.append((new_start, new_end))

        elif operator == '.':
            # Apply the concatenation operation
            start2, ends2 = self.stack.pop()
            start1, ends1 = self.stack.pop()
            for end in ends1:
                nfa.states[end]['ε'] = nfa.states.get(end, {}).get('ε', set()) | {start2}
            for end in ends1:
                nfa.remove_final_state(end)
            self.stack.append((start1, ends2))

        elif operator == '|':
            # Apply the union operation
            start2, ends2 = self.stack.pop()
            start1, ends1 = self.stack.pop()
            new_start = self.new_state()
            nfa.add_state(new_start, {'ε': {start1, start2}})
            new_ends = ends1.union(ends2)
            self.stack.append((new_start, new_ends))

# Usage
regex = '(a|a.b)*'
converter = RegexToNFAConverter(regex)
nfa = converter.convert()

# Print the NFA
for state, transitions in nfa.states.items():
    print(f'{state}: {transitions}')
print(f'Start state: {nfa.start_state}')
print(f'Final states: {nfa.final_states}')
