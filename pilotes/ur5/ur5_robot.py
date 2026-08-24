"""
Classe UR5 : encapsule la connexion RTDE et les mouvements basiques.
Responsabilité : communication RTDE uniquement.
"""
import signal
import sys
import rtde_control
import rtde_receive

class UR5:
    def __init__(self, ip="10.120.0.11"):
        self.ip = ip
        self.rtde_c = None
        self.rtde_r = None
        self._connect()
        signal.signal(signal.SIGINT, self._cleanup)
        signal.signal(signal.SIGTERM, self._cleanup)

    def _connect(self):
        """Établir la connexion RTDE."""
        try:
            self.rtde_c = rtde_control.RTDEControlInterface(self.ip)
            self.rtde_r = rtde_receive.RTDEReceiveInterface(self.ip)
            print(f"[UR5] Connecté à {self.ip}")
        except Exception as e:
            print(f"[UR5] Erreur connexion : {e}")
            raise

    def _cleanup(self, signum=None, frame=None):
        """Fermer la connexion proprement."""
        print("[UR5] Fermeture connexion RTDE...")
        if self.rtde_c:
            try:
                self.rtde_c.disconnect()
            except:
                pass
        sys.exit(0)

    def moveL(self, pose, speed=0.1, acceleration=0.1):
        """Mouvement linéaire (TCP)."""
        self.rtde_c.moveL(pose, speed, acceleration)

    def moveJ(self, joint_angles, speed=0.3, acceleration=0.3):
        """Mouvement articulaire."""
        self.rtde_c.moveJ(joint_angles, speed, acceleration)

    def speedL(self, xd, acceleration=0.05, time=0.0):
        """Mouvement continu linéaire."""
        self.rtde_c.speedL(xd, acceleration, time)

    def speedStop(self, deceleration=0.5):
        """Arrêter le mouvement continu."""
        self.rtde_c.speedStop(deceleration)

    def get_actual_q(self):
        """Récupérer la position articulaire actuelle."""
        return self.rtde_r.getActualQ()

    def get_actual_pose(self):
        """Récupérer la pose TCP actuelle."""
        return self.rtde_r.getActualTCPPose()

    def get_actual_force(self):
        """Récupérer la force au TCP."""
        return self.rtde_r.getActualTCPForce()

    def zero_ft_sensor(self):
        """Tarer le capteur de force."""
        self.rtde_c.zeroFtSensor()

    def get_inverse_kinematics(self, pose, qnear=None):
        """Calculer l'inverse kinématique."""
        return self.rtde_c.getInverseKinematics(pose, qnear=qnear)

    def pose_trans(self, from_pose, to_pose):
        """Transformer une pose d'un repère à l'autre."""
        return self.rtde_c.poseTrans(from_pose, to_pose)
