from socket import socket, AF_INET, SOCK_STREAM, timeout


def request_current_from_ammeter(port: int, command: bytes) -> float:
    """
    Sends a measurement command to a specific ammeter emulator
    and returns the current measurement as float.
    """

    try:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(('localhost', port))
            s.sendall(command)

            data = s.recv(1024)

            if not data:
                raise ValueError(f"No data received from ammeter on port {port}")

            response = data.decode('utf-8')

            if response.startswith("ERROR"):
                raise ValueError(response)

            current = float(response)

            print(f"Received current measurement from port {port}: {current} A")
            return current

    except timeout:
        raise TimeoutError(f"Connection to ammeter on port {port} timed out")

    except ConnectionRefusedError:
        raise ConnectionRefusedError(
            f"Could not connect to ammeter on port {port}. Make sure the emulator is running."
        )

    except ValueError as e:
        raise ValueError(f"Invalid measurement response from port {port}: {e}")