import os
from pathlib import Path
import typer
from rich import print
from rich.console import Console
from rich.prompt import Prompt

app = typer.Typer()
console = Console()

def create_functional_component(component_name: str) -> str:
    """Generate a functional React component."""
    return f"""import React from 'react';
import './{component_name}.css';

const {component_name} = () => {{
  return (
    <div className="{component_name}">
      <h1>{component_name}</h1>
    </div>
  );
}}

export default {component_name};
"""

def create_class_component(component_name: str) -> str:
    """Generate a class-based React component."""
    return f"""import React, {{ Component }} from 'react';
import './{component_name}.css';

class {component_name} extends Component {{
  render() {{
    return (
      <div className="{component_name}">
        <h1>{component_name}</h1>
      </div>
    );
  }}
}}

export default {component_name};
"""

def create_hoc_component(component_name: str) -> str:
    """Generate a Higher-Order React component."""
    return f"""import React from 'react';
import './{component_name}.css';

const {component_name} = (WrappedComponent) => {{
  return (props) => (
    <div className="{component_name}">
      <WrappedComponent {{...props}} />
    </div>
  );
}}

export default {component_name};
"""

def create_pure_component(component_name: str) -> str:
    """Generate a Pure React component."""
    return f"""import React, {{ PureComponent }} from 'react';
import './{component_name}.css';

class {component_name} extends PureComponent {{
  render() {{
    return (
      <div className="{component_name}">
        <h1>{component_name}</h1>
      </div>
    );
  }}
}}

export default {component_name};
"""

def create_memoized_component(component_name: str) -> str:
    """Generate a memoized functional React component."""
    return f"""import React from 'react';
import './{component_name}.css';

const {component_name} = React.memo(() => {{
  return (
    <div className="{component_name}">
      <h1>{component_name}</h1>
    </div>
  );
}});

export default {component_name};
"""

def generate_component(component_name: str, component_type: str, components_path: Path, use_subfolder: bool):
    """Generate the component files based on type and whether to use a subfolder."""
    if use_subfolder:
        component_folder = components_path / component_name
        component_folder.mkdir(parents=True, exist_ok=True)
        component_file_path = component_folder / f"{component_name}.js"
        css_file_path = component_folder / f"{component_name}.css"
    else:
        component_file_path = components_path / f"{component_name}.js"
        css_file_path = components_path / f"{component_name}.css"

    if component_type == "functional":
        component_content = create_functional_component(component_name)
    elif component_type == "class":
        component_content = create_class_component(component_name)
    elif component_type == "hoc":
        component_content = create_hoc_component(component_name)
    elif component_type == "pure":
        component_content = create_pure_component(component_name)
    elif component_type == "memoized":
        component_content = create_memoized_component(component_name)
    else:
        print(f"[red]Invalid component type selected.[/red]")
        return

    with open(component_file_path, "w") as component_file:
        component_file.write(component_content)
    print(f"[green]Component {component_name}.js created successfully![/green]")

    with open(css_file_path, "w") as css_file:
        css_file.write(f".{component_name} {{\n  /* Your styles here */\n}}")
    print(f"[green]CSS file {component_name}.css created successfully![/green]")

    print(f"[blue]Add the component to your project by importing it into the desired file, like so:[/blue]")
    import_path = f'./components/{component_name}/{component_name}' if use_subfolder else f'./components/{component_name}'
    print(f"```javascript\nimport {component_name} from '{import_path}';\n```")

@app.command()
def cli():
    """CLI interface to interactively generate React components."""
    console.print("[bold green]Welcome to the React Component Generator CLI! Damian @ pylds@github[/bold green]")
    
    while True:
        console.print("[bold]Please choose an option:[/bold]")
        console.print("[1] Generate a React Component")
        console.print("[2] Exit")

        choice = Prompt.ask("[bold]Enter your choice[/bold]", choices=["1", "2"], default="1")

        if choice == "2":
            console.print("[bold green]Exiting...[/bold green]")
            break

        if choice == "1":
            component_name = Prompt.ask("[bold]Enter the component name[/bold]")
            project_path = Prompt.ask("Enter the path to your React project", default=os.getcwd())
            components_path = Path(project_path) / "src" / "components"

            if not Path(project_path).exists():
                print(f"[red]The specified project path does not exist. Creating components in a local 'components' folder...[/red]")
                components_path = Path(os.getcwd()) / "components"
            else:
                print(f"[green]Project path found. Generating components in {components_path}...[/green]")

            components_path.mkdir(parents=True, exist_ok=True)

            component_type = Prompt.ask(
                "Select the type of component to generate",
                choices=["functional", "class", "hoc", "pure", "memoized"],
                default="functional"
            )

            use_subfolder = Prompt.ask(
                "Would you like to create a subfolder for the component?",
                choices=["yes", "no"],
                default="no"
            ) == "yes"

            generate_component(component_name, component_type, components_path, use_subfolder)
        else:
            console.print("[red]Invalid choice. Please select a valid option.[/red]")

if __name__ == "__main__":
    app()

