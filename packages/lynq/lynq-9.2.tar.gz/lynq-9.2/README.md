# lynq

Lynq for Python is an open-source python framework that allows developers to host servers absurdly easily
(we're talking 1-line easily)
And this isn't even an exaggeration! Once you have Lynq imported, the world is basically in your hands.

Let's look at the most configurable and advanced way to host servers using Lynq,
and move our way down the ladder to the easiest way. First though, let's see how you can get lynq on your own system. Or you can skip this part.

# Install Guide

## Methods

### 1. Use `pip`
DISCLAIMER: This method requires `pip` to be installed on your system.

- Open any command line terminal like powershell, cmd, git bash etc.
- Run this command: `pip install lynq`.
- Done! You now have the newest version of Lynq installed locally on your system.
- Want to upgrade? Run `pip install lynq --upgrade` to automatically download the newest version released currently released on `pip`.
- Use `pip show lynq` to view info and version about lynq on your local system.
- Use `pip uninstall lynq` to uninstall lynq from your local system.

### 2. Clone from GitHub
DISCLAIMER: This method requires the `git` CLI to be installed on your system.

- Open any command line terminal like powershell, cmd, git bash etc.
- Run this command: `git clone https://github.com/elemenom/lynq.git`.
- Complete! Please note that this only creates a directory of lynq, so you may need to run this is each project you need lynq for.
- Updating and uninstalling is done using `rm ./lynq/*; rm -r ./lynq; git clone https://github.com/elemenom/lynq.git` and `rm ./lynq/*; rm -r ./lynq` in Windows PowerShell respectively.

### 3. Download a release from GitHub
DISCLAIMER: This method requires any modern web browser to be installed on your system.

- Open a web browser.
- Navigate to https://github.com/elemenom/lynq/
- Select any release (preferably a stable one).
- Select an installation type and download it.

### 4. Build from source
- You can view the source code for lynq on GitHub

# `ConfigurableLynqServer` Class Documentation

The `ConfigurableLynqServer` class is an extension of the `LynqServer` class that adds flexibility and configurability to the basic HTTP server setup. This class allows the server to be configured either via a JSON configuration file, command-line arguments, or default values. Below is a detailed explanation of its functionality and components.

## Overview

The `ConfigurableLynqServer` class is designed to provide a customizable HTTP server setup by allowing configuration through multiple sources:

1. **Configuration File**: A JSON file containing server settings.
2. **Command-line Arguments**: Options provided via the command line to override or set specific settings.
3. **Default Values**: Fallbacks for when no other configuration is provided.

### Class Definition

```python
class ConfigurableLynqServer(LynqServer):
    def __init__(self, config_file: Optional[str] = None, directory: Optional[str] = None, handler: Optional[Type[http.server.BaseHTTPRequestHandler]] = None):
        config = self.load_config(config_file)
        port = config.get("port", 8000)  # Default to int
        directory = directory or config.get("directory")
        super().__init__(port, directory, handler)

    @staticmethod
    def load_config(config_file: Optional[str]) -> dict:
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                try:
                    config = json.load(f)
                    logger.info(f"Loaded configuration from {config_file}")
                    return config
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing config file: {e}")
        else:
            logger.warning(f"No valid config file found. Using default settings.")
        return {}

    @staticmethod
    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Start a local HTTP server.")
        parser.add_argument('--port', type=int, default=8000, help="Port number to run the server on")
        parser.add_argument('--config', type=str, help="Path to configuration file")
        parser.add_argument('--directory', type=str, help="Directory to serve files from")
        return parser.parse_args()
```

## Constructor: `__init__`

### Parameters

- **`config_file`**: An optional string representing the path to a JSON configuration file. If provided, this file is used to set the server's port and directory.
  
- **`directory`**: An optional string representing the directory from which files will be served. If not provided, it defaults to the directory specified in the configuration file or remains `None`.
  
- **`handler`**: An optional HTTP request handler class. If not specified, a default handler is used.

### Functionality

1. **Load Configuration**: The constructor calls the `load_config` method to load settings from the provided configuration file (if any).

2. **Port Setup**: The server port is determined by checking the loaded configuration for a `"port"` key. If absent, it defaults to `8000`.

3. **Directory Setup**: The directory is set based on the provided argument or from the configuration file if the argument is `None`.

4. **Superclass Initialization**: The constructor calls the superclass (`LynqServer`) constructor with the determined port, directory, and handler.

## Methods

### `load_config(config_file: Optional[str]) -> dict`

#### Description

This static method attempts to load a configuration file in JSON format.

#### Parameters

- **`config_file`**: A string representing the path to the configuration file. It can be `None` if no file is provided.

#### Returns

- A dictionary containing the configuration settings. If the file doesn't exist or can't be parsed, an empty dictionary is returned.

#### Functionality

1. **File Existence Check**: The method checks if the provided configuration file path exists.
  
2. **File Parsing**: If the file exists, it attempts to parse it as JSON. Errors during parsing are logged, and an empty dictionary is returned.
  
3. **Fallback**: If the file doesn't exist or cannot be loaded, a warning is logged, and the method returns an empty dictionary.

### `parse_args() -> argparse.Namespace`

#### Description

This static method parses command-line arguments to provide additional configuration options for the server.

#### Returns

- An `argparse.Namespace` object containing the parsed arguments.

#### Arguments

- **`--port`**: The port number on which the server should run. Defaults to `8000`.
  
- **`--config`**: The path to the configuration file.
  
- **`--directory`**: The directory to serve files from.

#### Usage

This method is typically called when running the server script from the command line, allowing users to override defaults or configuration file settings directly.

## Usage Example

```python
if __name__ == "__main__":
    args = ConfigurableLynqServer.parse_args()
    server = ConfigurableLynqServer(config_file=args.config, directory=args.directory)
    server.serve_forever()
```

In this example:

1. Command-line arguments are parsed.
2. A `ConfigurableLynqServer` instance is created using the parsed arguments.
3. The server is started, serving files from the specified directory and listening on the specified port.

## Summary

The `ConfigurableLynqServer` class offers a flexible way to configure and run an HTTP server. By leveraging configuration files, command-line arguments, and defaults, it provides a robust mechanism to tailor server behavior to various needs.

**`ConfigurableLynqServer` is a great choice for experienced programmers that know what they're doing**

# `LynqServer` Class Documentation

The `LynqServer` class provides a basic, customizable HTTP server capable of serving files from a specified directory. It leverages Python’s `http.server` and `socketserver` modules to handle HTTP requests and manage the server’s lifecycle. Below is a detailed explanation of its functionality and components.

## Overview

The `LynqServer` class is designed to facilitate the creation and management of a simple HTTP server. It provides functionality to:

- Initialize the server with a specific port and directory.
- Create a custom request handler.
- Start and stop the server.
- Automatically open a web browser pointing to the server’s URL.

### Class Definition

```python
class LynqServer:
    def __init__(self, port: int, directory: Optional[str] = None, handler: Optional[Type[http.server.BaseHTTPRequestHandler]] = None):
        self.port: int = port
        self.directory: Path = Path(directory) if directory else Path.cwd()
        self.handler: Type[http.server.BaseHTTPRequestHandler] = handler or self._create_handler()
        try:
            self.httpd: socketserver.TCPServer = socketserver.TCPServer(("localhost", self.port), self.handler)
            self.httpd.directory = str(self.directory)  # Set directory for the server
            logger.info(f"Server initialized on port {self.port} with directory {self.directory}")
        except OSError as e:
            logger.error(f"Could not start server on port {self.port}: {e}")
            raise

    def _create_handler(self) -> Type[http.server.BaseHTTPRequestHandler]:
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def translate_path(self, path: str) -> str:
                # Removes query parameters, etc., from the URL path
                path = path.split('?', 1)[0]
                path = path.split('#', 1)[0]
                path = Path(path).relative_to('/')

                # Combine the requested path with the server's directory
                full_path = self.server.directory / path

                # Resolve the final absolute path
                return str(full_path.resolve())
        return CustomHandler

    def _start_server(self) -> None:
        server_thread: threading.Thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        logger.info(f"Server started on port {self.port}")

    def open(self) -> None:
        self._start_server()
        url = f"http://localhost:{self.port}"
        logger.info(f"Opening browser at {url}")
        webbrowser.open(url)

    def _stop_server(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        logger.info(f"Server on port {self.port} stopped")

    def close(self) -> None:
        self._stop_server()
```

## Constructor: `__init__`

### Parameters

- **`port`**: An integer specifying the port number on which the server will listen.
  
- **`directory`**: An optional string representing the directory from which the server will serve files. If not provided, it defaults to the current working directory (`Path.cwd()`).

- **`handler`**: An optional HTTP request handler class. If not specified, a custom handler is created using the `_create_handler` method.

### Functionality

1. **Port Initialization**: The port is set based on the provided argument.
  
2. **Directory Initialization**: The directory is set to the provided path or defaults to the current working directory.

3. **Request Handler**: The server uses the provided handler or a custom handler created by `_create_handler`.

4. **Server Setup**: The server is initialized with the `socketserver.TCPServer` class, binding it to `localhost` on the specified port and using the configured request handler.

5. **Error Handling**: If the server fails to start (e.g., due to the port being in use), an error is logged, and an `OSError` is raised.

## Methods

### `_create_handler() -> Type[http.server.BaseHTTPRequestHandler]`

#### Description

This private method creates and returns a custom request handler class based on `http.server.SimpleHTTPRequestHandler`.

#### Functionality

- **Path Translation**: The `translate_path` method is overridden to clean the URL path by removing query parameters and fragments. It then combines the cleaned path with the server’s base directory to determine the absolute file path to be served.

### `_start_server() -> None`

#### Description

This private method starts the server in a background thread, allowing it to serve requests indefinitely without blocking the main thread.

#### Functionality

- **Threading**: The server runs in a daemon thread, meaning it will automatically stop when the main program exits.
  
- **Logging**: A message is logged when the server starts successfully.

### `open() -> None`

#### Description

This method starts the server and opens the default web browser to the server's URL.

#### Functionality

- **Start Server**: The server is started using `_start_server`.
  
- **Open Browser**: The server's URL (`http://localhost:{port}`) is opened in the default web browser.

### `_stop_server() -> None`

#### Description

This private method stops the server gracefully by shutting it down and closing the server socket.

#### Functionality

- **Shutdown**: The server's request-handling loop is stopped.
  
- **Close Socket**: The server socket is closed, freeing up the port.
  
- **Logging**: A message is logged indicating that the server has been stopped.

### `close() -> None`

#### Description

This method is a public interface to stop the server by calling `_stop_server`.

#### Functionality

- **Stop Server**: The server is stopped and cleaned up.

## Usage Example

```python
if __name__ == "__main__":
    server = LynqServer(port=8000, directory="/path/to/serve")
    server.open()
    # The server is now running and serving files
    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        server.close()  # Stop the server on Ctrl+C
```

In this example:

1. The server is initialized with a specific port and directory.
2. The server is started, and the default web browser opens to the server's URL.
3. The server runs indefinitely until interrupted (e.g., via `Ctrl+C`), after which it stops gracefully.

## Summary

The `LynqServer` class provides a simple and customizable way to create an HTTP server. With built-in methods for server management and a customizable request handler, it is well-suited for scenarios requiring a lightweight and configurable web server.

**`LynqServer` is a great choice for intermediate programmers that know how this works, but aren't quite experienced enough to tackle `ConfigurableLynqServer`**

# `launch` Function Documentation

The `launch` function is a utility function that simplifies the process of starting a `LynqServer` instance. It is designed to quickly initialize, start, and manage the lifecycle of a basic HTTP server with minimal setup.

## Function Definition

```python
def launch(port: Optional[int] = None, directory: Optional[str] = None) -> None:
    server: LynqServer = LynqServer(port or 8000, directory or ".")

    try:
        server.open()
        input("\033[1;93mPress enter to exit your Lynq server...\n\033[0m")

    finally:
        server.close()
```

### Parameters

- **`port`**: An optional integer specifying the port number on which the server will listen. If not provided, the function defaults to port `8000`.

- **`directory`**: An optional string specifying the directory from which the server will serve files. If not provided, the function defaults to the current directory (`"."`).

### Functionality

1. **Server Initialization**: 
    - The function initializes a `LynqServer` instance using the provided `port` and `directory` arguments. 
    - If either argument is not provided, it falls back to the default values: port `8000` and the current directory (`"."`).

2. **Server Startup**:
    - The `server.open()` method is called to start the server. 
    - This method also opens the default web browser to the server's URL (`http://localhost:{port}`).

3. **User Prompt**:
    - The function waits for user input with a prompt: "Press enter to exit your Lynq server...".
    - The prompt is displayed in yellow text to stand out in the console.

4. **Server Shutdown**:
    - Regardless of how the function exits (either after user input or due to an exception), the server is properly closed by calling `server.close()`.
    - This ensures that the server shuts down gracefully and the port is released.

### Usage Example

```python
if __name__ == "__main__":
    launch(port=8080, directory="/path/to/serve")
```

In this example:

- The `launch` function is called with a specific port (`8080`) and directory (`/path/to/serve`).
- The server starts and serves files from the specified directory.
- The function waits for the user to press enter, after which the server shuts down.

### Summary

The `launch` function provides a convenient way to start and manage a `LynqServer` instance with minimal code. It handles the server’s lifecycle, from initialization to shutdown, and includes user interaction to control when the server should stop running. This makes it an ideal entry point for scripts that need to quickly start a basic HTTP server.

**`launch()` is a great choice for beginners, or basically anybody who just wants to open a server really quickly and efficiently.**

# Summary

*As you saw from the above documentation, Lynq for Python is a quick, efficient web framework that is insanely easy to master, features many different levels of difficulty to appeal to different skill-levels of programmers, and overall is great at it's job; hosting local servers easily, as smooth as butter.*

- All Lynq servers (no matter the type) will run until the heat death of the universe (unless you press enter to exit them manually)

# Lynq x MSIE

You can now host custom instances of internet explorer that very easily allow you to remotely interact with them using their COM objects.

DISCLAIMER: We are *not* partnered with Microsoft or any other company, all material is open source.

# `InternetExplorerInstance` Class Documentation

The `InternetExplorerInstance` class provides a high-level interface for controlling Internet Explorer instances via PowerShell commands. This class allows for launching a new Internet Explorer window, navigating to specific URLs, and refreshing the browser window. It utilizes the PowerShell COM object model to interact with Internet Explorer.

## Overview

The `InternetExplorerInstance` class is designed to facilitate browser automation with Internet Explorer, using PowerShell scripts executed through Python’s `subprocess` module. This class is particularly useful for scripting and testing environments where Internet Explorer is required.

### Class Definition

```python
class InternetExplorerInstance:
    def __init__(self) -> None:
        self.pwie: Callable = lambda cmd: pwsh(f"$ie = New-Object -ComObject \"InternetExplorer.Application\"; {cmd}")

    def open(self) -> None:
        self.pwie("$ie.Visible = $true")
        logger.info("Launched new internet explorer instance")

    def navigate(self, link: Optional[str]) -> None:
        self.pwie(f"$ie.Navigate({repr(link) or 'http://localhost'})")
        logger.info(f"Navigated internet explorer into {link}")

    def refresh(self) -> None:
        self.pwie("$ie.Refresh()")
        logger.info("Refresh internet explorer")
```

## Methods

### `__init__() -> None`

#### Description

The constructor initializes an instance of `InternetExplorerInstance`.

#### Functionality

- **PowerShell Command Wrapper**: Defines a `self.pwie` lambda function to run PowerShell commands that create a new Internet Explorer COM object. This lambda function calls the `pwsh` function with the appropriate PowerShell command string.

### `open() -> None`

#### Description

Launches a new Internet Explorer instance and makes it visible.

#### Functionality

- **PowerShell Command**: Executes a PowerShell command to make the Internet Explorer instance visible.
  
- **Logging**: Logs an informational message indicating that a new Internet Explorer instance has been launched.

### `navigate(link: Optional[str]) -> None`

#### Description

Navigates the Internet Explorer instance to a specified URL.

#### Parameters

- **`link`**: An optional string representing the URL to navigate to. If `None`, it defaults to `http://localhost`.

#### Functionality

- **PowerShell Command**: Executes a PowerShell command to navigate to the specified URL.

- **Logging**: Logs an informational message indicating the URL to which the browser is navigating.

### `refresh() -> None`

#### Description

Refreshes the current page in the Internet Explorer instance.

#### Functionality

- **PowerShell Command**: Executes a PowerShell command to refresh the current page.

- **Logging**: Logs an informational message indicating that the Internet Explorer instance is being refreshed.

## Dependencies

- **PowerShell**: Required to execute PowerShell commands.
- **Internet Explorer**: The class specifically targets Internet Explorer via its COM object model.
- **Python Libraries**: 
  - `subprocess.run`: To execute PowerShell commands from Python.
  - `logging`: To provide logging functionality.

## Example Usage

```python
if __name__ == "__main__":
    ie = InternetExplorerInstance()
    ie.open()  # Launches a new Internet Explorer instance
    ie.navigate("https://www.example.com")  # Navigates to "https://www.example.com"
    ie.refresh()  # Refreshes the current page
```

In this example:

1. An `InternetExplorerInstance` object is created.
2. The `open` method is called to launch a new Internet Explorer window.
3. The `navigate` method is used to direct the browser to a specific URL.
4. The `refresh` method is invoked to refresh the page.

## Summary

The `InternetExplorerInstance` class provides a Python interface to automate Internet Explorer using PowerShell. It supports opening a new browser window, navigating to URLs, and refreshing the page. This class is useful in scenarios where Internet Explorer needs to be controlled programmatically, particularly in testing or automation tasks.

**Microsoft Internet Explorer is deprecated, but it's still a handy tool to view local servers (via localhost), and Lynq let's you do that quickly and easily.**

# New features in Lynq for Python 2.0

## P.E.B.L (Python Embedded Building Language) Documentation

**P.E.B.L (Python Embedded Building Language)** is a lightweight and flexible framework designed to facilitate the dynamic generation and serving of HTML content within a Python environment. It integrates seamlessly with the Lynq ecosystem, leveraging the power of LynqServer and ConfigurableLynqServer to deliver web content directly to the user.

#### Overview

P.E.B.L provides a streamlined interface for creating and managing web pages from within Python scripts. It supports a tag-based structure for building HTML components, enabling users to embed HTML directly in Python with ease. The core component of P.E.B.L is the `PeblApp` class, which manages the generation of HTML files and interacts with Lynq servers to serve this content.

#### Key Components

##### 1. **PeblApp Class**

The `PeblApp` class is the heart of P.E.B.L. It manages the lifecycle of an HTML page, from creation to serving, within a LynqServer environment.

- **Initialization (`__init__`)**:
  
  ```python
  def __init__(self, name: str, server: LynqServer | ConfigurableLynqServer | None = None) -> None:
  ```

  - `name`: The name of the HTML file to be created (without the `.html` extension).
  - `server`: An instance of `LynqServer`, `ConfigurableLynqServer`, or `None`. If provided, this server will be used to serve the generated HTML content.

  **Example**:
  ```python
  app = PeblApp(name="index", server=my_server)
  ```

- **Tag Creation (`tag`)**:

  ```python
  def tag(self, type_: str, args: Optional[str] = None) -> Any:
  ```

  - `type_`: The type of HTML tag to be generated (e.g., `div`, `p`, `a`).
  - `args`: Optional attributes or content for the tag.

  This method returns a `TagObject` which can be further manipulated or directly inserted into the HTML document.

  **Example**:
  ```python
  app.tag("div", "class='container'")
  ```

- **Single Line Insertion (`singular`)**:

  ```python
  def singular(self, ln: str) -> None:
  ```

  - `ln`: A string representing a single line of HTML to be appended to the HTML file.

  This method allows for quick insertion of raw HTML content into the document.

  **Example**:
  ```python
  app.singular("<h1>Welcome to P.E.B.L!</h1>")
  ```

- **Exiting Context (`__exit__`)**:

  ```python
  def __exit__(self, *_) -> None:
  ```

  Automatically invoked when the `PeblApp` instance exits a context manager. This method ensures that the generated HTML content is passed to the server for serving.

  **Example**:
  ```python
  with PeblApp(name="index", server=my_server) as app:
      app.singular("<p>Hello, World!</p>")
  ```

- **Pass to Server (`pass_to_server`)**:

  ```python
  def pass_to_server(self) -> None:
  ```

  This method handles passing the generated HTML file to the provided server instance and launching it. If no server is provided, an error is logged, and an exception is raised.

  **Example**:
  ```python
  app.pass_to_server()
  ```

#### Usage Example

Here's a basic example of using P.E.B.L to generate and serve an HTML page:

```python
from lynq.server import LynqServer
from lynq.app import PeblApp

# Create a LynqServer instance
server = LynqServer(port=8080, directory=".")

# Initialize the PeblApp with the server
with PeblApp(name="index", server=server) as app:
    app.singular("<h1>Hello from P.E.B.L!</h1>")
    app.singular("<p>This is a dynamically generated page.</p>")
```

#### Error Handling

- If no server is provided when attempting to pass the script to a server, an error is logged, and an exception is raised.
  
  **Example Error**:
  ```python
  logger.error("Cannot pass pebl script to server when no server was provided.")
  ```

- The HTML file is automatically removed after it has been served to prevent unnecessary clutter, ensuring a clean working directory.

#### Integration with Lynq

P.E.B.L integrates tightly with Lynq, allowing for a fluid workflow where HTML content can be generated and served within the same Python environment. It leverages the existing `LynqServer` and `ConfigurableLynqServer` classes for this purpose.

This documentation covers the basics of working with P.E.B.L, including the main class `PeblApp`, its methods, and typical usage patterns. For more advanced features or extensions, refer to the full Lynq documentation or explore additional components within the `lynq.app` module.

## Lynq 2.0 Logging with External Terminal Setup

### Overview

Lynq 2.0 introduces an upgraded logging system that allows for more flexible and powerful logging configurations, including the ability to log to an external terminal or console. This enhancement provides developers with better control over logging output, making it easier to monitor and debug applications in real-time.

### Key Features

1. **Enhanced Logging Flexibility**: Configure logging to output to an external terminal, allowing real-time monitoring of log messages.
2. **Customizable Log Formats**: Define custom formats for log messages to suit different needs and preferences.
3. **Advanced Logging Levels**: Utilize different logging levels (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL) for more granular control over what gets logged.
4. **Integration with External Terminal**: Redirect log output to an external terminal for easier access and visibility.

### Setup and Configuration

#### 1. **Initial Configuration**

Lynq 2.0’s logging system can be configured using the `logging` module in Python. To set up logging to an external terminal, you need to configure the logging handlers appropriately.

#### 2. **Configure Logging to an External Terminal**

To direct logs to an external terminal, follow these steps:

##### a. **Import the Required Modules**

```python
import logging
import sys
```

##### b. **Set Up the Logging Configuration**

You can configure logging to output to an external terminal by using the `StreamHandler` provided by Python's `logging` module. This handler can be set up to write log messages to `sys.stdout`, which is the standard output stream often connected to the terminal.

```python
def setuplogging():
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the root logger level

    # Create a stream handler to output to the terminal
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)  # Set the handler level

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)
```

##### c. **Use the Logger in Your Application**

After setting up logging, you can use the logger in your application code to log messages:

```python
def main():
    setuplogging()
    
    logger = logging.getLogger(__name__)
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
if __name__ == "__main__":
    main()
```

#### 3. **Customizing Log Output**

You can further customize the logging output by modifying the `Formatter` in the `setuplogging` function. For example, you can include additional information like module names or line numbers.

##### Example Formatter Customization

```python
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s')
```

#### 4. **Integration with External Terminal Applications**

For enhanced integration, you might use external terminal applications or tools that support real-time log monitoring. Ensure that the terminal is set to receive logs from the standard output.

##### Example: Running a Script in a Terminal

Run your script in a terminal to see the log output directly:

```bash
python your_script.py
```

### Troubleshooting

- **No Logs Appearing**: Ensure that the terminal or console you are using is configured correctly to display standard output.
- **Incorrect Log Levels**: Verify that the logging levels set in `setuplogging` match the levels you are using in your code.
- **Formatting Issues**: If log messages appear incorrectly formatted, check the `Formatter` configuration in the `setuplogging` function.

### Summary

Lynq 2.0’s upgraded logging system provides a robust solution for directing log output to an external terminal, enhancing real-time monitoring and debugging capabilities. By configuring the `StreamHandler` to use `sys.stdout`, you can easily integrate logging into your terminal-based workflows and customize the logging output to meet your needs.

For more advanced configurations and additional features, refer to the [Python logging documentation](https://docs.python.org/3/library/logging.html) and explore Lynq's logging capabilities further.

## Lynq Server Launch Documentation

### Overview

Lynq provides functionality to launch servers with ease through the `directlaunch` and `launch` functions. These functions facilitate starting and stopping `LynqServer` or `ConfigurableLynqServer` instances, handling user interaction and server management in a streamlined manner.

### Functions Overview

#### `directlaunch`

The `directlaunch` function sets up and starts a basic `LynqServer` instance, using default values if no specific configuration is provided.

##### Function Signature

```python
def directlaunch(port: Optional[int] = None, directory: Optional[str] = None) -> None:
```

##### Parameters

- **`port`** (`Optional[int]`): The port number on which the server will listen. Defaults to `8000` if not provided.
- **`directory`** (`Optional[str]`): The directory from which to serve files. Defaults to the current working directory (`"."`) if not provided.

##### Functionality

1. **Initialization**: Creates an instance of `LynqServer` with the specified port and directory.
2. **Starting the Server**: Calls the `open` method to start the server.
3. **User Interaction**: Waits for user input to keep the server running. The prompt message is styled in yellow to indicate the user should press Enter to exit.
4. **Stopping the Server**: Ensures the server is properly closed after exiting the user prompt.

##### Example Usage

```python
# Launch a LynqServer on port 8080 serving from the current directory
directlaunch(port=8080)
```

#### `launch`

The `launch` function starts a server instance, which can be either a `LynqServer` or a `ConfigurableLynqServer`. It is more flexible than `directlaunch` as it accepts any server that adheres to the expected interface.

##### Function Signature

```python
def launch(server: LynqServer | ConfigurableLynqServer):
```

##### Parameters

- **`server`** (`LynqServer | ConfigurableLynqServer`): An instance of `LynqServer` or `ConfigurableLynqServer` that will be started.

##### Functionality

1. **Starting the Server**: Calls the `open` method on the provided server instance to start it.
2. **User Interaction**: Waits for user input to keep the server running. The prompt message is styled in yellow to indicate the user should press Enter to exit.
3. **Stopping the Server**: Ensures the server is properly closed after exiting the user prompt.

##### Example Usage

```python
from lynq.server import LynqServer
from lynq.customserver import ConfigurableLynqServer

# Create a LynqServer instance
server = LynqServer(port=8080, directory=".")

# Launch the server
launch(server)

# Create a ConfigurableLynqServer instance with custom settings
config_server = ConfigurableLynqServer(config_file="config.json")

# Launch the configurable server
launch(config_server)
```

### Error Handling

- **No Server Provided**: Ensure that a valid `LynqServer` or `ConfigurableLynqServer` instance is passed to `launch`. Otherwise, an exception may be raised.

- **Port Conflicts**: If the specified port is already in use, an `OSError` or similar exception may be encountered when trying to start the server.

- **Directory Issues**: Ensure the specified directory exists and is accessible. Incorrect paths may lead to errors when attempting to serve files.

### Summary

The `directlaunch` and `launch` functions provide straightforward methods for starting and stopping Lynq servers. `directlaunch` is a simple wrapper around `LynqServer`, while `launch` offers flexibility by accepting any compatible server instance. Both functions ensure that the server runs interactively, waiting for user input to gracefully shut down.

**The directlaunch function is a rename of the OG launch function, which has been repurposed to run already created servers with the same treatement as directlaunched ones**

> Hey! This is Elekk! I hope you enjoy this new release of Lynq for Python. As you may know, this is an entirely solo open-source project I've been working on.
> If you have _Any__ issues, suggestions, or feedback, please open an issue!

# New features in Lynq v3

- Bug fixes
- P.E.B.L has default supported tags; so instead of `app.tag("html", "arguments")`, you can write `app.html("arguments")`
- P.E.B.L apps are now created using the `appnode` decorator from `lynq.app.app`
- External logging has been changed to run in the terminal you started the server from.
- More logging
- Better clean up
- Many P.E.B.L improvements
- No more log file
- Warn count has been removed
- Other QoL changes

# New features in Lynq v4
- Bug fixes
- Support for Basin config files
- Various improvements and updates to the README.md file
- Better launcher mechanics
- Basin now comes bundled in with the base release of Lynq v4.0.0 for Python and up
- Other QoL changes
- Improved app node
- Improved type annotations and types
- Global type for all LynqServer-like objects: `LynqServerOrRelatedObjects` from `lynqserverorrelated` 
- The pizza is in the oven :>

# New features in Lynq v5

## Changelog

- MANY bug fixes
- Imports in backend files are now harder to get confused by
- Performance enhancements
- More Basin features
- BetterPebl 1 and 2 are fullt implemented
- Cool changes
- P.E.B.L and Basin apps are supercharged with new features and are now created using the `@app() .export` and `@basinapp() .export` decorators respectively.

## lynqconfig

- You can now create a file in the same directory as the importing file(s) (the file(s) that are importing lynq) which will change some properties of how lynq works.
- Make sure to include ALL options or lynq will use defaults for everything. Any options you don't want to modify, just set them to None.

```python
# lynqconfig.py

import logging

LOGGER = None
# This can be a logger object or 'None' for default logger.

LOGGINGCONFIG = {
    "filename": "mylog.log"
}
# Additional arguments for the default logger. 'LOGGER' must be 'None' for this to take effect.

LOGGINGLEVEL = logging.DEBUG
# Modify the 'level' argument for the default logger. 'LOGGER' must be 'None' for this to take effect.

LOGGINGFORMAT = "%(asctime)s, %(levelname)s, %(message)s"
# Modify the 'format' argument for the default logger. 'LOGGER' must be 'None' for this to take effect.

CLEANPYCACHE = False
# This is a new feature in lynq v5. Lynq can now automatically remove all __pycache__ files in the lynq directory. This makes development much easier as it removes the need for manual deletion. Leaving this off might make lynq run slightly faster. Default is 'False'.
```

- More options will be added in the future.
- You can also clean pycache from lynq manually by running `python -m lynq._utils._lynq.manualcleanup` in your command terminal.

## _config

- `_config.py` is the backend file that manages `lynqconfig.py` and the entire logging system. It is not importable*

*learn more at the 'what are _ prefixes' section.

## _utils

- `_utils` is like the closet of useful stuff lynq uses to run how it does. It is not importable*

*learn more at the 'what are _ prefixes' section.

## what are _ prefixes

- If something from lynq is prefixed with '_', this can be an item from a file (for ex. function or variable), it is not importable, which means you should ***not*** import them to your own projects. These items could potentially harm your computer if they aren't handled properly, and it's overall a bad idea and unintended to import them.

## VERSION.md

Just a short markdown file indicating the current running lynq version and how to upgrade.

## Where the heck is `lynq/server.py`???

- All server-related files (`server`, `customserver` and `basinserver`) have been moved to the `lynq.server` **package**.
- `lynq.server` is now located in `lynq.server.standard`
- `lynq.customserver` is now located in `lynq.server.custom`
- `lynq.basinserver` is now located in `lynq.server.basin`

# New features in Lynq v6

## Changelog

- Lynq is A LOT more memory-efficient
- Less files for navigation
- All servers (`LynqServer`, `ConfigurableLynqServer` and `BasinLynqServer`) are now all in one module: `lynq.server`
- `app` and `basinapp` can now both be accessed in the `lynq.app` module

## Complete reworking of PEBL apps
- PEBL apps have been reworked and are much more object oriented now.

### Defining a PEBL app
```python
# index.py

from lynq.app import app
from lynq.server import LynqServer

@app(LynqServer(
    port=8000,
    directory="./"
)) .export .standard
def my_pebl_app(self, name: str, age: int) -> None:
    with self.head() as head:
        ... # Code here

    with self.body() as body:
        with body.p() as p:
            p.singular("Your name is {}, you are {} years old.".format(name, age))
```

In the above example, we create an app called `index`.

**DISCLAIMER: The name of the function/app DOES matter! It defines the name of your app, and therefore the HTML file assigned to it. It is recomended to use `index` for your main app. The name of the python file does not impact anything.**

Now we have an app, but how do we pass it to it's server?

*Spoiler: This has also been reworked*

```python
# main.py

from index import index

index(name="Bob", age=20) .launch()
```

#### How it works:
- The decorator `app` and `basinapp` are classes, so passing the server or basin path respectively are actually passed to `app.__init__`. Then, `app.export` is a custom "Shallow Blank Slate Object" (SBSO) which is also a memory-efficient way to store small classes in memory. After `export` is the "Export Method". Export methods change the way your PEBL app displays. The only export method implemented in Lynq PEBL so far is `standard`. This implements elements normally, like everyone is used to. More export methods will be implemented later on.
- In the `main.py` file, the `index` function is imported, but it's no longer a function because of the decorator. What we're calling `.launch()` on is actually a `StandardAppExportObject`; an object in charge of passing your apps to their dedicated `LynqServer` in Lynq v6.