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
        self.ir1 = bundle.irs[0]
        self.game = game
        
        # set state
        # self.move_state = self.move_state()
        self.move_state = self.move_state.STOP
        self.move_state2 = self.move_state2.STOP
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

    class turn_state(Enum) :
        STOP = 0
        TURN_LEFT = 1
        TURN_RIGHT = 2
        STOPPING = 3

    class move_state(Enum) :
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
        yaw = self.gyro.yaw + 2
        roll = self.gyro.roll

        print(self.turn_state)
        print(self.move_state)

        # 자이로 센서 인식해서 좌우 이동
        if yaw > 15:
            if self.turn_state == self.turn_state.STOP:
                self.turn_state = self.turn_state.MOVE_LEFT
            elif self.turn_state == self.turn_state.MOVE_RIGHT:
                self.turn_state = self.turn_state.STOPPING
        elif yaw < -15:
            if self.turn_state == self.turn_state.STOP:
                self.turn_state = self.turn_state.MOVE_RIGHT
            elif self.turn_state == self.turn_state.MOVE_LEFT:
                self.turn_state = self.turn_state.STOPPING
        else:
            if self.turn_state == self.turn_state.MOVE_LEFT:
                self.turn_state = self.turn_state.STOPPING
            if self.turn_state == self.turn_state.MOVE_RIGHT:
                self.turn_state = self.turn_state.STOPPING
            if self.turn_state == self.turn_state.STOPPING:
                self.turn_state = self.turn_state.STOP
        
        # 자이로 센서 인식해서 앞뒤 이동
        if roll < -15:
            if self.move_state == self.move_state.STOP:
                self.move_state = self.move_state.MOVE_FORWARD
            elif self.move_state == self.move_state.MOVE_BACKWARD:
                self.move_state = self.move_state.STOPPING
        elif roll > 15:
            if self.move_state == self.move_state.STOP:
                self.move_state = self.move_state.MOVE_BACKWARD
            elif self.move_state == self.move_state.MOVE_FORWARD:
                self.move_state = self.move_state.STOPPING
        else:
            if self.move_state == self.move_state.MOVE_FORWARD:
                self.move_state = self.move_state.STOPPING
            if self.move_state == self.move_state.MOVE_BACKWARD:
                self.move_state = self.move_state.STOPPING
            if self.move_state == self.move_state.STOPPING:
                self.move_state = self.move_state.STOP

        k = 0


        # Turn Actions

        if self.turn_state == self.turn_state.MOVE_LEFT:
            # self.move_left()
            k += 1
        elif self.turn_state == self.turn_state.MOVE_RIGHT:
            # self.move_right()
            k += 2
        # elif self.move_state == self.move_state.STOP:
            # self.stop()
        # else:
            # self.stopping()


        # Move Actions

        if self.move_state == self.move_state.MOVE_FORWARD:
            # self.move_forward()
            k += 4
        elif self.move_state == self.move_state.MOVE_BACKWARD:
            # self.move_backward()
            k += 8
        # elif self.move_state2 == self.move_state2.STOP:
            # self.stop()
        # else:
            # self.stopping()        


        # 버튼 클릭할 시 사격
        if self.button1.pressed :
            # self.attack()
            k += 16

        # ir 센서 인식 시 무기 전환
        if self.ir1.proximity > 50 :
            # self.select_next_weapon()
            k += 32

        if self.dial1.degree < 45 :
            k += 64
        elif self.dial1.degree > 55 :
            k += 128
        
        return self.game.make_action(self.actions[k])
        # return self.gyro.acceleration_x


   
    # def stop(self) :
    #     # self.move_state = self.move_state.STOP
    #     return self.game.make_action(self.actions[0])

    # def stopping(self) :
    #     # self.move_state = self.move_state.STOPPING
    #     return self.game.make_action(self.actions[0])

    # def move_left(self) :
    #     return self.game.make_action(self.actions[1])

    # def move_right(self) : 
    #     return self.game.make_action(self.actions[2])
    
    # def move_forward(self) :
    #     return self.game.make_action(self.actions[4])

    # def move_backward(self) : 
    #     return self.game.make_action(self.actions[8])
    
    # # shoot 사격
    # def attack(self) :
    #     return self.game.make_action(self.actions[16])

    # def select_next_weapon(self) :
    #     return self.game.make_action(self.actions[32])
    
        

