# rules.py by CoccaGuo at 2021/03/07 20:40

from vector3d import V, Velocity
from with_rule import WithRule
from prey import Prey
from predator import Predator
import matplotlib.pyplot as plt

  
class CatchRule(WithRule):
    # predators will find its way to catch the prey.
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world

    def rule(self):
        # distinct prey and predator
        prey_list = list(filter(lambda obj: isinstance(obj, Prey), self.world.objects))
        predator_list = list(filter(lambda obj: isinstance(obj, Predator), self.world.objects))
        
        # predator-wised aim decide
        for predator in predator_list:
            # find the nearest prey
            distance = []
            for prey in prey_list:
                distance.append(predator.position.distance(prey.position))
            if len(distance) == 0:
                return
            min_distance = min(distance) # decide by distance
            aim_prey = prey_list[distance.index(min_distance)]
            predator_speed = 1
            orient = aim_prey.position.minus(predator.position).normalize()
            velocity = orient.mul(predator_speed)
            predator.move(velocity)


class EscapeRule(WithRule):
    # preys should escape
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world

    def rule(self):
        # distinct prey and predator
        prey_list = list(filter(lambda obj: isinstance(obj, Prey), self.world.objects))
        predator_list = list(filter(lambda obj: isinstance(obj, Predator), self.world.objects))
        for prey in prey_list:
            danger_objs = []
            for predator in predator_list:
                distance = prey.position.distance(predator.position)
                if distance < 13: # start to run 
                    danger_objs.append(predator)
            # rules on how to escape:
            orient = V(0, 0, 0)
            for danger_obj in danger_objs:
                escape_orient = prey.position.minus(danger_obj.position).normalize()
                orient = orient.add(escape_orient)
            orient = orient.normalize()

            escape_speed = 0.5
            escape_velocity = orient.mul(escape_speed)
            prey.move(escape_velocity)



class EatRule(WithRule):
    # how preys eaten
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world

    def rule(self):
        # distinct prey and predator
        prey_list = list(filter(lambda obj: isinstance(obj, Prey), self.world.objects))
        predator_list = list(filter(lambda obj: isinstance(obj, Predator), self.world.objects))
        
        # predator-wised aim decide
        for predator in predator_list:
            for prey in prey_list:
                distance = predator.position.distance(prey.position)
                if distance < 1: #  too close, will be eaten!
                    self.world.remove_object(prey)



class PrintRule(WithRule):
    # print results on screen
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world

    def rule(self):
        print("-----time: ", self.world.now, "-----")
        for obj in self.world.objects:
           print(obj.name, obj.position.string())
        print("-------------------\n")


class PlotRule(WithRule):
    # visualization
    def __init__(self, world, limit=0) -> None:
        super().__init__()
        self.world = world
        if limit == 0:
            self.x_max = max([obj.position.x for obj in self.world.objects])
            self.x_min = min([obj.position.x for obj in self.world.objects])
            self.y_max = max([obj.position.y for obj in self.world.objects])
            self.y_min = min([obj.position.y for obj in self.world.objects])
        else:
            self.x_max = limit[0]
            self.x_min = limit[1]
            self.y_max = limit[2]
            self.y_min = limit[3]
    

    def rule(self):
        prey_list = list(filter(lambda obj: isinstance(obj, Prey), self.world.objects))
        predator_list = list(filter(lambda obj: isinstance(obj, Predator), self.world.objects))

        plt.xlim(self.x_min*1.1, self.x_max*1.1)
        plt.ylim(self.y_min*1.1, self.y_max*1.1)
        plt.axis("off")

        for obj in prey_list:
            plt.plot(obj.position.x, obj.position.y, 'kx')
            plt.text(obj.position.x, obj.position.y, obj.name)
        for obj in predator_list:
            plt.plot(obj.position.x, obj.position.y, 'ko')
            plt.text(obj.position.x, obj.position.y, obj.name)
        plt.text(self.x_min, self.y_max, "tick: {}".format(self.world.now))
        plt.pause(0.05)
        plt.cla()
        if self.world.now == (self.world.ticks-1):
            plt.show()