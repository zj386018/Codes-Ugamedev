from typing import Dict, List


class ResourceManager:
    def __init__(self):
        self.resources: Dict[str, int] = {
            "wood": 100,
            "stone": 50,
            "gold": 20,
            "food": 80,
        }
        self.resource_caps: Dict[str, int] = {
            "wood": 500,
            "stone": 500,
            "gold": 200,
            "food": 300,
        }
        self.population = 0
        self.max_population = 10

    def add_resource(self, resource_type: str, amount: int):
        if resource_type in self.resources:
            cap = self.resource_caps.get(resource_type, 9999)
            self.resources[resource_type] = min(
                self.resources[resource_type] + amount, cap
            )

    def spend_resource(self, resource_type: str, amount: int) -> bool:
        if resource_type in self.resources and self.resources[resource_type] >= amount:
            self.resources[resource_type] -= amount
            return True
        return False

    def can_afford(self, cost: Dict[str, int]) -> bool:
        for res_type, amount in cost.items():
            if self.resources.get(res_type, 0) < amount:
                return False
        return True

    def spend(self, cost: Dict[str, int]) -> bool:
        if not self.can_afford(cost):
            return False
        for res_type, amount in cost.items():
            self.spend_resource(res_type, amount)
        return True

    def increase_cap(self, resource_type: str, bonus: int):
        if resource_type in self.resource_caps:
            self.resource_caps[resource_type] += bonus

    def add_population_cap(self, bonus: int):
        self.max_population += bonus
