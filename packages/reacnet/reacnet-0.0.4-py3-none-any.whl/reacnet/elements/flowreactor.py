from omnisoot import PlugFlowReactor
from reacnet.connectors import Connection
from reacnet.elements import ElementBase

class FlowReactor(ElementBase):
    def __init__(self, reactor, run_callback, call_back_config, name = ""):
        self.reactor = reactor;
        self._match_with_reactor();
        self.inlet = None;
        self._run_callback = run_callback;
        self._call_back_config = call_back_config;
        super().__init__(self.reactor.soot.soot_gas, name)
    
    
    def connect_inlet(self, inlet: Connection):
        self.inlet = inlet;
        self.reactor.inlet = inlet;
        inlet.downstream = self;
        
    def _match_with_reactor(self):
        self._X = self.reactor.X;
        self._Y = self.reactor.Y;
        self._T = self.reactor.T;
        self._P = self.reactor.P;
        self._soot = self.reactor.soot_array;
        self._mdot = self.reactor.mdot;

    def run(self):
        self._run_upstream();
        if self.verbose:
            self._start_message();
        self._run_callback(**self._call_back_config);
        self._match_with_reactor();
        if self.verbose:
            print(f"reactor {self.name} mdot is {self.reactor.mdot:0.5e}")
            self._success_message();