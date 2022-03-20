from pynput import keyboard
import geometry_msgs.msg
import rclpy

moveBindings = {
    'i': (1, 0, 0, 0),
    'o': (1, 0, 0, -1),
    'j': (0, 0, 0, 1),
    'l': (0, 0, 0, -1),
    'u': (1, 0, 0, 1),
    ',': (-1, 0, 0, 0),
    '.': (-1, 0, 0, 1),
    'm': (-1, 0, 0, -1),
    'O': (1, -1, 0, 0),
    'I': (1, 0, 0, 0),
    'J': (0, 1, 0, 0),
    'L': (0, -1, 0, 0),
    'U': (1, 1, 0, 0),
    '<': (-1, 0, 0, 0),
    '>': (-1, -1, 0, 0),
    'M': (-1, 1, 0, 0),
    't': (0, 0, 1, 0),
    'b': (0, 0, -1, 0),
}

speedBindings = {
    'q': (1.1, 1.1),
    'z': (.9, .9),
    'w': (1.1, 1),
    'x': (.9, 1),
    'e': (1, 1.1),
    'c': (1, .9),
}

class KeyboardInput():

    def __init__(self):
        rclpy.init()

        node = rclpy.create_node('teleop_twist_keyboard')
        self.pub = node.create_publisher(geometry_msgs.msg.Twist, '/drone1/cmd_vel', 10)

        self.speed = 0.5
        self.turn = 1.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        self.status = 0.0

    def on_press(self, Key):
        try:
            if Key.char in moveBindings.keys():
                self.x = moveBindings[Key.char][0]
                self.y = moveBindings[Key.char][1]
                self.z = moveBindings[Key.char][2]
                self.th = moveBindings[Key.char][3]
            elif Key.char in speedBindings.keys():
                self.speed = self.speed * speedBindings[Key.char][0]
                self.turn = self.turn * speedBindings[Key.char][1]
            else:
                self.x = 0.0
                self.y = 0.0
                self.z = 0.0
                self.th = 0.0
                if Key == keyboard.Key.esc:
                    # Stop listener
                    return False

            twist = geometry_msgs.msg.Twist()
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = self.th * self.turn
            self.pub.publish(twist)

        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char in moveBindings.keys():
                self.x = 0
                self.y = 0
                self.z = 0
                self.th = 0

            twist = geometry_msgs.msg.Twist()
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = self.th * self.turn
            self.pub.publish(twist)
            
        except AttributeError:
            pass     
        if key == keyboard.Key.esc:
            # Stop listener
            return False


# Collect events until released
keyAction = KeyboardInput()
getInput = keyboard.Listener(
    on_press=keyAction.on_press, on_release=keyAction.on_release)
getInput.start()
getInput.join()
