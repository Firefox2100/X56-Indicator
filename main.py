import pygame
import sys
import playsound

BLACK = (0, 0, 0)
GREY = (150, 150, 150)


# Class to print the texts
class TextPrint:
    def __init__(self):
        self.line_height = 15
        self.font = pygame.font.Font(None, 20)

    def print(self, window, text, x, y, color):
        text_bitmap = self.font.render(text, True, color)
        window.blit(text_bitmap, [x, int(y - self.line_height / 2)])


class ThrottleBar:
    def __init__(self):
        self.width = 20
        self.height = 200
        self.x = 10
        self.y = 10

    def draw_empty_bar(self, window, profile, is_left):
        # pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height))
        current_y = self.y + self.height
        for p in profile:
            new_y = current_y - int(self.height * p.percentage)
            pygame.draw.line(window, (p.R, p.G, p.B), (self.x, new_y + 1), (self.x + self.width - 1, new_y + 1), 3)
            if is_left:
                textPrint.print(window, p.name, 15, int((current_y + new_y) / 2), (p.R, p.G, p.B))
            else:
                textPrint.print(window, p.name, 120, int((current_y + new_y) / 2), (p.R, p.G, p.B))
            current_y = new_y

    def draw_full_bar(self, window, profile):
        current_y = self.y + self.height
        for p in profile:
            new_y = current_y - int(self.height * p.percentage)
            pygame.draw.rect(window, (p.R, p.G, p.B), (self.x, new_y, self.width, current_y - new_y))
            current_y = new_y

    def draw_bar(self, window, profile, value, is_left):
        self.draw_full_bar(window, profile)
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height * (1 - value)))
        self.draw_empty_bar(window, profile, is_left)

    def draw_bar_middle(self, window, profile, value, percentage, is_left):
        self.draw_full_bar(window, profile)
        if value > percentage:
            p_y = self.y + self.height * (1 - percentage)
            pygame.draw.rect(window, BLACK, (self.x, p_y, self.width, self.height * percentage))
            pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height * (1 - value)))
        else:
            v_y = self.y + self.height * (1 - value)
            pygame.draw.rect(window, BLACK, (self.x, v_y, self.width, self.height * value + 1))
            pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height * (1 - percentage)))
        self.draw_empty_bar(window, profile, is_left)


class Profile:
    def __init__(self):
        self.name = ""
        self.percentage = 0.0
        self.R = 0
        self.G = 0
        self.B = 0

    def string_to_profile(self, s):
        parameters = s.split()
        self.name = parameters[1]
        self.percentage = float(parameters[2])
        self.R = float(parameters[3])
        self.G = float(parameters[4])
        self.B = float(parameters[5])


class Detent:
    def __init__(self, p, t):
        self.position = p
        self.type = t
        self.p_triggered = False
        self.n_triggered = False

    def enter(self):
        playsound.playsound('enter.wav')
        # print('Entering')

    def leave(self):
        playsound.playsound('leave.wav')
        # print('Leaving')

    def vibrate(self, v):
        if self.type == 1:
            # Positive detent
            if self.position - 0.02 < v < self.position:
                if not self.p_triggered:
                    # In range and not triggered
                    if self.n_triggered:
                        # Pulling back
                        self.leave()
                        self.n_triggered = False
                    else:
                        # Pushing forward
                        self.enter()
                    self.p_triggered = True
                else:
                    # Already triggered
                    pass
            elif self.position < v < self.position + 0.02:
                if not self.n_triggered:
                    # In range and not triggered
                    if self.p_triggered:
                        # Pushing forward
                        self.leave()
                        self.p_triggered = False
                    else:
                        # Pulling back, since it's positive it shouldn't click
                        pass
                    self.n_triggered = True
                else:
                    # Already triggered
                    pass
            else:
                # Out of detent range, reset
                self.p_triggered = False
                self.n_triggered = False
        elif self.type == -1:
            # Negative detent
            if self.position - 0.02 < v < self.position:
                if not self.p_triggered:
                    # In range and not triggered
                    if self.n_triggered:
                        # Pulling back
                        self.leave()
                        self.n_triggered = False
                    else:
                        # Pushing forward, since it's negative it shouldn't click
                        pass
                    self.p_triggered = True
                else:
                    # Already triggered
                    pass
            elif self.position < v < self.position + 0.02:
                if not self.n_triggered:
                    # In range and not triggered
                    if self.p_triggered:
                        # Pushing forward
                        self.leave()
                        self.p_triggered = False
                    else:
                        # Pulling back
                        self.enter()
                    self.n_triggered = True
                else:
                    # Already triggered
                    pass
            else:
                # Out of detent range, reset
                self.p_triggered = False
                self.n_triggered = False
        else:
            # Normal detent
            if self.position - 0.02 < v < self.position:
                if not self.p_triggered:
                    # In range and not triggered
                    if self.n_triggered:
                        # Pulling back
                        self.leave()
                        self.n_triggered = False
                    else:
                        # Pushing forward
                        self.enter()
                    self.p_triggered = True
                else:
                    # Already triggered
                    pass
            elif self.position < v < self.position + 0.02:
                if not self.n_triggered:
                    # In range and not triggered
                    if self.p_triggered:
                        # Pushing forward
                        self.leave()
                        self.p_triggered = False
                    else:
                        # Pulling back
                        self.enter()
                    self.n_triggered = True
                else:
                    # Already triggered
                    pass
            else:
                # Out of detent range, reset
                self.p_triggered = False
                self.n_triggered = False


# Parse the parameter
if len(sys.argv) == 1:
    ex = Exception('Error: Not enough parameters')
    raise ex

is_center = False
percentage = 0.0

for i in range(1, len(sys.argv)):
    if sys.argv[i] == '-m':
        is_center = True
        i += 1
        percentage = float(sys.argv[i])
    elif sys.argv[i] == '-z':
        is_center = False

# Read in the profile
with open('profile.txt') as profile_in:
    lines = profile_in.readlines()

profile_L = []
profile_R = []
detent_L = []
detent_R = []

sum_L = 0
sum_R = 0

for line in lines:
    temp = Profile()
    temp.string_to_profile(line)
    temp_detent = Detent(0, 0)

    detent_flag = True

    if line[1] == 'P':
        temp_detent = Detent(temp.percentage, 1)
    elif line[1] == 'N':
        temp_detent = Detent(temp.percentage, -1)
    elif line[1] == 'D':
        temp_detent = Detent(temp.percentage, 0)
    else:
        detent_flag = False

    if line[0] == 'L':
        profile_L.append(temp)
        if detent_flag:
            temp_detent.position += sum_L
            detent_L.append(temp_detent)
        sum_L += temp.percentage
    else:
        profile_R.append(temp)
        if detent_flag:
            temp_detent.position += sum_R
            detent_R.append(temp_detent)
        sum_R += temp.percentage

# Screen initialize
pygame.init()
size = [170, 260]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Throttle")
screen.fill(GREY)

# Find and initialize the throttle
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
throttle = pygame.joystick.Joystick(0)
for i in range(joystick_count):
    if "Throttle" in pygame.joystick.Joystick(i).get_name():
        throttle = pygame.joystick.Joystick(i)
throttle.init()

# Parameters initialization
done = False
clock = pygame.time.Clock()
textPrint = TextPrint()

left_bar = ThrottleBar()
left_bar.x = 60
left_bar.y = 30
right_bar = ThrottleBar()
right_bar.x = 90
right_bar.y = 30

detent_flag = False
if detent_L or detent_R:
    detent_flag = True

while not done:
    # Quit when user close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear screen
    screen.fill(GREY)

    # Get axis from throttle
    axis_L = (1 - throttle.get_axis(0)) / 2
    axis_R = (1 - throttle.get_axis(1)) / 2

    # Draw the throttle indicator bar
    if is_center:
        left_bar.draw_bar_middle(screen, profile_L, axis_L, percentage, True)
        right_bar.draw_bar_middle(screen, profile_R, axis_R, percentage, False)
    else:
        left_bar.draw_bar(screen, profile_L, axis_L, True)
        right_bar.draw_bar(screen, profile_R, axis_R, False)

    if detent_flag:
        if abs(axis_L - axis_R) < 0.05:
            for d in detent_L:
                d.vibrate(axis_L)
        else:
            for d in detent_L:
                d.vibrate(axis_L)
            for d in detent_R:
                d.vibrate(axis_R)

    # Refresh the screen
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
