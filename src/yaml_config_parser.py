import yaml
import os
import re


# YAML fájl beolvasása
def read_yaml_file(file_path):
    if not os.path.exists(file_path):  # Ha nem létezik a fájl
        raise FileNotFoundError(f"A(z) {file_path} fájl nem található.")
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:  # Ha a YAML fájl formátuma hibás
        raise ValueError(f"Hiba történt a YAML fájl beolvasása közben: {e}")
    except Exception as e:
        raise Exception(f"Ismeretlen hiba történt a fájl beolvasása közben: {e}")


# Adatok típusellenőrzése
def validate_config_data(config):
    # Ellenőrzés a 'version' mezőre, hogy számokat tartalmazzon
    if 'Application' in config and 'version' in config['Application']:
        version = config['Application']['version']
        if not isinstance(version, str) or not version.replace('.', '').isdigit():
            raise ValueError("A 'version' mezőnek számnak kell lennie, pl. 1.2.3")

    # Ellenőrzés a 'port' mezőre a 'Server' szekcióban, hogy szám legyen
    if 'Server' in config and 'port' in config['Server']:
        port = config['Server']['port']
        if not isinstance(port, int):
            raise ValueError("A 'Server.port' mezőnek egész számnak kell lennie.")

    # Ellenőrzés a 'enabled' mezőre, hogy bool típusú legyen
    if 'Features' in config:
        for feature, settings in config['Features'].items():
            if 'enabled' in settings:
                enabled = settings['enabled']
                if not isinstance(enabled, bool):
                    raise ValueError(f"A '{feature}.enabled' mezőnek boolean értéket kell tartalmaznia.")

    # Ellenőrzés a 'max_size' mezőre, hogy numerikus értéket vagy érvényes mértékegységet tartalmazzon
    if 'Logging' in config and 'file' in config['Logging'] and 'max_size' in config['Logging']['file']:
        max_size = config['Logging']['file']['max_size']

        # Ellenőrizzük, hogy max_size számot vagy szám + mértékegységet tartalmaz
        if isinstance(max_size, str):
            # A regex segítségével ellenőrizzük, hogy szám + opcionális mértékegység (pl. MB, GB) szerepel
            match = re.match(r'^(\d+)(MB|GB|KB)?$', max_size)
            if not match:
                raise ValueError(
                    "A 'max_size' mezőnek számot vagy szám + érvényes mértékegységet (MB, GB, KB) kell tartalmaznia.")
        elif not isinstance(max_size, int):
            raise ValueError("A 'max_size' mezőnek számnak kell lennie.")


# Rekurzív függvény az adatok formázott kiírásához
def write_config(data, file, indent=0):
    try:
        for key, value in data.items():
            if isinstance(value, dict):  # Ha a value egy szótár (nested dict)
                file.write(" " * indent + f"--- {key} ---\n")  # Szekció elválasztó
                write_config(value, file, indent + 2)  # Rekurzív hívás a nested dict-ra
            elif isinstance(value, list):  # Ha a value lista (pl. handlers)
                file.write(" " * indent + f"{key}:\n")
                for item in value:
                    if isinstance(item, dict):
                        file.write(" " * (indent + 2) + "-\n")
                        write_config(item, file, indent + 4)
                    else:
                        file.write(" " * (indent + 2) + f"- {item}\n")
            else:  # Ha az érték egy sima típus (pl. string, int, stb.)
                file.write(" " * indent + f"{key} = {value}\n")

        # Üres sor hozzáadása minden szekció után
        file.write("\n")

    except Exception as e:
        raise Exception(f"Hiba történt a konfigurációs adatok kiírása közben: {e}")


# Fájlba írás
def write_to_output_file(file_path, config_data):
    try:
        with open(file_path, 'w') as output_file:
            write_config(config_data, output_file)
    except PermissionError:  # Ha nincs jogosultság a fájl írásához
        raise PermissionError(f"Nincs jogosultság a(z) {file_path} fájlba való íráshoz.")
    except Exception as e:
        raise Exception(f"Ismeretlen hiba történt a fájl írása közben: {e}")


# Fő program
def main():
    input_file = 'config.yaml'  # A bemeneti YAML fájl neve
    output_file = 'output.txt'  # A kimeneti fájl neve

    try:
        # A YAML fájl beolvasása
        config_data = read_yaml_file(input_file)

        # A konfigurációs adatok validálása
        validate_config_data(config_data)

        # A kimeneti fájlba írás
        write_to_output_file(output_file, config_data)

        print(f"A konfigurációs adatok sikeresen kiírásra kerültek a {output_file} fájlba.")

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except PermissionError as e:
        print(e)
    except Exception as e:
        print(f"Valami hiba történt: {e}")


if __name__ == "__main__":
    main()
