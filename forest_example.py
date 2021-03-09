# forest_example.py by CoccaGuo at 2021/03/08 23:01

from world import World
from vector3d import V, Velocity
from with_rule import WithRule
from prey import Prey
from predator import Predator
from rules import CatchRule, EscapeRule, PrintRule
from random import randint
import matplotlib.pyplot as plt


""" 
这个模型希望构建一个简单的食物链来演示森林中的捕食现象。基于以下规则(调整了一些)：
1. 狼吃羊
2. 狼会在一定范围内寻找羊，羊在一定范围内感受到威胁
3. 吃羊肉可以恢复狼的生命值，不吃东西生命值会掉
4. 羊会老死，同时也会在地图上刷新
5. 在狼吃饱的时候会考虑繁殖后代

具体基于以下参数设定：
1. PlotRule: 地图大小为500*500
2. HPDownRule: 羊和狼初始都有animal.hp点血，每个tick狼下降0.5点血，羊下降0.5点血，hp为0死亡
3. HPEatRule: 吃一个羊回复20点血
4. BorderRule: 逃到地图外的羊会消失
5. SpawnRule: 羊在地图每5个tick刷新出一只，狼每50个tick刷新一只
6. ReproduceRule: 狼血量大于90时会寻找周围50范围内的狼，并且在血量大于70时进行繁殖，出生1~2匹狼。
7. InitRule: 初始时在地图上随机生成10只狼和50只羊

"""
BORDER_SETUP = (500, 0, 500, 0)

class HPDownRule(WithRule):
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world

    def rule(self):
        prey_list = list(filter(lambda obj: isinstance(obj, Prey), self.world.objects))
        predator_list = list(filter(lambda obj: isinstance(obj, Predator), self.world.objects))
        
        for sheep in prey_list:
            sheep.hp = sheep.hp - 0.5
            if sheep.hp == 0:
                self.world.remove_object(sheep)
        
        for wolf in predator_list:
            wolf.hp = wolf.hp - 0.5
            if wolf.hp == 0:
                self.world.remove_object(wolf)


class HPEatRule(WithRule):
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world

    def rule(self):
        prey_list = list(filter(lambda obj: isinstance(obj, Prey), self.world.objects))
        predator_list = list(filter(lambda obj: isinstance(obj, Predator), self.world.objects))
        
        # predator-wised aim decide
        for predator in predator_list:
            for prey in prey_list:
                distance = predator.position.distance(prey.position)
                if distance < 1: #  too close, will be eaten!
                    try:
                        self.world.remove_object(prey)
                    except ValueError:
                        pass
                    predator.hp = predator.hp + 20
                    if predator.hp > 100:
                        predator.hp == 100


class BorderRule(WithRule):
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world
    
    def rule(self):
        prey_list = list(filter(lambda obj: isinstance(obj, Prey), self.world.objects))
        predator_list = list(filter(lambda obj: isinstance(obj, Predator), self.world.objects))

        for sheep in prey_list:
            if sheep.position.x > BORDER_SETUP[0] or sheep.position.x < BORDER_SETUP[1]:
                self.world.remove_object(sheep)
                return
            if sheep.position.y > BORDER_SETUP[2] or sheep.position.y < BORDER_SETUP[3]:
                self.world.remove_object(sheep)
                return


class SpawnRule(WithRule):
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world
    
    def rule(self):
        if self.world.now % 5 == 0:
            x = randint(BORDER_SETUP[1], BORDER_SETUP[0])
            y = randint(BORDER_SETUP[3], BORDER_SETUP[2])
            self.world.add_object(Prey(position=V(x, y), velocity=V(0, 0), name="sheep"))

        if self.world.now % 50 == 0:
            x = randint(BORDER_SETUP[1], BORDER_SETUP[0])
            y = randint(BORDER_SETUP[3], BORDER_SETUP[2])
            self.world.add_object(Predator(position=V(x, y), velocity=V(0, 0), name="wolf"))


class ReproduceRule(WithRule):
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world

    def rule(self):
        predator_list = list(filter(lambda obj: isinstance(obj, Predator), self.world.objects))

        for wolf in predator_list:
            if wolf.hp < 70: return
            distance = []
            for other_wolf in predator_list:
                distance.append(wolf.position.distance(other_wolf.position))
            if len(distance) == 0:
                return
            min_distance = sorted(distance)[1] # decide by distance, exclude itself
            ideal = predator_list[distance.index(min_distance)]
            if min_distance < 1:
                if wolf.hp > 70:
                    self.world.add_object(Predator(position=wolf.position, velocity=V(0,0), name="wolf"))
                    wolf.hp = wolf.hp - 20
                    ideal.hp = ideal.hp - 20
                return
            wolf_speed = 0.5
            orient = ideal.position.minus(wolf.position).normalize()
            velocity = orient.mul(wolf_speed)
            wolf.move(velocity)


class InitRule(WithRule):
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world

    def rule(self):
        if self.world.now == 0:
            for i in range(50):
                x = randint(BORDER_SETUP[1], BORDER_SETUP[0])
                y = randint(BORDER_SETUP[3], BORDER_SETUP[2])
                hp = randint(60, 100)
                self.world.add_object(Prey(position=V(x, y), velocity=V(0, 0), name="sheep", hp=hp))
            
            for i in range(10):
                x = randint(BORDER_SETUP[1], BORDER_SETUP[0])
                y = randint(BORDER_SETUP[3], BORDER_SETUP[2])
                self.world.add_object(Predator(position=V(x, y), velocity=V(0, 0), name="wolf"))


class PlotRule(WithRule):
    # visualization
    def __init__(self, world, limit=0) -> None:
        super().__init__()
        self.world = world
        self.wolf_counter = [0, 0]
        self.sheep_counter = [0, 0]
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

        plt.subplot(2, 2, 1)
        self.sheep_counter[0] = self.sheep_counter[1]
        self.sheep_counter[1] = len(prey_list)
        plt.plot([self.world.now-1, self.world.now], self.sheep_counter, 'k')
        plt.xlabel("sheep")

        plt.subplot(2, 2, 2)
        self.wolf_counter[0] = self.wolf_counter[1]
        self.wolf_counter[1] = len(predator_list)
        plt.plot([self.world.now-1, self.world.now], self.wolf_counter, 'k')
        plt.xlabel("wolf")

        plt.subplot(2, 2, 3)
        for obj in prey_list:
            plt.plot(obj.position.x, obj.position.y, 'ko', MarkerSize=3)
            plt.text(obj.position.x, obj.position.y, obj.hp, FontSize=8)
        for obj in predator_list:
            plt.plot(obj.position.x, obj.position.y, 'rx', MarkerSize=3)
            plt.text(obj.position.x, obj.position.y, obj.hp, FontSize=8)
        plt.text(self.x_min, self.y_max, "tick: {}".format(self.world.now))
        plt.pause(0.05)
        plt.cla()

        if self.world.now == (self.world.ticks-1):
            plt.show()



if __name__ == '__main__':
    world = World(ticks=1000, objects=[])
    world.rule.add_rules([
        InitRule(world),
        HPDownRule(world),
        CatchRule(world), 
        EscapeRule(world), 
        HPEatRule(world), 
        BorderRule(world),
        SpawnRule(world),
        ReproduceRule(world),
        PrintRule(world),
        PlotRule(world, limit=BORDER_SETUP)
        ])
    world.start()