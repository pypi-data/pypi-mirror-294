from adi_env_parser import EnvironmentParser
from os import environ as env

TEST_DATA_DIR = "adi_env_parser/test_data"


class TestParser:
    def test_parser_empty_objects(self):
        env_prefix = "OBJ"

        expected = {
            "key_one": "value one",
            "key_two": {
                "sub_one": "value_sub_one",
                "sub_two": "value_sub_two"
            }
        }

        env["OBJ_key_one"] = "value one"
        env["OBJ_key_two__sub_one"] = "value_sub_one"
        env["OBJ_key_two__sub_two"] = "value_sub_two"

        parser = EnvironmentParser(env_prefix)
        assert parser.configuration == expected

    def test_parser_empty_lists(self):
        env_prefix = "LIST"

        expected = {
            "list_one": [
                "one",
                "two",
                "three"
            ],
            "key_one": {
                "list_two": [
                    "four",
                    "five"
                ]
            }
        }

        env["LIST_list_one__0"] = "one"
        env["LIST_list_one__1"] = "two"
        env["LIST_list_one__2"] = "three"
        env["LIST_key_one__list_two__0"] = "four"
        env["LIST_key_one__list_two__1"] = "five"

        parser = EnvironmentParser(env_prefix)
        assert parser.configuration == expected

    def test_parser_empty_dictionary_in_list(self):
        env_prefix = "DICTLIST"

        expected = {
            "people": [
                {
                    "name": "John",
                    "surname": "Smith"
                },
                {
                    "name": "Jane",
                    "surname": "Smith"
                }
            ]
        }

        env["DICTLIST_people__0__name"] = "John"
        env["DICTLIST_people__0__surname"] = "Smith"
        env["DICTLIST_people__1__name"] = "Jane"
        env["DICTLIST_people__1__surname"] = "Smith"

        parser = EnvironmentParser(env_prefix)
        assert parser.configuration == expected

    def test_parser_empty_complex(self):
        env_prefix = "TEST"

        expected = {
            "work_tasks": {
                "task_two": "done"
            },
            "work_inventory": [
                "keyboard"
            ],
            "home": {
                "kitchen_inventory": [
                    "cuttlery",
                    "pots"
                ]
            },
            "games": [
                {
                    "title": "Unfathomable",
                    "publisher": "Fantasy Flight Games"
                },
                {
                    "title": "Cartographers",
                    "publisher": "Thunderworks Games"
                }
            ]
        }

        # Set environment for tests
        env["TEST_work_tasks__task_two"] = "done"
        env["TEST_work_inventory__0"] = "keyboard"
        env["TEST_home__kitchen_inventory__0"] = "cuttlery"
        env["TEST_home__kitchen_inventory__1"] = "pots"
        env["TEST_games__4__title"] = "Scythe"
        env["TEST_games__4__publisher"] = "Stonemaier Games"
        env["TEST_games__0__title"] = "Unfathomable"
        env["TEST_games__0__publisher"] = "Fantasy Flight Games"
        env["TEST_games__1__title"] = "Cartographers"
        env["TEST_games__1__publisher"] = "Thunderworks Games"
        env["TEST_games__3__title"] = "Anachrony"
        env["TEST_games__3__publisher"] = "Mindclash Games"

        parser = EnvironmentParser(env_prefix)
        assert parser.configuration == expected

    def test_parser_empty_invalid_list_key(self):
        env_prefix = "TEST2"

        expected = {
            "games": {
                "invalid_list_key": "Not valid list key"
            }
        }

        # Set environment for tests
        env["TEST2_games__invalid_list_key"] = "Not valid list key"
        env["TEST2_games__0__title"] = "Unfathomable"
        env["TEST2_games__0__publisher"] = "Fantasy Flight Games"

        parser = EnvironmentParser(env_prefix)
        assert parser.configuration == expected

    def test_parser_empty_invalid_prefixes(self):
        env_prefix = "TEST3"

        expected = {
            "work_tasks": {
                "task_two": "done"
            }
        }

        # Set environment for tests
        env["TEST3"] = "just base of prefix"
        env["TEST3_"] = "just prefix"
        env["TEST3__"] = "prefix with additional underline"
        env["TEST3__not_valid"] = "prefix with additional underline and " \
            "key word"
        env["TEST3_work_tasks__task_two"] = "done"

        parser = EnvironmentParser(env_prefix)
        assert parser.configuration == expected

    def test_parser_empty_underscore_key(self):
        env_prefix = "TEST4"

        expected = {
            "employee": {
                "surname": "Smith"
            },
            "work_task_one": "done"
        }

        # Set environment for tests
        env["TEST4_employee___name"] = "John"
        env["TEST4_employee__surname"] = "Smith"
        env["TEST4_work_task_one"] = "done"

        parser = EnvironmentParser(env_prefix)
        assert parser.configuration == expected

    def test_exclusion_list(self):
        env_prefix = "IGNORE"
        ignore_prefixes = ["IGNORE_external", "IGNORE_visitor",
                           "IGNORE_exact_match"]

        expected = {
            "employee": {
                "surname": "Smith"
            },
            "externaluser": {
                "surname": "Threepwood"
            },
            "work_task_one": "done"
        }

        # Set environment for tests
        env["IGNORE_employee__surname"] = "Smith"
        env["IGNORE_external__surname"] = "Doe"
        env["IGNORE_external__name"] = "John"
        env["IGNORE_externaluser__surname"] = "Threepwood"
        env["IGNORE_visitor_surname"] = "Manley"
        env["IGNORE_visitor_name"] = "Les"
        env["IGNORE_exact_match"] = "true"
        env["IGNORE_work_task_one"] = "done"

        parser = EnvironmentParser(env_prefix,
                                   prefix_ignore_list=ignore_prefixes)
        assert parser.configuration == expected

    def test_convert_values(self):
        env_prefix = "CONVERT"

        expected = {
            "boolean": {
                "true": True,
                "false": False
            },
            "integer": 123,
            "strings": ["text", "123.0"]
        }

        # Set environment for tests
        env["CONVERT_boolean__true"] = "true"
        env["CONVERT_boolean__false"] = "false"
        env["CONVERT_integer"] = "123"
        env["CONVERT_strings__0"] = "text"
        env["CONVERT_strings__1"] = "123.0"

        parser = EnvironmentParser(env_prefix)
        assert parser.configuration == expected

    def test_no_convert_values(self):
        env_prefix = "CONVERT"

        expected = {
            "boolean": {
                "true": "true",
                "false": "false"
            },
            "integer": "123",
            "strings": ["text", "123.0"]
        }

        parser = EnvironmentParser(env_prefix, convert_values=False)
        assert parser.configuration == expected

    def test_parser_existing_config(self):
        env_prefix = "EXISTING"

        expected = {
            "work_tasks": {
                "task_one": "done",
                "task_two": "done"
            },
            "work_inventory": [
                "laptop",
                "mouse",
                "keyboard"
            ],
            "home": {
                "garage_inventory": [
                    "tools",
                    "lawnmover"
                ],
                "kitchen_inventory": [
                    "cuttlery",
                    "pots"
                ]
            },
            "games": [
                {
                    "title": "Unfathomable",
                    "publisher": "Fantasy Flight Games"
                },
                {
                    "title": "Cartographers",
                    "publisher": "Thunderworks Games"
                }
            ]
        }

        # Set environment for tests
        env["EXISTING_work_tasks__task_two"] = "done"
        env["EXISTING_work_inventory__2"] = "keyboard"
        env["EXISTING_home__kitchen_inventory__0"] = "cuttlery"
        env["EXISTING_home__kitchen_inventory__1"] = "pots"
        env["EXISTING_games__0__title"] = "Unfathomable"
        env["EXISTING_games__0__publisher"] = "Fantasy Flight Games"
        env["EXISTING_games__1__title"] = "Cartographers"
        env["EXISTING_games__1__publisher"] = "Thunderworks Games"

        parser = EnvironmentParser(env_prefix, f"{TEST_DATA_DIR}/base.json")
        assert parser.configuration == expected
