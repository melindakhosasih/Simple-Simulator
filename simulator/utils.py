import numpy as np
from typing import Optional

class ControlState():
    def __init__(self, type, *cstate):
        self.control_type = type
        if self.control_type == "basic":
            self.v = cstate[0]
            self.w = cstate[1]
        else:
            raise NameError("Unknown Control Type")
        
    def __str__(self) -> str:
        return f"[ControlState] v={self.v} w={self.w}"
    
class State():
    def __init__(self, x=0.0, y=0.0, yaw=0.0, v=0.0, w=0.0) -> None:
        """
            x   : agent position in x axis
            y   : agent position in y axis
            yaw : rotation of agent around vertical axis
            v   : agent velocity
            w   : agent angular velocity
        """
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.v = 0.0
        self.w = 0.0
        self.update(x, y, yaw, v, w)

    def update(self, x=None, y=None, yaw=None, v=None, w=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if yaw is not None:
            self.yaw = yaw
        if v is not None:
            self.v = v
        if w is not None:
            self.w = w

    def __str__(self) -> str:
        return f"[State] x={self.x:.2f}, y={self.y:.2f}, yaw={self.yaw:.2f}, v={self.v:.2f}, w={self.w:.2f}"

    def pose(self):
        return (self.x, self.y, self.yaw)

def paste_overlapping_image(
    background: np.ndarray,
    foreground: np.ndarray,
    location: tuple[int, int],
    mask: Optional[np.ndarray] = None,
):
    r"""Composites the foreground onto the background dealing with edge
    boundaries.
    Args:
        background: the background image to paste on.
        foreground: the image to paste. Can be RGB or RGBA. If using alpha
            blending, values for foreground and background should both be
            between 0 and 255. Otherwise behavior is undefined.
        location: the image coordinates to paste the foreground.
        mask: If not None, a mask for deciding what part of the foreground to
            use. Must be the same size as the foreground if provided.
    Returns:
        The modified background image. This operation is in place.
    """
    assert mask is None or mask.shape[:2] == foreground.shape[:2]
    foreground_size = foreground.shape[:2]
    min_pad = (
        max(0, foreground_size[0] // 2 - location[0]),
        max(0, foreground_size[1] // 2 - location[1]),
    )

    max_pad = (
        max(
            0,
            (location[0] + (foreground_size[0] - foreground_size[0] // 2))
            - background.shape[0],
        ),
        max(
            0,
            (location[1] + (foreground_size[1] - foreground_size[1] // 2))
            - background.shape[1],
        ),
    )

    background_patch = background[
        (location[0] - foreground_size[0] // 2 + min_pad[0]) : (
            location[0]
            + (foreground_size[0] - foreground_size[0] // 2)
            - max_pad[0]
        ),
        (location[1] - foreground_size[1] // 2 + min_pad[1]) : (
            location[1]
            + (foreground_size[1] - foreground_size[1] // 2)
            - max_pad[1]
        ),
    ]
    foreground = foreground[
        min_pad[0] : foreground.shape[0] - max_pad[0],
        min_pad[1] : foreground.shape[1] - max_pad[1],
    ]
    if foreground.size == 0 or background_patch.size == 0:
        # Nothing to do, no overlap.
        return background

    if mask is not None:
        mask = mask[
            min_pad[0] : foreground.shape[0] - max_pad[0],
            min_pad[1] : foreground.shape[1] - max_pad[1],
        ]
    
    if foreground.shape[2] == 4:
        # Alpha blending
        foreground = (
            background_patch.astype(np.int32) * (255 - foreground[:, :, [3]])
            + foreground[:, :, :3].astype(np.uint8) * foreground[:, :, [3]]
        ) // 255
    
    if mask is not None:
        background_patch[mask] = foreground[mask]
    else:
        background_patch[:] = foreground

    return background
