import time
import serial


def plugin(kernel, lifecycle):
    if lifecycle == "register":
        @kernel.console_option("port", "p", type=str, default="COM4")
        @kernel.console_option(
            "baud_rate", "b", type=int, default=9600, help="baud rate"
        )
        @kernel.console_option(
            "timeout", "t", type=float, default=20.0, help="timeout in seconds"
        )
        @kernel.console_option(
            "delay", "d", type=float, default=5.0, help="Wait time before sending data info."
        )
        @kernel.console_command('feedmaterial', help="Feed Material.")
        def feedmaterial_cmd(channel, _, port="COM4", baud_rate=9600, timeout=20.0, delay=5.0, **kwargs):
            arduino = None
            try:
                # Open the serial port
                channel("Connecting")
                arduino = serial.Serial(port, baud_rate, timeout=2)
                channel(f"Connected, waiting {delay} seconds.")
                time.sleep(delay)

                channel("Writing Start.")
                # Send the "Start" command
                arduino.write(b"Start\n")

                # Read and print the response until "End" is received
                found = False
                end_time = time.time() + timeout
                while end_time > time.time():
                    response = arduino.readline().decode("utf-8").strip()
                    channel(response)

                    if "end" in response.lower():
                        found = True
                        break
                    if "failed" in response.lower():
                        break
                if not found:
                    channel("Timeout Reached or Failed, aborting...")
                    kernel.console("estop\n")

            except Exception as e:
                channel(f"Error: {e}")
                kernel.console("estop\n")
            finally:
                # Close the serial port
                if arduino is not None and arduino.is_open:
                    arduino.close()
