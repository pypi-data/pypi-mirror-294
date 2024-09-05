import aiohttp
import logging
from .devices import Device
from .jsongenerator import OperationMode
from .jsongenerator import EffectiveFlags

log  = logging.getLogger(__name__)

class MelcloudClient:
    def __init__(self, username, password):
        self.base_url = "https://app.melcloud.com/Mitsubishi.Wifi.Client/"
        self.username = username
        self.password = password
        self.session = None
        self.contextKey = None
        self.devices = []

    async def login(self):
        self.session = aiohttp.ClientSession()
        url = f"{self.base_url}Login/ClientLogin"
        data = {
            "Email": self.username,
            "Password": self.password,
            "AppVersion": "1.34.10.0"
        }

        async with self.session.post(url, json=data) as response:
            if response.status != 200:
                logging.error(f"Error: Received status code {response.status}")
                return False
            if 'application/json' not in response.headers.get('Content-Type', ''):
                logging.error(f"Error: Unexpected content type {response.headers.get('Content-Type')}")
                return False
            try:
                j = await response.json()
                self.contextKey = j["LoginData"]["ContextKey"]
                return self.contextKey
            except aiohttp.client_exceptions.ContentTypeError as e:
                logging.error(f"Error: {e}")
                return False

    async def get_devices(self):
        url = f"{self.base_url}User/ListDevices"
        headers = {"X-MitsContextKey": self.contextKey,"Content-Type": "application/json"}
    
        async with self.session.get(url, headers=headers) as response:
            if response.status != 200:
                logging.error(f"Error: Received status code {response.status}")
                return []
            if 'application/json' not in response.headers.get('Content-Type', ''):
                logging.error(f"Error: Unexpected content type {response.headers.get('Content-Type')}")
                return []
            try:
                j = await response.json()
                for device in j:
                    d = Device()
                    await d.set_device_id(device['Structure']['Devices'][0]['BuildingID'], 
                                          device['Structure']['Devices'][0]['DeviceID'], 
                                          device['Structure']['Devices'][0]['DeviceName'])

                    self.devices.append(d)
                log.info(f"Devices loaded. Found {len(self.devices)} devices")
            
            except aiohttp.client_exceptions.ContentTypeError as e:
                logging.error(f"Error: {e}")
                return []

    async def set_device_settings(self):
        headers = {"X-MitsContextKey": self.contextKey,"Content-Type": "application/json"}
        for device in self.devices:
            url = f"{self.base_url}Device/Get?id={device.device_id}&buildingID={device.building_id}"             
            async with self.session.get(url, headers=headers) as response:
                if response.status != 200:
                    logging.error(f"Error: Received status code {response.status}")
                    return []
                if 'application/json' not in response.headers.get('Content-Type', ''):
                        logging.error(f"Error: Unexpected content type {response.headers.get('Content-Type')}")
                        return []
                try:
                    j = await response.json()
                    data = {
                        "DeviceID": j['DeviceID'],
                        "Power": j['Power'],
                        "RoomTemperature": j['RoomTemperature'],
                        "SetTemperature": j['SetTemperature'],
                        "SetFanSpeed": j['SetFanSpeed'],
                        "OperationMode": j['OperationMode'],
                        "VaneHorizontal": j['VaneHorizontal'],
                        "VaneVertical": j['VaneVertical']
                    }
                    await device.set_device_settings(data)
                    log.info(f"Device settings for {device.device_name} set")
                    
                except aiohttp.client_exceptions.ContentTypeError as e:
                    logging.error(f"Error: {e}")
                    return []
                
    async def change_temp(self, deviceid, temperature: float):
        url = f"{self.base_url}Device/SetAta"
        headers = {"X-MitsContextKey":self.contextKey, "Content-Type":"application/json"}
        for device in self.devices:
            if device.device_id == deviceid:
                await device.jsonGenerator.set_new_roomtemperature(temperature)
                await device.jsonGenerator.set_EffectiveFlags(EffectiveFlags.CHANGE_TEMPRATURE.value)
                data = await device.create_request()
                async with self.session.post(url, headers=headers, json=data) as response:
                    if response.status != 200:
                        logging.error(f"Error: Received status code {response.status}")
                        return False
                    if 'application/json' not in response.headers.get('Content-Type', ''):
                        logging.error(f"Error: Unexpected content type {response.headers.get('Content-Type')}")
                        return False
                    try:
                        j = await response.json()
                        await device.update_device_settings()
                        log.info(f"Device temperature for {device.device_name} set to {temperature} C")
                    except aiohttp.client_exceptions.ContentTypeError as e:
                        logging.error(f"Error: {e}")
                        return False
                    
    async def change_mode(self, deviceid, mode: OperationMode):
        url = f"{self.base_url}Device/SetAta"
        headers = {"X-MitsContextKey":self.contextKey, "Content-Type":"application/json"}
        for device in self.devices:
            if device.device_id == deviceid:
                await device.jsonGenerator.set_new_operation_mode(mode)
                await device.jsonGenerator.set_EffectiveFlags(EffectiveFlags.CHANGE_OPERATION_MODE.value)
                data = await device.create_request()
                async with self.session.post(url, headers=headers, json=data) as response:
                    if response.status != 200:
                        logging.error(f"Error: Received status code {response.status}")
                        return False
                    if 'application/json' not in response.headers.get('Content-Type', ''):
                        logging.error(f"Error: Unexpected content type {response.headers.get('Content-Type')}")
                        return False
                    try:
                        j = await response.json()
                        await device.update_device_settings()
                        log.info(f"Device mode for {device.device_name} set to mode {mode}")
                    except aiohttp.client_exceptions.ContentTypeError as e:
                        logging.error(f"Error: {e}")
    
    async def change_fan_speed(self, deviceid, speed: int):
        url = f"{self.base_url}Device/SetAta"
        headers = {"X-MitsContextKey":self.contextKey, "Content-Type":"application/json"}
        for device in self.devices:
            if device.device_id == deviceid:
                await device.jsonGenerator.set_new_fanspeed(speed)
                await device.jsonGenerator.set_EffectiveFlags(EffectiveFlags.CHANGE_FANSPEED.value)
                data = await device.create_request()
                async with self.session.post(url, headers=headers, json=data) as response:
                    if response.status != 200:
                        logging.error(f"Error: Received status code {response.status}")
                        return False
                    if 'application/json' not in response.headers.get('Content-Type', ''):
                        logging.error(f"Error: Unexpected content type {response.headers.get('Content-Type')}")
                        return False
                    try:
                        j = await response.json()
                        await device.update_device_settings()
                        log.info(f"Device fan speed for {device.device_name} set to speed {speed}")
                    except aiohttp.client_exceptions.ContentTypeError as e:
                        logging.error(f"Error: {e}")
    
    async def change_vane_horizontal(self, deviceid, vane: int):
        url = f"{self.base_url}Device/SetAta"
        headers = {"X-MitsContextKey":self.contextKey, "Content-Type":"application/json"}
        for device in self.devices:
            if device.device_id == deviceid:
                await device.jsonGenerator.set_new_vane_horizontal(vane)
                await device.jsonGenerator.set_EffectiveFlags(EffectiveFlags.CHANGE_VANE_HORISONTAL.value)
                data = await device.create_request()
                async with self.session.post(url, headers=headers, json=data) as response:
                    if response.status != 200:
                        logging.error(f"Error: Received status code {response.status}")
                        return False
                    if 'application/json' not in response.headers.get('Content-Type', ''):
                        logging.error(f"Error: Unexpected content type {response.headers.get('Content-Type')}")
                        return False
                    try:
                        j = await response.json()
                        await device.update_device_settings()
                        log.info(f"Device vane horizontal for {device.device_name} set to {vane}")
                    except aiohttp.client_exceptions.ContentTypeError as e:
                        logging.error(f"Error: {e}")

    async def change_vane_vertical(self, deviceid, vane: int):
        url = f"{self.base_url}Device/SetAta"
        headers = {"X-MitsContextKey":self.contextKey, "Content-Type":"application/json"}
        for device in self.devices:
            if device.device_id == deviceid:
                await device.jsonGenerator.set_new_vane_vertical(vane)
                await device.jsonGenerator.set_EffectiveFlags(EffectiveFlags.CHANGE_VANE_VERTICAL.value)
                data = await device.create_request()
                async with self.session.post(url, headers=headers, json=data) as response:
                    if response.status != 200:
                        logging.error(f"Error: Received status code {response.status}")
                        return False
                    if 'application/json' not in response.headers.get('Content-Type', ''):
                        logging.error(f"Error: Unexpected content type {response.headers.get('Content-Type')}")
                        return False
                    try:
                        j = await response.json()
                        await device.update_device_settings()
                        log.info(f"Device vane vertical for {device.device_name} set to {vane}")
                    except aiohttp.client_exceptions.ContentTypeError as e:
                        logging.error(f"Error: {e}")

    async def change_power_state(self, deviceid, power):
        url = f"{self.base_url}Device/SetAta"
        headers = {"X-MitsContextKey":self.contextKey, "Content-Type":"application/json"}
        for device in self.devices:
            if device.device_id == deviceid:
                await device.jsonGenerator.set_new_power_state(power)
                await device.jsonGenerator.set_EffectiveFlags(EffectiveFlags.CHANGE_POWER.value)
                data = await device.create_request()
                async with self.session.post(url, headers=headers, json=data) as response:
                    if response.status != 200:
                        logging.error(f"Error: Received status code {response.status}")
                        return False
                    if 'application/json' not in response.headers.get('Content-Type', ''):
                        logging.error(f"Error: Unexpected content type {response.headers.get('Content-Type')}")
                        return False
                    try:
                        j = await response.json()
                        await device.update_device_settings()
                        log.info(f"Device power state for {device.device_name} set to {power}")
                    except aiohttp.client_exceptions.ContentTypeError as e:
                        logging.error(f"Error: {e}")
    
    

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None