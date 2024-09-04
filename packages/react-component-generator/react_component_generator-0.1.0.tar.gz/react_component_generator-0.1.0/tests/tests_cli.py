import pytest
from unittest.mock import patch, MagicMock
from rich.console import Console
from react_component_generator.cli import app

@patch('react_component_generator.cli.Prompt.ask')
@patch('react_component_generator.cli.Path.exists')
@patch('react_component_generator.cli.Path.mkdir')
@patch('react_component_generator.cli.generate_component')
def test_cli(mock_generate_component, mock_mkdir, mock_exists, mock_ask):
    mock_ask.side_effect = [
        "MyComponent",                  # component_name
        "/path/to/project",             # project_path
        "functional"                    # component_type
    ]
    
    mock_exists.return_value = True
    
    mock_mkdir.return_value = None
    
    runner = app.test_cli()
    
    mock_generate_component.assert_called_once_with(
        component_name="MyComponent",
        component_type="functional",
        components_path=Path("/path/to/project") / "src" / "components"
    )

@patch('react_component_generator.cli.Prompt.ask')
@patch('react_component_generator.cli.Path.exists')
@patch('react_component_generator.cli.Path.mkdir')
@patch('react_component_generator.cli.generate_component')
def test_cli_invalid_path(mock_generate_component, mock_mkdir, mock_exists, mock_ask):
    mock_ask.side_effect = [
        "MyComponent",                  # component_name
        "/invalid/path",                # project_path
        "functional"                    # component_type
    ]
    
    mock_exists.return_value = False
    
    mock_mkdir.return_value = None
    
    runner = app.test_cli()
    
    mock_generate_component.assert_called_once_with(
        component_name="MyComponent",
        component_type="functional",
        components_path=Path.cwd() / "components"
    )
