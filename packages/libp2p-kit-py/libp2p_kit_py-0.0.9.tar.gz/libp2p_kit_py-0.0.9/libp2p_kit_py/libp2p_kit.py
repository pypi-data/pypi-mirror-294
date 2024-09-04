from libp2p_kit import libp2p_kit
from aria2_kit import aria2_kit
from s3_kit import s3_kit
from websocket_kit import websocket_kit
from websocket_kit import websocket_kit_lib

class libp2p_kit_py:
    def __init__(self, resources, metadata):
        self.libp2p_kit = libp2p_kit(resources, metadata)
        self.aria2_kit = aria2_kit(resources, metadata)
        self.s3_kit = s3_kit(resources, metadata)
        self.websocket_kit = websocket_kit(resources, metadata)
        self.websocket_kit_lib = websocket_kit_lib(resources, metadata)

    def run(self):

        return True
    
    