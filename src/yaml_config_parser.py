import yaml


with open('config.yaml', 'r') as file:

    config = yaml.safe_load(file)


def write_config(data, file, indent=0):
    for key, value in data.items():
        if isinstance(value, dict):
            file.write(" " * indent + f"{key}:\n")
            write_config(value, file, indent + 2)
        elif isinstance(value, list):
            file.write(" " * indent + f"{key}:\n")
            for item in value:
                if isinstance(item, dict):
                    file.write(" " * (indent + 2) + "-\n")
                    write_config(item, file, indent + 4)
                else:
                    file.write(" " * (indent + 2) + f"- {item}\n")
        else:
            file.write(" " * indent + f"{key}: {value}\n")


with open('output.txt', 'w') as output_file:
    write_config(config, output_file)

print("A konfigurációs adatok kiírása befejeződött az output.txt fájlba.")

