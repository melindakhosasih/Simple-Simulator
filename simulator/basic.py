import cv2
import scipy
import numpy as np

from simulator.base import Simulator
from simulator.utils import ControlState, State, paste_overlapping_image

from agents.basic import BasicAgent

class BasicSimulator(Simulator):
    def __init__(self,
                 v_limit=20,
                 w_limit=20,
                 dt=0.5):
        # Agent Type
        self.control_type = "basic"

        # Agent Speed limit
        self.v_limit = v_limit
        self.w_limit = w_limit

        # Initialize Agent
        self.agent = BasicAgent(dt)

        # Initialize State
        self.state = State()
        self.cstate = ControlState(self.control_type, 0.0, 0.0)

    def __str__(self) -> str:
        return self.state.__str__() + " " + self.cstate.__str__()

    def init_state(self, pose):
        self.state.update(x=pose[0], y=pose[1], yaw=pose[2])
        # self.max_len = 1000
        self.history = []
        
        try:
            img = cv2.imread("./agents/visualization/512x512.png", cv2.IMREAD_UNCHANGED)
            img = cv2.resize(img, (25, 25))
            # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # gray_img_3d = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
            self.agent.agent_visualize(img)
        except Exception as e:
            print(f"Error loading agent image: {e}")
        
        return self.state, {}
    
    def step(self, cmd, update_state=True):
        if cmd is not None:
            # self.cstate.v = cmd.v if cmd.v is not None else self.cstate.v
            self.cstate.v = cmd.v if cmd.v is not None else 0
            # self.cstate.w = cmd.w if cmd.w is not None else self.cstate.w
            self.cstate.w = cmd.w if cmd.w is not None else 0

        # Control Constraint
        if self.cstate.v > self.v_limit:
            self.cstate.v = self.v_limit
        elif self.cstate.v < -self.v_limit:
            self.cstate.v = -self.v_limit
        if self.cstate.w > self.w_limit:
            self.cstate.w = self.w_limit
        elif self.cstate.w < -self.w_limit:
            self.cstate.w = -self.w_limit

        state_next = self.agent.step(self.state, self.cstate)
        if update_state:
            self.state = state_next
            self.history.append((self.state.x, self.state.y, self.state.yaw))

        return state_next, {}
    
    def render(self, map=None):
        if map is None:
            map = np.ones((512, 512, 3))
        
        # Draw Trajectory
        # start = 0 if len(self.history) < self.max_len else len(self.history) - self.max_len
        
        color = (0/255, 97/255, 255/255)
        for i in range(0, len(self.history)-1):
            cv2.line(map, (int(self.history[i][0]), int(self.history[i][1])), (int(self.history[i+1][0]), int(self.history[i+1][1])), color, 1)

        if self.agent.img is not None:
            rotated_agent = scipy.ndimage.interpolation.rotate(
                self.agent.img, self.state.yaw + 90
            )
            rotated_agent = np.fliplr(rotated_agent)
            map = paste_overlapping_image(map, rotated_agent, (int(self.state.y), int(self.state.x)))

        return map
        