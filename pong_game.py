# Implementation of classic arcade game Pong by Aditya Kamath

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left

def reset():
    new_game()

def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [ WIDTH / 2, HEIGHT / 2]
    
    if direction == "RIGHT":
        ball_vel = [random.randrange(120, 240) / 60, - (random.randrange(60, 180)) / 60]
    
    elif direction == "LEFT":
        ball_vel = [ -random.randrange(120, 240) / 60, - (random.randrange(60, 180)) / 60] 

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, acc  # these are numbers
    global score1, score2  # these are ints
    score1, score2 = 0, 0
    paddle1_pos = [0, HEIGHT / 2]
    paddle2_pos = [WIDTH, HEIGHT / 2]
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball("LEFT")
    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, acc
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        
        if ( ball_pos[1] >= (paddle1_pos[1] - HALF_PAD_HEIGHT) ) and ( ball_pos[1] <= (paddle1_pos[1] + HALF_PAD_HEIGHT)  ):
            ball_vel[0] = - 1.1 * ball_vel[0]
            acc = acc * 1.1
         
        else:
            score2 += 1
            spawn_ball("RIGHT")
    
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        
        if ( ball_pos[1] >= (paddle2_pos[1] - HALF_PAD_HEIGHT) ) and ( ball_pos[1] <= (paddle2_pos[1] + HALF_PAD_HEIGHT)  ):
            ball_vel[0] = - 1.1 * ball_vel[0]
            acc = acc * 1.1
            
        else:
            score1 += 1
            spawn_ball("LEFT")
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'red', 'red')
    
    # update paddle's vertical position, keep paddle on the screen
    
    if paddle1_pos[1] < HALF_PAD_HEIGHT:
        paddle1_pos = [0, HALF_PAD_HEIGHT]
    
    elif paddle1_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = [0, HEIGHT - HALF_PAD_HEIGHT]
        
    elif paddle2_pos[1] < HALF_PAD_HEIGHT:
        paddle2_pos = [WIDTH, HALF_PAD_HEIGHT] 
        
    elif paddle2_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = [WIDTH, HEIGHT - HALF_PAD_HEIGHT]        

    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel

    
    # draw paddles
    
    canvas.draw_polygon( [ [paddle1_pos[0], paddle1_pos[1] - HALF_PAD_HEIGHT ], [paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0], paddle1_pos[1] + HALF_PAD_HEIGHT] ], 1, 'yellow', 'yellow')
    canvas.draw_polygon( [ [paddle2_pos[0] - PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0], paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0], paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] - PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT] ], 1, 'yellow', 'yellow')
    
    # determine whether paddle and ball collide
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 4, HEIGHT * 1/4], 30, 'white')
    canvas.draw_text(str(score2), [WIDTH * 3/4, HEIGHT * 1/4], 30, 'white')
        
def keydown(key):
    global paddle1_vel, paddle2_vel, acc, HEIGHT
    
    acc = 3
    
    if key == simplegui.KEY_MAP['w'] and paddle1_pos[1] > 0:
        paddle1_vel -= acc
        
    elif key == simplegui.KEY_MAP['s'] and paddle1_pos[1] < HEIGHT:
        paddle1_vel += acc
        
    elif key == simplegui.KEY_MAP['up'] and paddle2_pos[1] > 0:
        paddle2_vel -= acc
        
    elif key == simplegui.KEY_MAP['down'] and paddle2_pos[1] < HEIGHT:
        paddle2_vel += acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel, acc
    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
        
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
        
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
        
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset Game", reset, 100)

# start frame
new_game()
frame.start()
