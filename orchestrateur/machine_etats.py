from transitions import Machine

class OrchestratorCellule:
    states = [
        "idle",
        "ur12e_vers_a",
        "ur12e_vers_b",
        "ur5_vers_1",
        "ur12e_vers_2",
        "ur5_vers_3",
        "ur12e_vers_4",
        "ur5_vers_5",
        "ur12e_vers_6",
        "ur5_vers_7",
        "ur12e_vers_8",
        "ur5_vers_9",
        "ur12e_vers_10",
        "ur5_vers_11",
        "ur12e_vers_12",
        "ur5_vers_13",
        "ur12e_vers_14",
        "done",
        "error",
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=self.states, initial="idle")


        self.machine.add_transition("start", "idle", "ur12e_vers_a")
        self.machine.add_transition("a_reached", "ur12e_vers_a", "ur12e_vers_b")
        self.machine.add_transition("b_reached", "ur12e_vers_b", "ur5_vers_1")
        self.machine.add_transition("1_reached", "ur5_vers_1", "ur12e_vers_2")
        self.machine.add_transition("2_reached", "ur12e_vers_2", "ur5_vers_3")
        self.machine.add_transition("3_reached", "ur5_vers_3", "ur12e_vers_4")
        self.machine.add_transition("4_reached", "ur12e_vers_4", "ur5_vers_5")
        self.machine.add_transition("5_reached", "ur5_vers_5", "ur12e_vers_6")
        self.machine.add_transition("6_reached", "ur12e_vers_6", "ur5_vers_7")
        self.machine.add_transition("7_reached", "ur5_vers_7", "ur12e_vers_8")
        self.machine.add_transition("8_reached", "ur12e_vers_8", "ur5_vers_9")
        self.machine.add_transition("9_reached", "ur5_vers_9", "ur12e_vers_10")
        self.machine.add_transition("10_reached", "ur12e_vers_10", "ur5_vers_11")
        self.machine.add_transition("11_reached", "ur5_vers_11", "ur12e_vers_12")
        self.machine.add_transition("12_reached", "ur12e_vers_12", "ur5_vers_13")
        self.machine.add_transition("13_reached", "ur5_vers_13", "ur12e_vers_14")
        self.machine.add_transition("14_reached", "ur12e_vers_14", "done")

        # Gestion des erreurs
        self.machine.add_transition("fault", "*", "error")