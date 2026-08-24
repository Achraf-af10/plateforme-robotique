"""
Classe UR12e : encapsule la connexion RTDE et les mouvements basiques.
Responsabilité : communication RTDE uniquement.
"""
import signal
import sys
import rtde_control
import rtde_receive
import rtde_io

class UR12e:
    def __init__(self, ip="10.120.0.12"):
        self.ip = ip
        self.rtde_c = None
        self.rtde_r = None
        self.rtde_io = None
        self._connect()
        signal.signal(signal.SIGINT, self._cleanup)
        signal.signal(signal.SIGTERM, self._cleanup)

    def _connect(self):
        """Établir la connexion RTDE."""
        try:
            self.rtde_c = rtde_control.RTDEControlInterface(self.ip)
            self.rtde_r = rtde_receive.RTDEReceiveInterface(self.ip)
            self.rtde_io = rtde_io.RTDEIOInterface(self.ip)
            print(f"[UR12e] Connecté à {self.ip}")
        except Exception as e:
            print(f"[UR12e] Erreur connexion : {e}")
            raise

    def _cleanup(self, signum=None, frame=None):
        """Fermer la connexion proprement."""
        print("[UR12e] Fermeture connexion RTDE...")
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

    def get_actual_q(self):
        """Récupérer la position articulaire actuelle."""
        return self.rtde_r.getActualQ()

    def get_actual_pose(self):
        """Récupérer la pose TCP actuelle."""
        return self.rtde_r.getActualTCPPose()

    def get_actual_force(self):
        """Récupérer la force au TCP."""
        return self.rtde_r.getActualTCPForce()

    def get_inverse_kinematics(self, pose, qnear=None):
        """Calculer l'inverse kinématique."""
        return self.rtde_c.getInverseKinematics(pose, qnear=qnear)

    def pose_trans(self, from_pose, to_pose):
        """Transformer une pose d'un repère à l'autre."""
        return self.rtde_c.poseTrans(from_pose, to_pose)

    def set_speed_slider(self, speed):
        """Régler le multiplicateur de vitesse (0.0 à 1.0)."""
        self.rtde_io.setSpeedSlider(speed)

    def get_digital_in(self, pin):
        """Lire l'état d'une entrée digitale."""
        return self.rtde_r.getDigitalInState(pin)
