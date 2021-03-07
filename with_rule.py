# with_rule.py by CoccaGuo at 2021/03/07 18:59
# interface WithRule. Any class implements this interface could deal with the rule of the world.
from with_time import WithTime


class WithRule:

    #interface method
    def rule(self):
        pass


# use to register instances with WithRule interface
class RuleObserver(WithTime):
    
    def __init__(self) -> None:
        self.rule_list = []

    # register
    def add_rule(self, rule: WithRule):
        self.rule_list.append(rule)
    
    def add_rules(self, rules):
        self.rule_list = self.rule_list + rules

    # cancel register
    def cancel_rule(self, rule: WithRule):
        self.rule_list.remove(rule)

    # because implemented WithTime
    def next_tick(self):
        for rule in self.rule_list:
            rule.rule()