# world.py by CoccaGuo at 2021/03/07 19:02
from with_rule import RuleObserver
from with_time import TimeObserver


class World:
    
    def __init__(self, time =TimeObserver(), rule=RuleObserver(), ticks=100, objects=[]):
        self.time = time
        self.rule = rule
        self.ticks = ticks
        self.objects = objects
        self.now = 0
        self.time.with_time(rule) # add rule list into the calculation of time

    def add_object(self, obj):
        self.objects.append(obj)
        self.time.with_time(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)
        self.time.cancel_with_time(obj)

    def start(self):
        for obj in self.objects:
            self.time.with_time(obj)
        for tick in range(self.ticks):
            self.now = tick
            self.time.next_tick()

