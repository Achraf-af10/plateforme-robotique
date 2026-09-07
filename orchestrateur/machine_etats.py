from transitions import Machine

class OrchestratorCellule:
    states = [
        "idle",
        "ur5_vers_a",
        "ur12e_vers_b",
        "ur5_vers_c",
        "ur12e_vers_d",
        "ur5_vers_e",
        "ur12e_vers_f",
        "ur5_vers_g",
        "ur5_vers_h",
        "ur12e_vers_i",
        "ur5_vers_j",
        "ur12e_vers_k",
        "done",
        "error",
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=self.states, initial="idle")
        self.machine.add_transition("start", "idle", "ur5_vers_a")
        self.machine.add_transition("a_reached", "ur5_vers_a", "ur12e_vers_b")
        self.machine.add_transition("b_reached", "ur12e_vers_b", "ur5_vers_c")
        self.machine.add_transition("c_reached", "ur5_vers_c", "ur12e_vers_d")
        self.machine.add_transition("d_reached", "ur12e_vers_d", "ur5_vers_e")
        self.machine.add_transition("e_reached", "ur5_vers_e", "ur12e_vers_f")
        self.machine.add_transition("f_reached", "ur12e_vers_f", "ur5_vers_g")
        self.machine.add_transition("j_reached","ur5_vers_g", "ur5_vers_h")
        self.machine.add_transition("i_reached", "ur5_vers_h", "ur12e_vers_i")
        self.machine.add_transition("g_reached", "ur12e_vers_i", "ur5_vers_j")
        self.machine.add_transition("h_reached", "ur5_vers_j", "ur12e_vers_k")
        self.machine.add_transition("k_reached", "ur12e_vers_k", "done")
        self.machine.add_transition("fault", "*", "error")



