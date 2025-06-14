import RPi.GPIO as GPIO
import time
import serial
from colorama import Fore, Style

# Stylish Green Banner
def print_banner():
    banner = f"""
{Fore.GREEN}
   ____  _     ___   ____ _  _______ ____  
  | __ )| |   / _ \\ / ___| |/ / ____|  _ \\ 
  |  _ \\| |  | | | | |   | ' /|  _| | | | |
  | |_) | |__| |_| | |___| . \\| |___| |_| |
  |____/|______\\___/ \\____|_|\\_|_____|____/
  
  Bluetooth-Controlled Car
  Coded by Pakistani Ethical Hacker: Mr. Sabaz Ali Khan
  {Style.RESET_ALL}
    """
    print(banner)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Pins (Adjust according to your L298N connections)
IN1 = 17  # Motor A Input 1
IN2 = 18  # Motor A Input 2
IN3 = 22  # Motor B Input 1
IN4 = 23  # Motor B Input 2
ENA = 24  # Enable A (PWM for Motor A)
ENB = 25  # Enable B (PWM for Motor B)

# Setup GPIO pins
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# PWM Setup for speed control
pwm_a = GPIO.PWM(ENA, 100)
pwm_b = GPIO.PWM(ENB, 100)
pwm_a.start(0)
pwm_b.start(0)

# Bluetooth Setup
bluetooth_port = '/dev/rfcomm0'  # Adjust if different
baud_rate = 9600
bluetooth = serial.Serial(bluetooth_port, baud_rate)

# Motor Control Functions
def set_speed(speed):
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Main Program
def main():
    print_banner()
    speed = 50  # Default speed (0-100)
    set_speed(speed)

    try:
        while True:
            if bluetooth.in_waiting > 0:
                command = bluetooth.read().decode('utf-8').strip()
                print(f"Received: {command}")

                if command == 'F':
                    forward()
                elif command == 'B':
                    backward()
                elif command == 'L':
                    left()
                elif command == 'R':
                    right()
                elif command == 'S':
                    stop()
                elif command.isdigit():
                    speed = int(command) * 10  # Scale 0-9 to 0-90
                    set_speed(speed)
                    print(f"Speed set to: {speed}%")

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    finally:
        stop()
        pwm_a.stop()
        pwm_b.stop()
        GPIO.cleanup()
        bluetooth.close()
        print("Cleanup complete.")

if __name__ == "__main__":
    main()