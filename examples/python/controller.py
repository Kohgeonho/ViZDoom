import modi
from time import sleep
from enum import Enum
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

        self.actions = [
            [True, False, False],   # Move Left
            [False, True, False],   # Move Right
            [False, False, True],   # Shoot
            [True, True, False], 
            [True, False, True], 
            [False, True, True], 
            [False, False, False],  # Do Nothing
            [True, True, True]
        ]
        # 주석 무시해주세요
        # self.r = null
        # self.move_state = Enum("STOP", "MOVE_FORWARD", "MOVE_RIGHT", "MOVE_LEFT",
        #     "TURN_RIGHT", "TURN_LEFT", "SIGHT_UP", "SIGHT_DOWN", "SHOOT", "WEAPON_CHANGE")
        # self.move_state = "STOP"

    class move_state(Enum) :
        STOP = 0
        MOVE_FORWARD = 1
        MOVE_RIGHT = 2 
        MOVE_LEFT = 3
        STOPPING = 4

    class sight_state(Enum) :
        SIGHT_UP = 0
        SIGHT_DOWN = 1

    # 자이로센서 인식할 때까지 대기
    def initial_ready(self, time = 0.1) :
        while self.gyro.acceleration_x == 0 or self.gyro.acceleration_y == 0 or self.gyro.acceleration_z == 0:
            sleep(time)

    # 모든 동작 실행
    def act(self) :
        accx = self.gyro.acceleration_x

        print(self.move_state.STOP)

        # 자이로 센서 인식해서 좌우 이동
        if accx < -10:
            if self.move_state == self.move_state.STOP:
                self.move_state = self.move_state.MOVE_LEFT
            elif self.move_state == self.move_state.MOVE_LEFT:
                self.move_state = self.move_state.STOPPING
        elif accx > 10:
            if self.move_state == self.move_state.STOP:
                self.move_state = self.move_state.MOVE_RIGHT
            elif self.move_state == self.move_state.MOVE_RIGHT:
                self.move_state -= self.move_state.STOPPING
        else:
            if self.move_state == self.move_state.STOPPING:
                self.move_state = self.move_state.STOP
        
        # Move Actions
        if self.move_state == self.move_state.MOVE_LEFT:
            self.move_left()
        elif self.move_state == self.move_state.MOVE_RIGHT:
            self.move_right()
        else:
            pass

        # 버튼 클릭할 시 사격
        if self.button1.pressed :
            self.shoot()
        
    # move 이동
    def move_forward(self) :
        self.move_state = self.move_state.MOVE_FORWARD
        pass

    def move_left(self) :
        self.move_state = self.move_state.MOVE_LEFT
        return self.game.make_action(self.actions[0])

    def move_right(self) : 
        self.move_state = self.move_state.MOVE_RIGHT
        return self.game.make_action(self.actions[1])
    
    def stopping(self) :
        self.move_state = self.move_state.STOPPING
    
    def stop(self) :
        self.move_state = self.move_state.STOP
    
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

    # shoot 사격
    def shoot(self) :
        return self.game.make_action(self.actions[2])

    # weapon change 무기 변경
    def weapon_change(self) :
        pass

