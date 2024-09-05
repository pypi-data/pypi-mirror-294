#  Copyright (c) 2024. All rights reserved.
"""Provides classes and methods to convert command line arguments to a configuration
dictionary, as well as to read values from environment variables and convert them
to a configuration dictionary"""
import os
import sys
from typing import Any, Optional


def merge_dictionaries ( dict1: dict[ str, Any ], dict2: dict[ str, Any ] ) -> dict[ str, Any ]:
    """Merges two dictionaries, with dict2 taking precedence over dict1"""
    dict3 = dict1.copy()
    for key in dict2:
        if key in dict3:
            if isinstance( dict3[ key ], dict ):
                if isinstance( dict2[ key ], dict ):
                    dict3[ key ] = merge_dictionaries( dict3[ key ], dict2[ key ] )
                else:
                    dict3[ key ] = dict2[ key ]
            else:
                dict3[ key ] = dict2[ key ]
        else:
            dict3[ key ] = dict2[ key ]
    return dict3


def arguments_to_dict ( arguments: list[ str ], force_keys_lowercase : bool = True ) -> dict[ str, Any ]:
    """Converts command line arguments to a configuration dictionary.  Command line
    values are of the form --config_block_block_key=value or --config_block_block_key
    value or block_block_key=value."""
    config = { }
    keys = None
    skip_next_argument = False
    for arg in arguments:
        if skip_next_argument:
            skip_next_argument = False
            continue
        if keys is None:
            can_take_next_argument = False
            keys = arg
            if keys.startswith( "--" ):
                if keys.startswith("--config_"):
                    # OK, this is our guy
                    keys = keys[9:]
                    can_take_next_argument = True
                else:
                    keys = None
                    skip_next_argument = True
                    continue
            if "=" in keys:
                keys, value = keys.split( "=" )
            else:
                if not can_take_next_argument:
                    keys = None
                continue
        else:
            value = arg
        for key in reversed( keys.split( "_" ) ):
            this_config = { key.lower() if force_keys_lowercase else key: value }
            value = this_config
        if isinstance( value, dict ):
            config = merge_dictionaries( config, value )
        keys = None

    return config


def command_line_as_config_dictionary ( force_keys_lowercase : bool = True ) -> dict[ str, Any ]:
    """Converts command line arguments to a configuration dictionary.  Command line
    values are of the form --config_block_block_key=value or --config_block_block_key
    value or block_block_key=value."""
    return arguments_to_dict( sys.argv[1:], force_keys_lowercase )


def environment_variables_as_config_dictionary ( environment_variable_prefix : Optional[str] = None,
                                                 force_keys_lowercase : Optional[bool] = True ) -> dict[ str, Any]:
    """Converts environment variables to a configuration dictionary.  Environment
    variables are of the form BLOCK_BLOCK_KEY=value.  If environment_variable_prefix is
    provided, then we only consider environment variables that start with that prefix."""
    config = { }
    for raw_key, value in os.environ.items():
        if environment_variable_prefix is not None:
            if not raw_key.startswith( environment_variable_prefix + "_" ):
                continue
            raw_key = raw_key[len(environment_variable_prefix)+1:]
        for key in reversed( raw_key.split( "_" ) ):
            this_config = { key.lower() if force_keys_lowercase else key: value }
            value = this_config
        if isinstance( value, dict ):
            config = merge_dictionaries( config, value )
    return config
