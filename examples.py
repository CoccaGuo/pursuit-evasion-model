# examples.py by CoccaGuo at 2021/03/07 19:53
from rules import PrintRule
from with_rule import WithRule
from world import World
from prey import Prey
from vector3d import V
from random import random


def example01():
    dear_a = Prey(name="a", velocity=V(1, 0), position=V(0, 0))
    prey_list = [dear_a] # define an object list for the world
    # create a world
    world = World(ticks=4, objects=prey_list) 
    # add a simple rule for print the result
    world.rule.add_rule(PrintRule(world))
    world.start()


def example02():
    # define a new rule for random walk. 
    # rules should impliment WithRule interface and be added in world rule list.
    class RandomWalkRule(WithRule):
        def __init__(self, world) -> None:
            super().__init__()
            self.world = world

        def rule(self):
            for obj in self.world.objects:
                obj.move(V(random()-0.5, random()-0.5))


    dear_a = Prey(name="a", velocity=V(0, 0), position=V(0, 0))
    dear_b = Prey(name="b", velocity=V(1, 1), position=V(0, 0))
    prey_list = [dear_a, dear_b]
    
    world = World(ticks=4, objects=prey_list)
    world.rule.add_rules([RandomWalkRule(world), PrintRule(world)])
    world.start()

example02()