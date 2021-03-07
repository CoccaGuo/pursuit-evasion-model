# rules.py by CoccaGuo at 2021/03/07 20:40

from with_rule import WithRule

# use to print results on screen
class PrintRule(WithRule):
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world

    def rule(self):
        print("-----time: ", self.world.now, "-----")
        for obj in self.world.objects:
           print(obj.name, obj.position.string())
        print("-------------------\n")
