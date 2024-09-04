# React Component Generator

`react-component-generator` is a CLI tool for generating React components quickly and easily. This generator allows you to create functional, class-based, HOC (Higher-Order Components), pure, and memoized components, including CSS files for styling.

## Installation

You can install `react-component-generator` using pip. Ensure you have pip installed on your system.

```bash
pip install react-component-generator
```

## Usage

Once installed, you can use the tool directly from the command line. Here's how to do it:

### Run the CLI

```bash
react-component-generator
```

This will open the interactive interface where you can select the desired option.

### Available Options

- **Generate a React Component**: Select this option to create a new component.
- **Exit**: Exit the tool.

### Generate a Component

If you choose to generate a component, you will be prompted to enter the component name, your project path, and the type of component you want to create. Available types are:

- **Functional**: Functional component.
- **Class**: Class-based component.
- **HOC (Higher-Order Component)**: HOC component.
- **Pure**: Pure component.
- **Memoized**: Memoized functional component.

The tool will automatically create `.js` and `.css` files for the selected component in the specified path.

## License

This project is licensed under the MIT License.
