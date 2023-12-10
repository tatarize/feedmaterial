import time

import serial


def communicate_with_arduino(port, baud_rate, channel=print):
    arduino = None
    try:
        # Open the serial port
        channel("Connecting")
        arduino = serial.Serial(port, baud_rate, timeout=2)
        channel("Connected, waiting 5 seconds.")
        time.sleep(5.0)

        channel("Writing Start.")
        # Send the "Start" command
        arduino.write(b"Start\n")

        # Read and print the response until "End" is received
        while True:
            response = arduino.readline().decode("utf-8").strip()
            channel(response)

            if "end" in response.lower():
                break

    except Exception as e:
        channel(f"Error: {e}")
    finally:
        # Close the serial port
        if arduino is not None and arduino.is_open:
            arduino.close()


def plugin(kernel, lifecycle):
    if lifecycle == "register":
        @kernel.console_option('com_port', 'c', type=str, default="COM4")
        @kernel.console_command('feedmaterial', help="Feed Material.")
        def example_cmd(command, channel, _, com_port="COM4", **kwargs):
            communicate_with_arduino(com_port, 9600, channel=channel)
