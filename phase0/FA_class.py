import json


class State:
    __counter = 0

    def __init__(self, id: None) -> None:
        if id is None:
            self.id = State._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, 'State'] = {}

    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class DFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list['State'] = []
        self.alphabet: list['str'] = []
        self.final_states: list['State'] = []

    @staticmethod
    def deserialize_json(json_str: str) -> 'DFA':
        fa = DFA()
        json_fa = json.loads(json_str)

        fa.alphabet = json_fa["alphabet"]

        for state_str in json_fa["states"]:
            fa.add_state(state_str[2:])

        fa.init_state = fa.get_state_by_id(json_fa["initial_state"][2:])

        for final_str in json_fa["final_states"]:
            fa.add_final_state(fa.get_state_by_id(final_str[2:]))

        for state_str in json_fa["states"]:
            for symbol in fa.alphabet:
                fa.add_transition(fa.get_state_by_id(state_str[2:]), fa.get_state_by_id(json_fa[state_str][symbol][2:]),
                                  symbol)

        return fa

    def serialize_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }

        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                fa[f"q_{state.id}"][symbol] = f"q_{state.transitions[symbol].id}"

        return json.dumps(fa)

    def add_state(self, id: int | None = None) -> State:
        state = State(id)
        self.states.append(state)
        return state

    def add_transition(self, from_state: State, to_state: State, input_symbol: str) -> None:
        from_state.add_transition(input_symbol, to_state)

    def assign_initial_state(self, state: State) -> None:
        self.init_state = state

    def add_final_state(self, state: State) -> None:
        self.final_states.append(state)

    def get_state_by_id(self, id) -> State | None:
        for state in self.states:
            if state.id == id:
                return state
        return None

    def is_final(self, state: State) -> bool:
        return state in self.final_states


class NFAState:
    __counter = 0

    def __init__(self, id: None) -> None:
        if id is None:
            self.id = NFAState._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, list['NFAState']] = {}

    def add_transition(self, symbol: str, state: 'NFAState') -> None:
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

    def add_epsilon_transition(self, state: 'NFAState') -> None:
        self.add_transition("", state)

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class NFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list['NFAState'] = []
        self.alphabet: list['str'] = []
        self.final_states: list['NFAState'] = []

    def deserialize_json(json_str: str) -> 'NFA':
        fa = NFA()
        json_fa = json.loads(json_str)

        fa.alphabet = json_fa["alphabet"]

        for state_str in json_fa["states"]:
            fa.add_state(int(state_str[2:]))

        fa.init_state = fa.get_state_by_id(json_fa["initial_state"][2:])

        for final_str in json_fa["final_states"]:
            fa.add_final_state(fa.get_state_by_id(final_str[2:]))

        for state_str in json_fa["states"]:
            for symbol in fa.alphabet:
                next_states = json_fa[state_str][symbol]
                for next_state_str in next_states:
                    fa.add_transition(fa.get_state_by_id(state_str[2:]), fa.get_state_by_id(next_state_str[2:]), symbol)

        return fa

    def serialize_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }

        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                next_state_ids = []
                for next_state in state.transitions.get(symbol, []):
                    next_state_ids.append(f"q_{next_state.id}")
                fa[f"q_{state.id}"][symbol] = next_state_ids

        return json.dumps(fa)

    def add_state(self, id: int | None = None) -> NFAState:
        state = NFAState(id)
        self.states.append(state)
        return state

    def add_transition(self, from_state: NFAState, to_state: NFAState, input_symbol: str) -> None:
        from_state.add_transition(input_symbol, to_state)

    def add_epsilon_transition(self, from_state: NFAState, to_state: NFAState) -> None:
        from_state.add_epsilon_transition(to_state)

    def assign_initial_state(self, state: NFAState) -> None:
        self.init_state = state

    def add_final_state(self, state: NFAState) -> None:
        self.final_states.append(state)

    def get_state_by_id(self, id) -> NFAState | None:
        for state in self.states:
            if state.id == id:
                return state
        return None

    def is_final(self, state: NFAState) -> bool:
        return state in self.final_states

    @staticmethod
    def convert_DFA_instanse_to_NFA_instanse(dfa_machine: 'DFA') -> 'NFA':
        nfa_machine = NFA()
        nfa_machine.alphabet = dfa_machine.alphabet

        for state in dfa_machine.states:
            nfa_state = nfa_machine.add_state(state.id)
            if state == dfa_machine.init_state:
                nfa_machine.assign_initial_state(nfa_state)
            if state in dfa_machine.final_states:
                nfa_machine.add_final_state(nfa_state)

        for state in dfa_machine.states:
            for symbol, next_state in state.transitions.items():
                nfa_machine.add_transition(nfa_machine.get_state_by_id(state.id),
                                           nfa_machine.get_state_by_id(next_state.id), symbol)

        return nfa_machine

    @staticmethod
    def union(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        union_machine = NFA()
        union_machine.alphabet = list(set(machine1.alphabet + machine2.alphabet))

        init_state = union_machine.add_state()
        union_machine.assign_initial_state(init_state)
        union_machine.add_transition(init_state, machine1.init_state, "")
        union_machine.add_transition(init_state, machine2.init_state, "")

        for final_state in machine1.final_states:
            union_machine.add_final_state(final_state)
        for final_state in machine2.final_states:
            union_machine.add_final_state(final_state)

        for state in machine1.states + machine2.states:
            union_state = union_machine.add_state(state.id)
            if state == machine1.init_state or state == machine2.init_state:
                union_machine.add_transition(init_state, union_state, "")
            if state in machine1.final_states or state in machine2.final_states:
                union_machine.add_transition(union_state, init_state, "")

            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    union_machine.add_transition(union_state, union_machine.get_state_by_id(next_state.id), symbol)

        return union_machine

    @staticmethod
    def concat(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        concat_machine = NFA()
        concat_machine.alphabet = list(set(machine1.alphabet + machine2.alphabet))

        for state in machine1.states:
            concat_state = concat_machine.add_state(state.id)
            if state == machine1.init_state:
                concat_machine.assign_initial_state(concat_state)
            if state in machine1.final_states:
                concat_machine.add_final_state(concat_state)
            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    concat_machine.add_transition(concat_state, concat_machine.get_state_by_id(next_state.id), symbol)

        for state in machine2.states:
            concat_state = concat_machine.add_state(state.id)
            if state == machine2.init_state:
                concat_machine.add_transition(concat_machine.final_states[0], concat_state, "")
            if state in machine2.final_states:
                concat_machine.add_final_state(concat_state)
            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    concat_machine.add_transition(concat_state, concat_machine.get_state_by_id(next_state.id), symbol)

        return concat_machine

    @staticmethod
    def star(machine: 'NFA') -> 'NFA':
        star_machine = NFA()
        star_machine.alphabet = machine.alphabet

        init_state = star_machine.add_state()
        star_machine.assign_initial_state(init_state)
        star_machine.add_transition(init_state, machine.init_state, "")
        star_machine.add_transition(init_state, star_machine.final_states[0], "")

        for final_state in machine.final_states:
            star_machine.add_transition(final_state, init_state, "")
        for state in machine.states:
            star_state = star_machine.add_state(state.id)
            if state == machine.init_state:
                star_machine.add_transition(init_state, star_state, "")
            if state in machine.final_states:
                star_machine.add_transition(star_state, init_state, "")
            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    star_machine.add_transition(star_state, star_machine.get_state_by_id(next_state.id), symbol)

        return star_machine

    # def serialize_to_json(self) -> str:
