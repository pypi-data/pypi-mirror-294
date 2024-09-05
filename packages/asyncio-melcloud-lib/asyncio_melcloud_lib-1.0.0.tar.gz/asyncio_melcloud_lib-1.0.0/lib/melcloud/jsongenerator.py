import json
from enum import Enum

class EffectiveFlags(Enum):
    CHANGE_FANSPEED = 8
    CHANGE_OPERATION_MODE = 2
    CHANGE_TEMPRATURE = 4
    CHANGE_VANE_HORISONTAL = 256
    CHANGE_VANE_VERTICAL = 16
    CHANGE_POWER = 1

class OperationMode(Enum):
    HEAT = 1
    DRY = 2
    COOL = 3
    FAN = 7
    AUTO = 8


class JsonGenerator:
    def __init__(self, data):
        self.data = data
        self.request_data = None

    async def generate(self):
        return self.data
    
    async def generate_requestdata(self):
        return self.request_data
    
    
class MelcloudJsonGenerator(JsonGenerator):
    def __init__(self):
        self.type ="MelCloud_Device"
        self.power = "false"
        self.device_id = 0
        self.room_temperature = 0
        self.set_temperature = 0
        self.set_fan_speed = 0
        self.operation_mode = 0
        self.vane_horizontal = 0
        self.vane_vertical = 0
        self.effective_flags = 0
        self.request_data = None

        
    async def generate(self):
        self.data = {
            "Power": self.power,
            "DeviceID": self.device_id,
            "RoomTemperature": self.room_temperature,   
            "SetTemperature": self.set_temperature,
            "SetFanSpeed": self.set_fan_speed,
            "OperationMode": self.operation_mode,
            "VaneHorizontal": self.vane_horizontal,
            "VaneVertical": self.vane_vertical
        }
        return await super().generate()
    
    async def generate_request(self):
        self.request_data ={
            "EffectiveFlags": self.effective_flags,
            "Power": self.power,
            "RoomTemperature": self.room_temperature,
            "DeviceID": self.device_id,
            "SetTemperature": self.set_temperature,
            "SetFanSpeed": self.set_fan_speed,
            "OperationMode": self.operation_mode,
            "VaneHorizontal": self.vane_horizontal,
            "VaneVertical": self.vane_vertical
        }
        return await super().generate_requestdata()
    
    async def p_update(self):
        return await self.generate()
    
    async def update(self, data):
        self.device_id = data["DeviceID"]
        self.power = data["Power"]
        self.set_temperature = data["SetTemperature"]
        self.room_temperature = data["RoomTemperature"]
        self.set_fan_speed = data["SetFanSpeed"]
        self.operation_mode = data["OperationMode"]
        self.vane_horizontal = data["VaneHorizontal"]
        self.vane_vertical = data["VaneVertical"]
        return await self.generate()
    
    async def set_EffectiveFlags(self, flags: EffectiveFlags):
        self.effective_flags = flags
        return await self.generate()
    
    async def set_new_roomtemperature(self, set_temperature: float):
        self.set_temperature = set_temperature
        return await self.generate()
    
    async def set_new_fanspeed(self, fanspeed: int):
        self.set_fan_speed = fanspeed
        return await self.generate()
    
    async def set_new_operation_mode(self, operation_mode: OperationMode):
        self.operation_mode = operation_mode
        return await self.generate()
    
    async def set_new_power_state(self, power):
        self.power = power
        return await self.generate()
    
    async def set_new_vane_horizontal(self, vane_horizontal: int):
        self.vane_horizontal = vane_horizontal
        return await self.generate()
    
    async def set_new_vane_vertical(self, vane_vertical: int):
        self.vane_vertical = vane_vertical
        return await self.generate()
    
    async def generate_request(self):
        self.request_data ={
            "EffectiveFlags": self.effective_flags,
            "Power": self.power,
            "DeviceID": self.device_id,
            "RoomTemperature": self.room_temperature,
            "SetTemperature": self.set_temperature,
            "SetFanSpeed": self.set_fan_speed,
            "OperationMode": self.operation_mode,
            "VaneHorizontal": self.vane_horizontal,
            "VaneVertical": self.vane_vertical,
            "NumberOfFanSpeeds": 5,
            "LocalIPAddress": None
        }
        return self.request_data
