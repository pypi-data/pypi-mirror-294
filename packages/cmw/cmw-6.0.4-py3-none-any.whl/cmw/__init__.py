from mistletoe import markdown
from cmw.loader import load_yaml_with_dot_access
from pathlib import Path

def main():
    # Load up template
    template_path = Path(__file__).parent / "template.html"
    with template_path.open("r") as file:
        template = file.read()

    # Load up config.yaml
    config = load_yaml_with_dot_access("config.yaml")

    # Construct navigation
    if config.Navigation:
        links = ""
        for item in config.Navigation:
            links += f"<a href='{item.URL}'>{item.Text}</a>"
        navigation = f"<nav>{links}</nav>" 

    # Replace the variables that are consistent on every page
    if config.Title:
        template = template.replace("TITLE", config.Title)
    if config.Heading:
        template = template.replace("HEADING", config.Heading)
    if config.Tagline:
        template = template.replace("TAGLINE", config.Tagline)
    if config.Navigation:
        template = template.replace("NAVIGATION", navigation)
    if config.Footer:
        template = template.replace("FOOTER", config.Footer)

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
    return 0
