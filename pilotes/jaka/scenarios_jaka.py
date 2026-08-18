"""Tous les scénarios pour JAKA"""

def move_to_point_c(robot, data):
    """JAKA va au point C"""
    print(f"[jaka] Move to point C (N°{data.get('numero')})")
    point_c = [1.7388542253407, 1.2955673064333557, 1.5242288219560445, 1.8926079559748334, -1.5707928093415555, 3.3096465110834887]
    robot.joint_move(point_c, 0, True, 0.5)

def move_to_point_f(robot, data):
    """JAKA va au point F"""
    print(f"[jaka] Move to point F (N°{data.get('numero')})")
    point_f = [1.4738710124401888, 1.3598507487474776, 2.1521663365868333, 1.2003992163344779, -1.5707928093415555, 3.044663298182978]
    robot.joint_move(point_f, 0, True, 0.5)

# Dictionnaire des scénarios disponibles
SCENARIOS = {
    "move_to_point_c": move_to_point_c,
    "move_to_point_f": move_to_point_f,
}
