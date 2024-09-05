#  Copyright (c) 2024. All rights reserved.

from updrytwist import command_to_config

def test_merge_dictionaries_with_overlapping_keys():
    dict1 = {"key1": "value1", "key2": {"subkey1": "subvalue1"}}
    dict2 = {"key2": {"subkey2": "subvalue2"}, "key3": "value3"}
    result = command_to_config.merge_dictionaries(dict1, dict2)
    assert result == {"key1": "value1", "key2": {"subkey1": "subvalue1", "subkey2": "subvalue2"}, "key3": "value3"}

def test_merge_dictionaries_with_non_overlapping_keys():
    dict1 = {"key1": "value1"}
    dict2 = {"key2": "value2"}
    result = command_to_config.merge_dictionaries(dict1, dict2)
    assert result == {"key1": "value1", "key2": "value2"}

def test_arguments_to_dict_with_valid_arguments():
    arguments = ["--config_key1=value1", "--config_key2=value2"]
    result = command_to_config.arguments_to_dict(arguments)
    assert result == {"key1": "value1", "key2": "value2"}

def test_arguments_to_dict_with_valid_arguments_and_force_keys_lowercase():
    arguments = ["--config_keY1=value1", "--config_KEY2=value2"]
    result = command_to_config.arguments_to_dict(arguments, force_keys_lowercase=True)
    assert result == {"key1": "value1", "key2": "value2"}


def test_arguments_to_dict_with_nested_blocks():
    arguments = ["--config_block1_block2_key1=value1", "--config_block1_block2_key2=value2"]
    result = command_to_config.arguments_to_dict(arguments)
    assert result == {"block1": {"block2": {"key1": "value1", "key2": "value2"}}}


def test_arguments_to_dict_with_nested_unmerging_blocks():
    arguments = ["--config_block1_block2_key1=value1", "--config_block1_block3_key2=value2"]
    result = command_to_config.arguments_to_dict(arguments)
    assert result == {"block1": {"block2": {"key1": "value1"}, "block3": {"key2": "value2"}}}


def test_arguments_to_dict_with_replacement():
    arguments = ["--config_block1_block2_key1=value1", "--config_block1_block2_key1=value2"]
    result = command_to_config.arguments_to_dict(arguments)
    assert result == {"block1": {"block2": {"key1": "value2" }}}


def test_arguments_to_dict_with_invalid_arguments():
    arguments = ["--invalid_key1=value1", "--invalid_key2=value2"]
    result = command_to_config.arguments_to_dict(arguments)
    assert result == {}

def test_command_line_as_config_dictionary_with_valid_arguments(monkeypatch):
    monkeypatch.setattr('sys.argv', ['program_name', '--config_key1=value1', '--config_key2=value2'])
    result = command_to_config.command_line_as_config_dictionary()
    assert result == {"key1": "value1", "key2": "value2"}

def test_environment_variables_as_config_dictionary_with_valid_variables(monkeypatch):
    monkeypatch.setattr('os.environ', {'BLOCK_KEY1': 'value1', 'BLOCK_KEY2': 'value2'})
    result = command_to_config.environment_variables_as_config_dictionary('BLOCK')
    assert result == {"key1": "value1", "key2": "value2"}

def test_environment_variables_as_config_dictionary_with_invalid_variables(monkeypatch):
    monkeypatch.setattr('os.environ', {'INVALID_KEY1': 'value1', 'INVALID_KEY2': 'value2'})
    result = command_to_config.environment_variables_as_config_dictionary('BLOCK')
    assert result == {}