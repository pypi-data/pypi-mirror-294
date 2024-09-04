import numpy as np
from typing import Tuple, List, Optional
from airgen.types import Vector3r , Quaternionr, CarControls
from .mechanics import to_eularian_angles
from airgen.client import CarClient

#TODO: Write a AML pipeline to tune this for each form factor.

STANLEY_CONTROL_ATTRIBUTES = {'STANLEY_K' : 5.0, 'STANLEY_WHEEL_BASE':1.0}

def normalize_angle(angle: float) -> float:
    """Normalize an angle to the range [-pi, pi].

    This function ensures that the provided angle is within the
    standard range for angular measurements in radians.

    Args:
        angle (float): The angle to normalize.

    Returns:
        float: The normalized angle.
    """
    while angle > np.pi:
        angle -= 2.0 * np.pi
    while angle < -np.pi:
        angle += 2.0 * np.pi
    return angle


class State:
    """
    Represents the state of a vehicle.

    This class encapsulates the vehicle's position, orientation, and speed.

    Attributes:
        x (float): The x-coordinate of the vehicle's position.
        y (float): The y-coordinate of the vehicle's position.
        yaw (float): The yaw angle (orientation) of the vehicle in radians.
        v (float): The speed of the vehicle.

    Methods:
        __init__(x=0.0, y=0.0, yaw=0.0, v=0.0): Initializes the state with specified or default values.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0, yaw: float = 0.0, v: float = 0.0):
        """
        Initialize the vehicle's state.

        Args:
            x (float, optional): The x-coordinate of the vehicle's position. Defaults to 0.0.
            y (float, optional): The y-coordinate of the vehicle's position. Defaults to 0.0.
            yaw (float, optional): The yaw angle (orientation) of the vehicle in radians. Defaults to 0.0.
            v (float, optional): The speed of the vehicle. Defaults to 0.0.
        """
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v


class CarControl:
    """
    Base class for car control strategies.

    This class defines a common interface for all car controllers.

    Methods:
        controlParams(*args, **kwargs): Abstract method to calculate control parameters.
    """

    @staticmethod
    def controlParams(*args, **kwargs):
        """Calculate control parameters.

        This method should be implemented by subclasses to calculate control parameters
        based on the provided inputs.

        Args:
            *args: Positional arguments required by the control method.
            **kwargs: Keyword arguments required by the control method.

        Returns:
            The control commands, as defined by the specific controller implementation.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
    

class StanleyControl(CarControl):
    """
    Stanley controller for path following.

    This controller calculates the steering angle required to follow a path based
    on the vehicle's current state and the path coordinates.

    Methods:
        controlParams(state: State, cx: list, cy: list, cyaw: list) -> Tuple[float, int]:
            Calculates the steering angle and target index based on the current state and path coordinates.

        calc_target_index(state: State, cx: list, cy: list) -> Tuple[int, float]:
            Calculates the index of the target point on the path.
    """

    # the controller attributes might vary for each vehicle and hence should come from the client when it calls this method
    @staticmethod
    def controlParams(state: State, controller_attributes:dict, cx: list, cy: list, cyaw: list) -> Tuple[float, int]:
        """Calculate the steering angle and target index.

        This method calculates the steering angle required to follow the path
        and the index of the target point on the path.

        Args:
            state (State): The current state of the vehicle.
            cx (list): The x-coordinates of the path.
            cy (list): The y-coordinates of the path.
            cyaw (list): The yaw angles of the path.

        Returns:
            Tuple[float, int]: The steering angle and the target index.
        """
        k = controller_attributes['STANLEY_K']
        current_target_idx, error_front_axle = StanleyControl.calc_target_index(state, controller_attributes, cx, cy)
        theta_e = normalize_angle(cyaw[current_target_idx] - state.yaw)
        theta_d = np.arctan2(k * error_front_axle, state.v)
        delta = theta_e + theta_d

        return delta, current_target_idx

    @staticmethod
    def calc_target_index(state: State,  controller_attributes:dict, cx: list, cy: list) -> Tuple[int, float]:
        """Calculate the target index on the path.

        This method calculates the index of the target point on the path and
        the error between the front axle and the path.

        Args:
            state (State): The current state of the vehicle.
            cx (list): The x-coordinates of the path.
            cy (list): The y-coordinates of the path.

        Returns:
            Tuple[int, float]: The index of the target point and the front axle error.
        """
        wheel_base = controller_attributes['STANLEY_WHEEL_BASE']
        fx = state.x + wheel_base * np.cos(state.yaw)
        fy = state.y + wheel_base * np.sin(state.yaw)

        # Search nearest point index
        dx = [fx - icx for icx in cx]
        dy = [fy - icy for icy in cy]
        d = np.hypot(dx, dy)
        target_idx = np.argmin(d)

        # Project RMS error onto front axle vector
        front_axle_vec = [-np.cos(state.yaw + np.pi / 2),
                        -np.sin(state.yaw + np.pi / 2)]
        error_front_axle = np.dot([dx[target_idx], dy[target_idx]], front_axle_vec)

        return target_idx, error_front_axle



#spline computation code, we should by_pass the spline computation code if the orientations have already been populated by 
import math
import numpy as np
import bisect


class Spline:
    """
    Cubic Spline class
    """

    def __init__(self, x, y):
        self.b, self.c, self.d, self.w = [], [], [], []

        self.x = x
        self.y = y

        self.nx = len(x)  # dimension of x
        h = np.diff(x)

        # calc coefficient c
        self.a = [iy for iy in y]

        # calc coefficient c
        A = self.__calc_A(h)
        B = self.__calc_B(h)
        self.c = np.linalg.solve(A, B)
        #  print(self.c1)

        # calc spline coefficient b and d
        for i in range(self.nx - 1):
            self.d.append((self.c[i + 1] - self.c[i]) / (3.0 * h[i]))
            tb = (self.a[i + 1] - self.a[i]) / h[i] - h[i] * \
                (self.c[i + 1] + 2.0 * self.c[i]) / 3.0
            self.b.append(tb)

    def calc(self, t):
        """
        Calc position

        if t is outside of the input x, return None

        """

        if t < self.x[0]:
            return None
        elif t > self.x[-1]:
            return None

        i = self.__search_index(t)
        dx = t - self.x[i]
        result = self.a[i] + self.b[i] * dx + \
            self.c[i] * dx ** 2.0 + self.d[i] * dx ** 3.0

        return result

    def calcd(self, t):
        """
        Calc first derivative

        if t is outside of the input x, return None
        """

        if t < self.x[0]:
            return None
        elif t > self.x[-1]:
            return None

        i = self.__search_index(t)
        dx = t - self.x[i]
        result = self.b[i] + 2.0 * self.c[i] * dx + 3.0 * self.d[i] * dx ** 2.0
        return result

    def calcdd(self, t):
        """
        Calc second derivative
        """

        if t < self.x[0]:
            return None
        elif t > self.x[-1]:
            return None

        i = self.__search_index(t)
        dx = t - self.x[i]
        result = 2.0 * self.c[i] + 6.0 * self.d[i] * dx
        return result

    def __search_index(self, x):
        """
        search data segment index
        """
        return bisect.bisect(self.x, x) - 1

    def __calc_A(self, h):
        """
        calc matrix A for spline coefficient c
        """
        A = np.zeros((self.nx, self.nx))
        A[0, 0] = 1.0
        for i in range(self.nx - 1):
            if i != (self.nx - 2):
                A[i + 1, i + 1] = 2.0 * (h[i] + h[i + 1])
            A[i + 1, i] = h[i]
            A[i, i + 1] = h[i]

        A[0, 1] = 0.0
        A[self.nx - 1, self.nx - 2] = 0.0
        A[self.nx - 1, self.nx - 1] = 1.0
        #  print(A)
        return A

    def __calc_B(self, h):
        """
        calc matrix B for spline coefficient c
        """
        B = np.zeros(self.nx)
        for i in range(self.nx - 2):
            B[i + 1] = 3.0 * (self.a[i + 2] - self.a[i + 1]) / \
                h[i + 1] - 3.0 * (self.a[i + 1] - self.a[i]) / h[i]
        return B


class Spline2D:
    """
    2D Cubic Spline class

    """

    def __init__(self, x, y):
        self.s = self.__calc_s(x, y)
        self.sx = Spline(self.s, x)
        self.sy = Spline(self.s, y)

    def __calc_s(self, x, y):
        dx = np.diff(x)
        dy = np.diff(y)
        self.ds = np.hypot(dx, dy)
        s = [0]
        s.extend(np.cumsum(self.ds))
        return s

    def calc_position(self, s):
        """
        calc position
        """
        x = self.sx.calc(s)
        y = self.sy.calc(s)

        return x, y

    def calc_curvature(self, s):
        """
        calc curvature
        """
        dx = self.sx.calcd(s)
        ddx = self.sx.calcdd(s)
        dy = self.sy.calcd(s)
        ddy = self.sy.calcdd(s)
        k = (ddy * dx - ddx * dy) / ((dx ** 2 + dy ** 2)**(3 / 2))
        return k

    def calc_yaw(self, s):
        """
        calc yaw
        """
        dx = self.sx.calcd(s)
        dy = self.sy.calcd(s)
        yaw = math.atan2(dy, dx)
        return yaw

class SplineHelper:
    @staticmethod
    def calc_spline_course(path:List[Vector3r], ds=0.1):

        # Extract x_vals and y_vals into separate lists
        # TODO : find if there is a way in which we can avoid do this
        x_vals = [vector.x_val for vector in path]
        y_vals = [vector.y_val for vector in path]
        sp = Spline2D(x_vals, y_vals)
        s = list(np.arange(0, sp.s[-1], ds))

        rx, ry, ryaw, rk = [], [], [], []
        for i_s in s:
            ix, iy = sp.calc_position(i_s)
            rx.append(ix)
            ry.append(iy)
            ryaw.append(sp.calc_yaw(i_s))
            rk.append(sp.calc_curvature(i_s))

        return rx, ry, ryaw, rk, s

    @staticmethod
    def fitSpline(path:List[Vector3r]) -> Tuple:
        cx, cy, cyaw, ck, s = SplineHelper.calc_spline_course(path, ds=0.1)
        return cx, cy, cyaw, ck, s



class CarController:
    @staticmethod
    def runOneStep(
        client: CarClient,
        target_speed: float,
        state: State,
        cx: List[float],
        cy: List[float],
        cyaw: List[float],
        last_idx: int,
        brake_override: bool, 
        done: bool,
        lookahead:int = -1,
        adaptive_lookahead:int = 1,
    ) -> bool:
        """
        Executes one control step for the car to follow the path.

        Args:
            client (CarClient): The client controlling the car.
            state (State): The current state of the car.
            cx (List[float]): The x-coordinates of the path.
            cy (List[float]): The y-coordinates of the path.
            cyaw (List[float]): The yaw angles of the path.
            last_idx (int): The last index of the path.
            brake_override (bool): The current brake override status.
            lookahead (int): The number of waypoints to lookahead
            adaptive_lookahead (int): If its 1, the lookahead will be adaptive
        Returns:
            bool: Updated brake override status.
        """
        stanley_control_attributes = STANLEY_CONTROL_ATTRIBUTES
        steering, target_idx = StanleyControl.controlParams(state, stanley_control_attributes, cx, cy, cyaw)
        
        if not brake_override:
            brake_override = CarController.adjustSpeedForTurn(
                                                            client,
                                                            target_speed,
                                                            state,
                                                            steering,
                                                            target_idx,
                                                            cyaw,
                                                            last_idx,
                                                            brake_override,
                                                            lookahead,
                                                            adaptive_lookahead
                                                        )
        else:
            # print(f"handbrake mechanism activated")
            CarController.sendCommands(client, speed=0, steering=steering, handbrake=True)
            done = True
        # print(f"brake override at {target_idx} is {brake_override}")
        return target_idx, brake_override, done


    @staticmethod
    def setTargetSpeed(client: CarClient, speed: float) -> None:
        """
        Set the target speed for the car.

        This method sets the desired speed for the car using the provided client.

        Args:
            client (CarClient): The client controlling the car.
            speed (float): The target speed in meters per second.
        """
        client.setCarTargetSpeed(speed)

    @staticmethod
    def sendCommands(client: CarClient, speed: float = 0, steering: float = 0.0, handbrake: bool = False) -> None:
        """
        Send control commands to the car.

        This method sends the speed, steering, and handbrake commands to the car.

        Args:
            client (CarClient): The client controlling the car.
            speed (float, optional): The desired speed in meters per second. Defaults to 0.
            steering (float, optional): The steering angle, typically in radians. Defaults to 0.0.
            handbrake (bool, optional): Whether to apply the handbrake. Defaults to False.
        """
        CarController.setTargetSpeed(client, speed)
        controls = CarControls()
        controls.steering = steering
        controls.handbrake = handbrake
        client.setCarControls(controls)

    @staticmethod
    def updateState(client: CarClient, state: State) -> None:
        """
        Update the state of the car.

        This method updates the position, velocity, and orientation of the car.

        Args:
            client (CarClient): The client controlling the car.
            state (State): The current state object to be updated.
        """
        car_state = client.getCarState()
        state.x = car_state.kinematics_estimated.position.x_val
        state.y = car_state.kinematics_estimated.position.y_val

        state.v = np.linalg.norm(car_state.kinematics_estimated.linear_velocity.to_numpy_array())
        p, r, ye = to_eularian_angles(car_state.kinematics_estimated.orientation)
        state.yaw = ye

    @staticmethod
    def adjustSpeedForTurn(
        client: CarClient,
        target_speed: float, 
        state: State, 
        steering: float, 
        target_idx: int, 
        cyaw: List[float], 
        last_idx: int, 
        brake_override: bool,
        lookahead: int,
        adaptive_lookahead: int
    ) -> bool:
        """
        Adjust the car's speed when approaching a turn.

        Args:
            client (CarClient): The client controlling the car.
            state (State): The current state of the car.
            steering (float): The current steering angle.
            target_idx (int): The index of the target point in the path.
            cyaw (List[float]): The list of yaw angles for the path.
            last_idx (int): The last index of the path.
            brake_override (bool): The current brake override status.

        Returns:
            bool: Updated brake override status.
        """
        
        if not brake_override:
            speed = target_speed
            lookahead_window = 0
            # Use adaptive lookahead to figure out how far we are from a turn
            if(adaptive_lookahead == 1 or lookahead == -1):
                lookahead_window = int(speed)
            else: 
                lookahead_window = lookahead
            if target_idx + lookahead_window < len(cyaw):
                lookahead_idx = target_idx + lookahead_window
            else:
                lookahead_idx = len(cyaw) - 1

            # Slow down to 3 m/s if yaw difference is over a threshold, indicating an upcoming turn
            if abs((abs(cyaw[lookahead_idx]) - abs(cyaw[target_idx])) * 180 / np.pi) > 15.0:
                speed = min(target_speed, 3.0)

            CarController.sendCommands(client, speed=speed, steering=steering, handbrake=False)
            CarController.updateState(client, state)

            if target_idx > last_idx - min(min(int(speed),5), len(cyaw)-1):
                brake_override = True
                speed = 0

        return brake_override

    @staticmethod
    def moveOnPath(
        client: CarClient,
        path: List[Vector3r],
        velocity: float = 0,
        lookahead: int = -1,
        adaptive_lookahead: int = 1,
        orientations: Optional[List[float]] = None,
        ) -> None:
        """
        Command the car to move along a specified path.

        This function sends commands to a car to follow a given path at a specified velocity. 
        The path is a list of 3D vectors, and each vector represents a point in space that 
        the car should follow.

        Args:
            path (List[Vector3r]): A list of 3D vectors representing the path to follow.
            velocity (float): The speed at which the car should move along the path, in meters per second.
            timeout_sec (float, optional): The maximum time allowed for the car to reach the destination, in seconds. Defaults to 3e38.
            lookahead (int, optional): The number of points the car should look ahead on the path for control decisions. Defaults to -1, which means no specific lookahead.
            adaptive_lookahead (bool, optional): Whether to adjust the lookahead dynamically based on the car's speed. Defaults to True.
            orientations (Optional[List[Quarterion]], optional): Optional list of orientations corresponding to each path point. Defaults to empty.
        
        Returns:
            None
        """
        # Assert that if orientations are provided, their length matches the length of the path        
        if orientations:
            assert len(orientations) == len(path), "Length of orientations must match the length of the path."
            # Extract x_val and y_val into separate arrays
            cx = [point.x_val for point in path]
            cy = [point.y_val for point in path]
            cyaw = orientations
        else:
            cx, cy, cyaw, ck, s = SplineHelper.fitSpline(path)
        car_pose = client.simGetVehiclePose()
        # Initial state
        car_state = client.getCarState()
        curr_state = State(x = car_state.kinematics_estimated.position.x_val,
                           y = car_state.kinematics_estimated.position.y_val,
                           v = np.linalg.norm(car_state.kinematics_estimated.linear_velocity.to_numpy_array()),
                           yaw = np.radians(0.0))
        p, r, ye = to_eularian_angles(car_state.kinematics_estimated.orientation)
        curr_state.yaw = ye
        last_idx = len(cx) - 1
        brake_override = False
        done = False
        while not done:
            target_idx, brake_override, done = CarController.runOneStep(client , velocity, curr_state, cx , cy , cyaw , last_idx, brake_override, done, lookahead, adaptive_lookahead)
        

    
    

