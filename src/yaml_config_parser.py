import yaml

# Input fájl beolvasása (input.txt)
with open('input.txt', 'r') as file:
    # A fájl tartalmának beolvasása
    yaml_content = file.read()

    # YAML tartalom betöltése a python dict-be
    config = yaml.safe_load(yaml_content)

# Rekurzív függvény az adatok formázott kiírásához
def write_config(data, file, indent=0):
    for key, value in data.items():
        if isinstance(value, dict):
            file.write(" " * indent + f"{key}:\n")
            write_config(value, file, indent + 2)
        else:
            file.write(" " * indent + f"{key}: {value}\n")

# Kimeneti fájlba írás
with open('output.txt', 'w') as output_file:
    write_config(config, output_file)

print("A konfigurációs adatok kiírása befejeződött az output.txt fájlba.")
