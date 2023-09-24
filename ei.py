from abc import ABC, abstractmethod
from datetime import datetime

# Behavioral Pattern: Observer Pattern
class Observer(ABC):
    @abstractmethod
    def update(self):
        pass

class Device(Observer):
    def __init__(self, device_id, device_type, status='off', temperature=None):
        self.device_id = device_id
        self.device_type = device_type
        self.status = status
        self.temperature = temperature

    def turn_on(self):
        self.status = 'on'

    def turn_off(self):
        self.status = 'off'

    def update(self):
        if self.device_type == 'thermostat':
            print(f"{self.device_type.capitalize()} is set to {self.temperature} degrees.")
        else:
            print(f"{self.device_type.capitalize()} {self.device_id} is {self.status}.")

class Thermostat(Device):
    def __init__(self, device_id, temperature):
        super().__init__(device_id, 'thermostat', temperature=temperature)

class DoorLock(Device):
    def __init__(self, device_id):
        super().__init__(device_id, 'door', status='locked')

class SmartHomeHub:
    def __init__(self):
        self.devices = {}
        self.scheduled_tasks = []
        self.automated_triggers = []

    def add_device(self, device):
        self.devices[device.device_id] = device

    def turn_on(self, device_id):
        if device_id in self.devices:
            self.devices[device_id].turn_on()

    def turn_off(self, device_id):
        if device_id in self.devices:
            self.devices[device_id].turn_off()

    def set_schedule(self, device_id, time, action):
        self.scheduled_tasks.append({
            'device': device_id,
            'time': time,
            'action': action
        })

    def add_trigger(self, condition, operator, value, action):
        self.automated_triggers.append({
            'condition': condition,
            'operator': operator,
            'value': value,
            'action': action
        })

    def run_scheduled_tasks(self):
        current_time = datetime.now().strftime("%H:%M")
        for task in self.scheduled_tasks:
            if task['time'] == current_time:
                eval(f'self.{task["action"]}')

# Example usage
if __name__ == "__main__":
    hub = SmartHomeHub()

    devices = [
        {'id': 1, 'type': 'light', 'status': 'off'},
        {'id': 2, 'type': 'thermostat', 'temperature': 70},
        {'id': 3, 'type': 'door', 'status': 'locked'}
    ]

    for device_data in devices:
        if device_data['type'] == 'thermostat':
            device = Thermostat(device_data['id'], device_data['temperature'])
        else:
            device = Device(device_data['id'], device_data['type'], status=device_data['status'])
        hub.add_device(device)

    commands = [
        'turn_on(1)',
        'set_schedule(2, "06:00", "turn_on(1)")',
        'add_trigger("temperature", ">", 75, "turn_off(1)")'
    ]

    for command in commands:
        eval(f'hub.{command}')

    print("Status Report:")
    for device in hub.devices.values():
        device.update()

    print("Scheduled Tasks:")
    print(hub.scheduled_tasks)

    print("Automated Triggers:")
    print(hub.automated_triggers)



