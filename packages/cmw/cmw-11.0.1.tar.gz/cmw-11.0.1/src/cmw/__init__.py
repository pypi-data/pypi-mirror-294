from mistletoe import markdown
from cmw.loader import load_yaml_with_dot_access
from pathlib import Path
from sys import argv
from shutil import copy
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from signal import signal

PORT = 8000

httpd = None

def signal_handler(sig, frame):
    """Handle clean shutdown on Ctrl+C."""
    if httpd:
        print("Shutting down server...")
        httpd.server_close()
    sys.exit(0)

def server():
    global httpd
    # Create a signal handler for SIGINT (Ctrl+C)
    signal(signal.SIGINT, signal_handler)
    httpd = TCPServer(("", PORT), SimpleHTTPRequestHandler)
    print()
    print("Development server is running at:")
    print()
    print(f"    http://127.0.0.1:{PORT}")
    print()
    print("Exit with CTRL+C")
    print()
    httpd.serve_forever()

def main():
    this_file_directory = Path(__file__).parent
    template_path = this_file_directory / "template.html"
    config_path = this_file_directory / "config.yaml"
    index_path = this_file_directory / "index.md"
    styles_path = this_file_directory / "styles.css"

    if len(argv) == 2 and argv[1] == "init":
        path = Path(".")
        copy(template_path, path / "template.html")
        copy(config_path, path / "config.yaml")
        copy(index_path, path / "index.md")
        copy(styles_path, path / "styles.css")
        print()
        print(f"Initialized a new project")
        print()
        print("To get started:")
        print()
        print(" 1. Run: cmw server")
        print(" 2. Customize config.yaml")
        print(" 3. Customize index.md")
        print(" 4. If necessary, customize template.html")
        print(" 5. If necessary, customize styles.css")
        print()
        print("Happy coding!")
        print()
        return 0

    server_mode = (len(argv) == 2 and argv[1] == "server")
    build_mode = (len(argv) == 1)

    if not (server_mode or build_mode):
        print("Error: Unknown arguments.")
        return 1

    # Set the template and config paths
    if Path("template.html").exists():
        template_path = Path("template.html")
    if Path("config.yaml").exists():
        config_path = Path("config.yaml")

    # Load up template
    with template_path.open("r") as file:
        template = file.read()

    # Load up config.yaml
    config = load_yaml_with_dot_access(config_path)

    # Construct navigation
    if config.Navigation:
        links = ""
        for item in config.Navigation:
            links += f" <a href='{item.URL}'>{item.Text}</a> "
        navigation = f"<nav>{links}</nav>" 
    else:
        navigation = None

    # Replace the variables that are consistent on every page
    template = template.replace("TITLE", config.Title)
    template = template.replace("HEADING", config.Heading)
    template = template.replace("TAGLINE", config.Tagline if config.Tagline else "")
    template = template.replace("NAVIGATION", navigation if navigation else "")
    template = template.replace("FOOTER", config.Footer if config.Footer else "")

    for input_path in Path(".").rglob("*.md"):
        with input_path.open("r") as input_file:
            # Load up the Markdown and render it
            content = markdown(input_file.read())

            # Generate the output
            html = template.replace("CONTENT", content)

            # Get the output path
            output_path = Path(str(input_path)[:-2] + "html")

            # Write to disk
            with output_path.open("w") as output_file:
                output_file.write(html)

            # Print status
            print(f" - Converted {input_path} to {output_path}")

    if server_mode:
        server()

    return 0
