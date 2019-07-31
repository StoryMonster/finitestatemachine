from fsm_exceptions import FsmException
from state import FsmState, FsmFinalState
from collections import namedtuple
import logging

Transaction = namedtuple("Transaction", ["prev_state", "event", "next_state"])

class FSM:
    def __init__(self, context):
        self.context = context
        self.state_transaction_table = []
        self.global_transaction_table = []
        self.current_state = None
        self.working_state = FsmState

    def add_global_transaction(self, event, end_state):     # 全局转换，直接进入到结束状态
        if not issubclass(end_state, FsmFinalState):
            raise FsmException("The state should be FsmFinalState")
        self.global_transaction_table.append(Transaction(self.working_state, event, end_state))

    def add_transaction(self, prev_state, event, next_state):
        if issubclass(prev_state, FsmFinalState):
            raise FsmException("It's not allowed to add transaction after Final State Node")
        self.state_transaction_table.append(Transaction(prev_state, event, next_state))

    def process_event(self, event):
        for transaction in self.global_transaction_table:
            if isinstance(event, transaction.event):
                self.current_state = transaction.next_state()
                self.current_state.enter(event, self)
                self.clear_transaction_table()
                return
        for transaction in self.state_transaction_table:
            if isinstance(self.current_state, transaction.prev_state) and isinstance(event, transaction.event):
                self.current_state.exit(self.context)
                self.current_state = transaction.next_state()
                self.current_state.enter(event, self)
                if isinstance(self.current_state, FsmFinalState):
                    self.clear_transaction_table()
                return
        raise FsmException("Transaction not found")
    
    def clear_transaction_table(self):
        self.global_transaction_table = []
        self.state_transaction_table = []
        self.current_state = None

    def run(self):
        if len(self.state_transaction_table) == 0: return
        self.current_state = self.state_transaction_table[0].prev_state()
        self.current_state.enter(None, self)

    def isRunning(self):
        return self.current_state is not None

    def next_state(self, event):
        for transaction in self.global_transaction_table:
            if isinstance(event, transaction.event):
                return transaction.next_state
        for transaction in self.state_transaction_table:
            if isinstance(self.current_state, transaction.prev_state) and isinstance(event, transaction.event):
                return transaction.next_state
        return None
