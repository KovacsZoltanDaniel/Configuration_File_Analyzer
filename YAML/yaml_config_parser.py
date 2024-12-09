import yaml

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def validate_data(data):
    errors = []

    def validate_section(section, path="root"):
        for key, value in section.items():
            current_path = f"{path}.{key}"
            if isinstance(value, dict):
                validate_section(value, current_path)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        validate_section(item, f"{current_path}[{i}]")
            elif isinstance(value, str):
                if any(kw in key.lower() for kw in ["port", "time", "seconds", "minutes"]):
                    if not value.isdigit():
                        errors.append(f"Invalid value at {current_path}: expected a number, got '{value}'")

    validate_section(data)
    return errors

def write_parsed_yaml(data, output_file):
    def parse_section(section, indent=0):
        output = []
        for key, value in section.items():
            if isinstance(value, dict):
                output.append(f"{'  ' * indent}--- {key} ---")
                output.extend(parse_section(value, indent + 1))
                output.append('')
            elif isinstance(value, list):
                output.append(f"{'  ' * indent}{key} =")
                for item in value:
                    output.append(f"{'  ' * (indent + 1)}- {item}")
                output.append('')
            else:
                output.append(f"{'  ' * indent}{key} = {value}")
        return output

    parsed_data = parse_section(data)

    with open(output_file, 'w') as file:
        file.write('\n'.join(parsed_data))

def get_key_values(data, key_path):
    keys = key_path.split('.')
    current = data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current

if __name__ == "__main__":
    input_file = "config.yaml"
    output_file = "output.txt"

    yaml_data = load_yaml(input_file)

    validation_errors = validate_data(yaml_data)
    if validation_errors:
        print("Validation errors found:")
        for error in validation_errors:
            print(f"- {error}")
    else:
        choice = input("Do you want to print the entire YAML file or query a specific key? (Enter 'all' or 'key'): ").strip().lower()

        if choice == 'all':
            write_parsed_yaml(yaml_data, output_file)
            print(f"Parsed YAML data written to {output_file}")
        elif choice == 'key':
            key_path = input("Enter the key path (e.g., 'root.section.subsection'): ").strip()
            value = get_key_values(yaml_data, key_path)

            if value is not None:
                print(f"Value for '{key_path}': {value}")
            else:
                print(f"Key '{key_path}' not found in the YAML data.")
        else:
            print("Invalid choice. Please enter 'all' or 'key'.")
