# regex-machine
This repo contains an algorithm demonstrating the theorem that regular expressions are closed under their operators, converting any regex to a corresponding non-deterministic finite automaton (NFA), then to a deterministic one (DFA) using Thompson's construction algorithm.





## NFA and RegexToNFAConverter

This Python script contains two classes: `NFA` and `RegexToNFAConverter`. These classes work together to convert a regular expression (regex) into a non-deterministic finite automaton (NFA), a foundational concept in the theory of computation.

### How The Conversion Works

The `RegexToNFAConverter` class converts a regex to an NFA using the following steps:

1. **Initialization**: It initializes an empty NFA and a stack to hold intermediate results during the conversion.
2. **Character Processing**: It iterates over each character in the regex:
   - If the character is alphanumeric, it creates two new states, representing the start and end states of a new NFA that recognizes the single character.
   - If the character is one of the operators `*`, `|`, or `.`, or a parenthesis, it is added to a stack of operators to be processed later.
   - If the character is a closing parenthesis `)`, it applies operators until an opening parenthesis `(` is encountered.
3. **Operator Application**: After processing all characters, any remaining operators in the stack are applied to construct the final NFA.
4. **Finalizing NFA**: The start and final states of the resulting NFA are set based on the last element in the stack.

### Usage

To use these classes in your Python script, import them and then create a `RegexToNFAConverter` object with the regex you wish to convert. Call the `convert` method to get the resulting NFA. You can then use the NFA's attributes and methods to work with the NFA.

```python
converter = RegexToNFAConverter("a|b")
nfa = converter.convert()
```

### Note
The repo is still under development, next goals is to convert the NFA to DFA and miniminze it

