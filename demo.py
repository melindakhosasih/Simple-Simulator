import cv2
import argparse
from simulator.basic import BasicSimulator as Simulator
from simulator.utils import ControlState

def navigate():
    print("="*50)
    print("CONTROL MANUAL")
    print("[W] Move Forward")
    print("[A] Turn Left")
    print("[S] Move Backward")
    print("[D] Turn Right")
    print("[ESC] Exit")
    print("="*50)
    
    simulator = Simulator()
    simulator.init_state((256, 256, 0))

    while True:
        key = cv2.waitKey(1)

        if key == ord("w") or key == ord("W"):
            # print("move forward")
            cmd = ControlState(args.simulator, simulator.cstate.v+4, None)
        elif key == ord("a") or key == ord("A"):
            # print("turn left")
            cmd = ControlState(args.simulator, None, simulator.cstate.w-4)
        elif key == ord("s") or key == ord("S"):
            # print("move backward")
            cmd = ControlState(args.simulator, simulator.cstate.v-4, None)
        elif key == ord("d") or key == ord("D"):
            # print("turn right")
            cmd = ControlState(args.simulator, None, simulator.cstate.w+4)
        elif key == 27: # ESC button
            # print("exit")
            break
        else:
            cmd = ControlState(args.simulator, None, None)
        
        simulator.step(cmd)
        print(simulator, end="\r")
        img = simulator.render()
        cv2.imshow("demo", img)
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulator", type=str, default="basic", help="basic")
    args = parser.parse_args()

    if args.simulator == "basic":
        navigate()
        pass
    else:
        raise NameError("Unknown Simulator")
        