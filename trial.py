import serial
import time
import keyboard

# Establish serial communication with Arduino
ser = serial.Serial('COM4', 9600)  # Replace 'COM3' with the appropriate serial port
time.sleep(2)  # Allow time for the connection to be established

# Function to send commands to the Arduino
def send_command(motor_num, state):
    command = f"{motor_num},{state}"
    ser.write(command.encode())

# Main program loop
while True:
    # Prompt the user for a motor number
    motor_num = input("Enter the motor number (1-6), or 'q' to quit: ")
    
    # Check if the user wants to quit
    if motor_num.lower() == 'q':
        break
    
    # Convert the motor number to an integer
    motor_num = int(motor_num)
    
    # Check if the motor number is within the valid range
    if 1 <= motor_num <= 6:
        # Send command to turn on the motor
        send_command(motor_num, 1)
        
        # Wait for the key to be released
        keyboard.wait(motor_num)
        
        # Send command to turn off the motor
        send_command(motor_num, 0)
    else:
        print("Invalid motor number. Please enter a number between 1 and 6.")

# Close the serial connection
ser.close()
