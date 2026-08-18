import json
import paho.mqtt.client as mqtt

class RobotMqttClient:
    def __init__(self, robot_name, broker="localhost", port=1883):
        self.robot_name = robot_name
        self.cmd_topic = f"cell/robot/{robot_name}/cmd"
        self.status_topic = f"cell/robot/{robot_name}/status"
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.on_task = None
        self.broker = broker
        self.port = port

    def _on_connect(self, client, userdata, flags, rc):
        print(f"[{self.robot_name}] connecté au courtier (rc={rc})")
        client.subscribe(self.cmd_topic)
        client.on_message = self._on_message
        self.publish_status("idle")

    def _on_message(self, client, userdata, msg):
        payload_text = msg.payload.decode()
        
        # Ignorer les messages vides
        if not payload_text.strip():
            return
        
        try:
            data = json.loads(payload_text)
        except json.JSONDecodeError:
            print(f"[{self.robot_name}] erreur: message JSON invalide: {payload_text}")
            return
        
        print(f"[{self.robot_name}] tâche reçue: {data}")
        self.publish_status("busy", task=data.get("task"))
        if self.on_task:
            try:
                self.on_task(data)
                self.publish_status("done", task=data.get("task"))
            except Exception as e:
                print(f"[{self.robot_name}] erreur: {e}")
                self.publish_status("error", task=data.get("task"), error=str(e))

    def publish_status(self, state, task=None, error=None):
        payload = {"state": state}
        if task:
            payload["task"] = task
        if error:
            payload["error"] = error
        self.client.publish(self.status_topic, json.dumps(payload))

    def run_forever(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()