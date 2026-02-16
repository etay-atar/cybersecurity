# NeonScan - Advanced Port Scanner

A fast, multi-threaded port scanner with a modern Cyberpunk Web GUI.

## Features
-   **Multi-threaded Scanning**: Fast and efficient.
-   **Web GUI**: Real-time progress tracking with a beautiful neon interface.
-   **CLI Support**: Works as a command-line tool as well.

## Installation

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Web Interface (Recommended)

1.  Start the Flask server:
    ```bash
    python app.py
    ```
2.  Open your browser and go to:
    [http://localhost:5000](http://localhost:5000)

### Command Line Interface

Run the scanner directly from the terminal:
```bash
python simple_port_scanner.py <target> <start_port> <end_port> -t <threads>
```
Example:
```bash
python simple_port_scanner.py localhost 1 1024 -t 100
```

## Testing

To test the scanner, you can run the included dummy server which opens ports 9000-9002:

1.  Open a new terminal.
2.  Run the dummy server:
    ```bash
    python dummy_server.py
    ```
3.  Scan `localhost` ports `9000` to `9005`.
