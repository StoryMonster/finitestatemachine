

class FsmState:
    def enter(self, event, fsm):
        pass
    
    def exit(self, fsm):
        pass

class FsmFinalState:
    def enter(self, event, fsm):
        pass

class DefaultInitState(FsmState):
    pass