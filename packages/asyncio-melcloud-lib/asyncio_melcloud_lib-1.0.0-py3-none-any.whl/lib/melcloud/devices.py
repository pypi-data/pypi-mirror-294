from lib.melcloud.jsongenerator import MelcloudJsonGenerator


class Device():
    def __init__(self):
        self.building_id = None
        self.device_id = None
        self.device_name = None
        self.jsonGenerator = MelcloudJsonGenerator()
        self.settings = None

    async def set_device_id(self, building_id, device_id, device_name):
        self.building_id = building_id
        self.device_id = device_id
        self.device_name = device_name
        self.settings = await self.jsonGenerator.generate()
    
    async def get_settings(self):
        return self.settings
    
    async def set_device_settings(self, data):
        self.settings = await self.jsonGenerator.update(data)

    async def update_device(self,data):
        self.settings = await self.jsonGenerator.update(data)
    
    async def update_device_settings(self):
        self.settings = await self.jsonGenerator.p_update()

    async def create_device_dict(self):
        return {
            "BuildingID": self.building_id,
            "DeviceID": self.device_id,
            "DeviceName": self.device_name,
            "Settings": self.settings
        }
    async def print_device_dict(self):
        device_dict = await self.create_device_dict()
        print(device_dict)

    async def get_settings_dict(self):
        return self.settings
    
    async def create_request(self):
        return await self.jsonGenerator.generate_request()
    

  


