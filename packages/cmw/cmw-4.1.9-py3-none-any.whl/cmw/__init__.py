from mistletoe import markdown as render_markdown
from pathlib import Path
from shutil import rmtree
from sys import argv
from os import system

def init(input_folder):
    template_path = Path(__file__).parent / "template.html"
    print(f" - Copying boilerplate template.html to {input_folder}")
    path = Path(input_folder)
    path.mkdir(parents=True, exist_ok=True)
    system(f"cp {template_path} {path}")

def main():
    input_dir = 'input'
    output_dir = 'output'
    if len(argv) == 2 and argv[1] == "init":
        init("input")
        return 0
    elif len(argv) >= 3:
        if argv[1] == "init":
            init(argv[2])
            return 0
        else:
            input_dir = argv[1]
            output_dir = argv[2]

    print(f" - Erasing {output_dir}/ directory")
    try:
        rmtree(output_dir)
    except FileNotFoundError:
        pass

    template_path = Path(input_dir) / "template.html"
    if not template_path.exists():
        template_path = Path(__file__).parent / "template.html"

    with template_path.open("r") as template_file:
        template = template_file.read()

    # Load up HEADER
    header_path = Path(input_dir) / "Header.md"
    if header_path.exists():
        with header_path.open("r") as f:
            header = render_markdown(f.read())
    else:
        header = ""

    # Load up FOOTER
    footer_path = Path(input_dir) / "Footer.md"
    if footer_path.exists():
        with footer_path.open("r") as f:
            footer = render_markdown(f.read())
    else:
        footer = ""

    for input_path in Path(input_dir).rglob("*.md"):
        if ".git" in input_path.parts:
            continue
        if input_path.parts[-1] in ["Header.md", "Footer.md"]:
            continue
        with input_path.open("r") as input_file:
            # Load up the Markdown
            markdown = input_file.read()

            # Extract the Heading 1
            title = ''
            description = ''
            non_title_lines = []
            for line in markdown.split("\n"):
                if line.startswith("# "):
                    title = line[2:]
                elif line.startswith("Description: "):
                    description = line.split(maxsplit=1)[1]
                else:
                    non_title_lines.append(line)
            markdown = "\n".join(non_title_lines)

            # Render the content
            html_content = render_markdown(markdown)

            # Generate the output
            html_output = template.replace("DESCRIPTION", description).replace("HEADER", header).replace("FOOTER", footer).replace("TITLE", title).replace("CONTENT", html_content)

            # Get the output path
            output_path = Path(str(input_path).replace(input_dir, output_dir, 1)[:-2]+"html")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to disk
            with output_path.open("w") as output_file:
                output_file.write(html_output)

            # Print status
            print(f" - Converted {input_path} to {output_path}")

    # Copy static files
    for base_path in [Path(input_dir), template_path.parent]:
        for input_path in base_path.rglob(f"*"):
            if ".git" in input_path.parts:
                continue
            if input_path.suffix not in ["", ".py", ".md"] and input_path != template_path:
                with input_path.open("rb") as input_file:
                    # Load up the JS/PNG
                    static_file = input_file.read()

                    # Get the output path
                    output_path = Path(str(input_path).replace(str(base_path), output_dir, 1))

                    # Ensure output directory exists
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    # Write to disk
                    with output_path.open("wb") as output_file:
                        output_file.write(static_file)

                    # Print status
                    if str(input_path).startswith(str(template_path.parent)):
                        input_path = str(input_path).replace(str(base_path), "builtin")
                    print(f" - Copied {input_path} to {output_path}")
    return 0
