import modi
from time import sleep
from enum import Enum
import numpy as np
import vizdoom as vzd

class Controller :
    def __init__(self, game) -> None:
        # set modi
        bundle = modi.MODI()
        self.button1 = bundle.buttons[0]
        self.dial1 = bundle.dials[0]
        self.gyro = bundle.gyros[0]
        self.game = game
        
        # set state
        # self.move_state = self.move_state()
        self.move_state = self.move_state.STOP
        # self.sight_state = self.sight_state()
        self.sight_state = self.sight_state.SIGHT_DOWN

        actions = game.get_available_buttons()
        print(actions, len(actions))
        num_actions = len(actions)
        self.actions = np.array([
            np.array([i for i in np.binary_repr(n, width=num_actions)]).astype(np.bool)[::-1]
            for n in range(2 ** num_actions)
        ])
        # 주석 무시해주세요
        # self.r = null
        # self.move_state = Enum("STOP", "MOVE_FORWARD", "MOVE_RIGHT", "MOVE_LEFT",
        #     "TURN_RIGHT", "TURN_LEFT", "SIGHT_UP", "SIGHT_DOWN", "SHOOT", "WEAPON_CHANGE")
        # self.move_state = "STOP"

    class move_state(Enum) :
        STOP = 0
        MOVE_LEFT = 1
        MOVE_RIGHT = 2
        STOPPING = 3

    class move_state2(Enum) :
        STOP = 0
        MOVE_FORWARD = 1
        MOVE_BACKWARD = 2
        STOPPING = 3

    class sight_state(Enum) :
        SIGHT_UP = 0
        SIGHT_DOWN = 1

    # 자이로센서 인식할 때까지 대기
    def initial_ready(self, time = 0.1) :
        while self.gyro.acceleration_x == 0 or self.gyro.acceleration_y == 0 or self.gyro.acceleration_z == 0:
            sleep(time)

    # 모든 동작 실행
    def act(self) :
        yaw = self.gyro.yaw
        roll = self.gyro.roll

        print(self.move_state, self.move_state2)

        # 자이로 센서 인식해서 좌우 이동
        if yaw > 30:
            if self.move_state == self.move_state.STOP:
                self.move_state = self.move_state.MOVE_LEFT
            elif self.move_state == self.move_state.MOVE_RIGHT:
                self.move_state = self.move_state.STOPPING
        elif yaw < -30:
            if self.move_state == self.move_state.STOP:
                self.move_state = self.move_state.MOVE_RIGHT
            elif self.move_state == self.move_state.MOVE_LEFT:
                self.move_state = self.move_state.STOPPING
        else:
            if self.move_state == self.move_state.MOVE_LEFT:
                self.move_state = self.move_state.STOPPING
            if self.move_state == self.move_state.MOVE_RIGHT:
                self.move_state = self.move_state.STOPPING
            if self.move_state == self.move_state.STOPPING:
                self.move_state = self.move_state.STOP
        
        # 자이로 센서 인식해서 앞뒤 이동
        if roll < -30:
            if self.move_state2 == self.move_state2.STOP:
                self.move_state2 = self.move_state2.MOVE_FORWARD
            elif self.move_state2 == self.move_state2.MOVE_BACKWARD:
                self.move_state2 = self.move_state2.STOPPING
        elif roll > 30:
            if self.move_state2 == self.move_state2.STOP:
                self.move_state2 = self.move_state2.MOVE_BACKWARD
            elif self.move_state2 == self.move_state2.MOVE_FORWARD:
                self.move_state2 = self.move_state2.STOPPING
        else:
            if self.move_state2 == self.move_state2.MOVE_FORWARD:
                self.move_state2 = self.move_state2.STOPPING
            if self.move_state2 == self.move_state2.MOVE_BACKWARD:
                self.move_state2 = self.move_state2.STOPPING
            if self.move_state2 == self.move_state2.STOPPING:
                self.move_state2 = self.move_state2.STOP


        # Move Actions

        if self.move_state2 == self.move_state2.MOVE_FORWARD:
            self.move_forward()
        elif self.move_state2 == self.move_state2.MOVE_BACKWARD:
            self.move_backward()
        elif self.move_state2 == self.move_state2.STOP:
            self.stop()
        else:
            self.stopping()


        if self.move_state == self.move_state.MOVE_LEFT:
            self.move_left()
        elif self.move_state == self.move_state.MOVE_RIGHT:
            self.move_right()
        elif self.move_state == self.move_state.STOP:
            self.stop()
        else:
            self.stopping()

        

        # 버튼 클릭할 시 사격
        if self.button1.pressed :
            self.attack()

        return self.gyro.acceleration_x

        
        

    def stop(self) :
        # self.move_state = self.move_state.STOP
        return self.game.make_action(self.actions[0])

    def stopping(self) :
        # self.move_state = self.move_state.STOPPING
        return self.game.make_action(self.actions[0])

    def move_left(self) :
        return self.game.make_action(self.actions[1])

    def move_right(self) : 
        return self.game.make_action(self.actions[2])
    
    def move_forward(self) :
        return self.game.make_action(self.actions[4])

    def move_backward(self) : 
        return self.game.make_action(self.actions[8])
    
    # shoot 사격
    def attack(self) :
        return self.game.make_action(self.actions[16])

    def select_next_weapon(self) :
        return self.game.make_action(self.actions[32])
    
        
    
    
    
    # turn 방향 전환 
    def turn_left(self) :
        pass

    def turn_right(self) :
        pass

    # sight change 시선 옮기기
    def sight_up(self) :
        self.sight_state = self.sight_state.SIGHT_UP
        pass

    def sight_down(self) :
        self.sight_state = self.sight_state.SIGHT_DOWN
        pass

