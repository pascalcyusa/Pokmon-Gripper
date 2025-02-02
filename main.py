import RPi.GPIO as GPIO
import time

# Set BOARD numbering system (physical pins)
GPIO.setmode(GPIO.BOARD)

# Motor Driver Pins (L298N)
OUT1 = 31
OUT2 = 33
OUT3 = 35
OUT4 = 37

# Stepper Motor Sequence (Full-step)
STEP_SEQUENCE = [
    (1, 0, 1, 0),  # OUT1, OUT2, OUT3, OUT4
    (0, 1, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 0, 1)
]

# Global variables
current_step = 0
step_delay = 0.1  # Increase this value to slow down the motor

def setup():
    # Motor pins setup
    GPIO.setup(OUT1, GPIO.OUT)
    GPIO.setup(OUT2, GPIO.OUT)
    GPIO.setup(OUT3, GPIO.OUT)
    GPIO.setup(OUT4, GPIO.OUT)

def move_motor(steps, direction):
    global current_step
    for _ in range(abs(steps)):
        if direction == 1:
            current_step = (current_step + 1) % len(STEP_SEQUENCE)
        else:
            current_step = (current_step - 1) % len(STEP_SEQUENCE)
        set_motor_pins(STEP_SEQUENCE[current_step])
        time.sleep(step_delay)

def set_motor_pins(step):
    GPIO.output(OUT1, step[0])
    GPIO.output(OUT2, step[1])
    GPIO.output(OUT3, step[2])
    GPIO.output(OUT4, step[3])

def main():
    setup()
    try:
        # Move motor in one direction for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 10:
            move_motor(1, 1)  # Move one step forward

        # Move motor in the opposite direction for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 12:
            move_motor(1, -1)  # Move one step backward

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

