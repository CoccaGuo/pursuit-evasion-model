# time.py by CoccaGuo at 2021/03/07 18:19
# interface WithTime. Any class implements this interface could deal with time.
# This interface should be used in World in tick refresh.
class WithTime:

    #interface method
    def next_tick(self):
        pass


# use to register instances with WithTime interface
class TimeObserver:
    
    def __init__(self) -> None:
        self.object_list = []

    # register
    def with_time(self, object: WithTime):
        self.object_list.append(object)

    # cancel register
    def cancel_with_time(self, object: WithTime):
        self.object_list.remove(object)

    # time refreshes
    def next_tick(self):
        for instance in self.object_list:
            instance.next_tick()