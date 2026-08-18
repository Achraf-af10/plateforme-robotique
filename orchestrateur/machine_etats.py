from transitions import Machine

class OrchestratorCellule:
    states = [
        "idle",
        "ur5_vers_a",
        "ur12e_vers_b",
        "jaka_vers_c",
        "ur5_vers_d",
        "ur12e_vers_e",
        "jaka_vers_f",
        "done",
        "error",
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=self.states, initial="idle")
        self.machine.add_transition("start", "idle", "ur5_vers_a")
        self.machine.add_transition("a_reached", "ur5_vers_a", "ur12e_vers_b")
        self.machine.add_transition("b_reached", "ur12e_vers_b", "jaka_vers_c")
        self.machine.add_transition("c_reached", "jaka_vers_c", "ur5_vers_d")
        self.machine.add_transition("d_reached", "ur5_vers_d", "ur12e_vers_e")
        self.machine.add_transition("e_reached", "ur12e_vers_e", "jaka_vers_f")
        self.machine.add_transition("f_reached", "jaka_vers_f", "done")
        self.machine.add_transition("fault", "*", "error")



