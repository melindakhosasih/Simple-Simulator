import numpy as np

from simulator.utils import State, ControlState
from agents.base import AgentModel

class BasicAgent(AgentModel):
    def __init__(self, dt) -> None:
        self.dt = dt
        self.img = None

    def agent_visualize(self, img):
        self.img = img

    def step(self, state:State, cstate:ControlState) -> State:
        v = cstate.v
        w = cstate.w
        x = state.x + v * np.cos(np.deg2rad(state.yaw)) * self.dt
        y = state.y + v * np.sin(np.deg2rad(state.yaw)) * self.dt
        yaw = (state.yaw + state.w * self.dt) % 360
        return State(x, y, yaw, v, w)