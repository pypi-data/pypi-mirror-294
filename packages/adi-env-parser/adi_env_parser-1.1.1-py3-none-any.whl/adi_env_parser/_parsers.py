import json
import os
import sys
from typing import Union


class EnvironmentParser:
    def __init__(self, prefix: str = "PYENV", config_file: str = None,
                 convert_values: bool = True, prefix_ignore_list: list = []):
        """Environment Parser
        Parses environment variables prefixed by <prefix>_.
        Different objects within environment variables are separated by __.


        Args:
            prefix (str, optional): Environment variable prefix without _.
                Defaults to "PYENV".
            config_file (str, optional): Existing configuration file to update.
                Defaults to None.
        """
        self.key_delimiter = "__"
        self.namespace = prefix
        self.prefix_ignore_list = prefix_ignore_list
        self.convert_values = convert_values
        self.os_env = self.extract_variables(
            self.namespace, self.prefix_ignore_list
        )
        self.configuration = {} if not config_file else \
            self.load_json_configuration(config_file)
        self.build_configuration()

    def build_configuration(self):
        for k, v in self.os_env.items():
            key_levels = k.split(self.key_delimiter)
            b = self.configuration

            while key_levels:
                current_key = key_levels.pop(0)
                next_key = None if len(key_levels) == 0 else key_levels[0]

                # If it is not the last element, we need to determine whether
                # next element will be a dictionary or list and create it
                if next_key:
                    if isinstance(b, dict):
                        # Do not allow digit elements as dictionary keys, they
                        # are reserved for list indices and this case is likely
                        # a misconfiguration
                        if current_key.isdigit():
                            sys.stderr.write(f"Invalid object property name "
                                             f"{current_key}\n")
                            break
                        # Do not allow dictionary keys starting with _
                        elif current_key.startswith("_"):
                            sys.stderr.write(f"Invalid object property name "
                                             f"{current_key}\n")
                            break
                        b = b.setdefault(current_key, [] if next_key.isdigit()
                                         else {})
                    elif isinstance(b, list):
                        if len(b) > int(current_key):
                            b = b[int(current_key)]
                        elif len(b) == int(current_key):
                            b.append({})
                            b = b[int(current_key)]
                        else:
                            sys.stderr.write(f"Index {current_key} out of "
                                             f"bounds for list of length "
                                             f"{len(b)}\n")
                            break
                # If it is the last element, we need to either set the value
                # of the dictionary key or set the value of the list index
                else:
                    if isinstance(b, dict):
                        # Do not allow digit elements as dictionary keys, they
                        # are reserved for list indices and this case is likely
                        # a misconfiguration
                        if current_key.isdigit():
                            sys.stderr.write(f"Invalid object property name "
                                             f"{current_key}\n")
                            break
                        # Do not allow dictionary keys starting with _
                        elif current_key.startswith("_"):
                            sys.stderr.write(f"Invalid object property name "
                                             f"{current_key}\n")
                            break
                        b[current_key] = self._convert_value(v)
                    elif isinstance(b, list):
                        if not current_key.isdigit():
                            sys.stderr.write(f"Invalid list index "
                                             f"{current_key}\n")
                            break
                        if len(b) > int(current_key):
                            b[int(current_key)] = self._convert_value(v)
                        elif len(b) == int(current_key):
                            b.append(self._convert_value(v))
                        # In case index order defined in environment variables
                        # is incorrect, skip that variable.
                        else:
                            sys.stderr.write(f"Index {current_key} out of "
                                             f"bounds for list of length "
                                             f"{len(b)}\n")
                            break

    def _convert_value(self, value: str) -> Union[str, bool]:
        if not self.convert_values:
            return value

        if value.isdigit():
            return int(value)

        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return False

        return value

    @staticmethod
    def extract_variables(namespace: str, prefix_ignore_list: list) -> dict:
        """Extract variables belonging to namespace

        Args:
            namespace (str): Environment variable namespace (prefix)

        Returns:
            dict: Dictionary containing only variables belonging to namespace
        """
        def variable_in_ignore_list(variable, ignore_list):
            for prefix in ignore_list:
                pfx = prefix + "_"
                if variable.startswith(pfx):
                    return True
                if variable == prefix:
                    return True
            return False

        extracted = {}
        pfx = namespace + "_"
        for variable_name in os.environ.keys():
            if variable_in_ignore_list(variable_name, prefix_ignore_list):
                continue
            if variable_name.startswith(pfx):
                # With Python 3.9 remove_prefix function could be used
                no_pfx_name = variable_name[len(pfx):]

                # Do not allow empty env variables or those starting with _
                if len(no_pfx_name) == 0 or no_pfx_name.startswith("_"):
                    continue

                extracted.update(
                    {no_pfx_name: os.environ.get(variable_name)}
                )

        return extracted

    @staticmethod
    def load_json_configuration(file_path: str) -> dict:
        """Load JSON formated configuration file

        Args:
            file_path (str): Path to configuration file

        Returns:
            dict: Configuration dictionary
        """
        with open(file_path, "r") as file:
            return json.load(file)
