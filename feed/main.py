

import serial
import time

def communicate_with_arduino(port, baud_rate):
    try:
        # Open the serial port
        arduino = serial.Serial(port, baud_rate, timeout=2)

        # Send the "Start" command
        arduino.write(b"Start")

        # Read and print the response until "End" is received
        while True:
            response = arduino.readline().decode("utf-8").strip()
            print(response)

            if response == "End":
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the serial port
        if arduino.is_open:
            arduino.close()

def plugin(kernel, lifecycle):
    if lifecycle == "register":
        @kernel.console_command('feedmaterial', help="Feed Material.")
        def example_cmd(command, channel, _, **kwargs):
            communicate_with_arduino("COM4", 9600)
