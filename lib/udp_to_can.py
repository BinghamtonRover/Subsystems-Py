import time 

from network import ProtoSocket, Device
from lib.constants import NAME_TO_CAN_ID

class UdpToCan(ProtoSocket):
	def __init__(self, port, subsystems): 
		self.subsystems = subsystems
		super().__init__(port, device=Device.SUBSYSTEMS)

	# Overriden from ProtoSocket
	def on_disconnect(self): 
		self.subsystems.can.stop_driving()
		super().on_disconnect()

	def update_settings(self, settings): 
		print(f"Changing status to {settings.status}")
		super().update_settings(settings)

	# Overriden from ProtoSocket
	def on_message(self, wrapper): 
		if len(wrapper.data) > 8: 
			print(f"{wrapper.name} is {len(wrapper.data)} bytes long, but CAN only supports 8")
		elif wrapper.name not in NAME_TO_CAN_ID: 
			print(f"No handler for {wrapper.name}")
		else: 
			id = NAME_TO_CAN_ID[wrapper.name]
			# print(f"Received UDP message {wrapper.name}, sending CAN message to {id}: {wrapper.data}")
			self.subsystems.can.send(id, wrapper.data)
