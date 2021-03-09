# examples.py by CoccaGuo at 2021/03/07 19:53
import sys
sys.path.append("..")

from predator import Predator
from rules import CatchRule, EatRule, EscapeRule, PlotRule, PrintRule
from with_rule import WithRule
from world import World
from prey import Prey
from vector3d import V
from random import random


def example01():
    dear_a = Prey(name="a", velocity=V(1, 0), position=V(0, 0))
    prey_list = [dear_a] # define an object list for the world
    # create a world
    world = World(ticks=40, objects=prey_list) 
    # add a simple rule for print the result
    world.rule.add_rules([PrintRule(world)]) 
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


    dear_a = Prey(name="a", velocity=V(0, 0), position=V(10, 10))
    dear_b = Prey(name="b", velocity=V(1, 1), position=V(0, 0))
    prey_list = [dear_a, dear_b]
    
    world = World(ticks=40, objects=prey_list)
    world.rule.add_rules([RandomWalkRule(world), PrintRule(world)])
    world.start()


def example03():
    dear1 = Prey(name="dear1", velocity=V(0, 0), position=V(10, 20))
    dear2 = Prey(name="dear2", velocity=V(0, 0), position=V(20, -10))
    dear3 = Prey(name="dear3", velocity=V(0, 0), position=V(0, 5))
    dear4 = Prey(name="dear4", velocity=V(0, 0), position=V(15, -10))
    dear5 = Prey(name="dear5", velocity=V(0, 0), position=V(-15, 0))
    wolf1 = Predator(name="wolf1", velocity=V(0, 0), position=V(-10, 10))
    wolf2 = Predator(name="wolf2", velocity=V(0, 0), position=V(15, 0))
    obj_list = [dear1, dear2, dear3, dear4, dear5, wolf1, wolf2]
    
    world = World(ticks=100, objects=obj_list)
    world.rule.add_rules([
        CatchRule(world), 
        EscapeRule(world), 
        EatRule(world), 
        PrintRule(world), 
        PlotRule(world, limit=(50, -20, 30, -30))
        ])
    world.start()

example03()