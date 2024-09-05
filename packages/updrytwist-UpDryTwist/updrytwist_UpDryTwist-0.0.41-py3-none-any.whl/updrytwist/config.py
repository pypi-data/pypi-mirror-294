#!/usr/bin/env python

#  Copyright (c) 2024. All rights reserved.

from __future__ import annotations

import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Optional, Union, ClassVar, Any

import yaml

from . import __version__
from . import command_to_config
from . import gentleargparser

#  Copyright (c) 2024. All rights reserved.

DEFAULT_CONFIG = os.getenv( "CONFIGFILE", "myapp.yaml" )
DEFAULT_LOGFILE = os.getenv( "LOGFILE", "myapp.log" )
DEFAULT_ENV_PREFIX = os.getenv( "CONFIG_ENV_PREFIX", "MYAPP" )

DEFAULT_LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOGLEVEL = "INFO"

_LOGGER = logging.getLogger( __name__ )


def convert_keys_to_lowercase(data):
    if isinstance(data, dict):
        return {key.lower(): convert_keys_to_lowercase(value) for key, value in data.items()}
    else:
        return data

def var_to_bool ( input_var : Any ) -> bool:
    """Convert a variable to a boolean value.  Handle expectable values, such as yes,
    true, on, and so forth.  Non-zero integers are true. Raises an exception if none
    of the above."""
    if input_var is None:
        return False
    elif isinstance(input_var, bool):
        return input_var
    elif isinstance(input_var, int):
        return input_var != 0
    elif isinstance(input_var, float):
        return input_var != 0.0
    elif isinstance(input_var, str):
        return str_to_bool(input_var)
    else:
        raise ValueError(f"Cannot convert variable {input_var} of type {type(input_var)} to boolean.")


def str_to_bool ( input_str : str ) -> bool:
    """Convert a string to a boolean value.  Handle expectable values, such as yes,
    true, on, and so forth.  Non-zero integers are true. Raise an exception if can't
    interpret the string."""
    true_values = [ 'yes', 'true', 'on' ]
    false_values = [ 'no', 'false', 'off' ]

    # Convert to lower case to handle case variants
    input_str = str( input_str ).lower()

    # Check if the string can be interpreted as an integer
    try:
        return int( input_str ) != 0
    except ValueError:
        pass

    # Check if the string is in the list of true or false values
    if input_str in true_values:
        return True
    elif input_str in false_values:
        return False

    # Otherwise, raise an exception
    raise ValueError( f"Cannot convert string {input_str} to boolean." )


def legacydictread ( dictionary, key: str, default=None, force_keys_lowercase : Optional[bool]=False ):
    if force_keys_lowercase:
        key = key.lower()
    if dictionary is None:
        return default
    elif key in dictionary:
        return dictionary[ key ]
    else:
        return default


def strreadNoneOk ( object, key: str, default: Optional[ str ] = None, force_keys_lowercase : Optional[bool] = True ) -> str | None:
    value = dictread( object, key, default, force_keys_lowercase )
    return default if value is None else str( value )


def strread ( object, key: str, default: Optional[ str ] = None, force_keys_lowercase : Optional[bool] = True ) -> str:
    value = strreadNoneOk( object, key, default, force_keys_lowercase )
    if value is not None:
        return value
    else:
        raise ValueError( f"Failed to read value {key} from configuration!" )


def dictread ( object, key: str, default : Any =None, force_keys_lowercase : Optional[bool] = True ) -> Any:
    if force_keys_lowercase:
        key = key.lower()
    if object is None:
        return default
    elif isinstance( object, dict ):
        if key in object:
            return object[ key ]
        else:
            return default
    elif isinstance( object, list ):
        if key in object:
            return key
        # could still be a dictionary in the list . . .
        for item in object:
            if isinstance( item, dict ):
                if key in item:
                    return item[ key ]
        return default
    elif isinstance( object, str ):
        # It's an empty block (just the name)
        return default
    else:
        # this is a weird case we shouldn't encounter . . .
        _LOGGER.warning(
                f"Configuration yamlread() encountered unexpected case where object *{object}* is of type {type( object )} and trying to read key {key} with default {default}"
        )
        return default


class ConfigReader:

    def __init__ ( self, readerFunction, force_keys_lowercase : Optional[bool] = True):
        self.readerFunction = readerFunction
        self.force_keys_lowercase = force_keys_lowercase

    def read ( self, key: str, default=None ):
        return self.readerFunction( key, default, self.force_keys_lowercase )

    def forceread ( self, key: str ):
        value = self.read( key, None )
        if value is None:
            raise ValueError( f"Failed to read value {key} from configuration!" )
        return value

    def boolreadNoneOk (
            self, key: str, default: Optional[ bool ] = None
    ) -> Union[ bool, None ]:
        val = self.read( key, default )
        if val is not None:
            return var_to_bool( val )
        else:
            return default

    def boolread ( self, key: str, default: Optional[ bool ] = None ) -> bool:
        value = self.boolreadNoneOk( key, default )
        if value is not None:
            return value
        else:
            raise ValueError( f"Failed to read value {key} from configuration!" )

    def strreadNoneOk (
            self, key: str, default: Optional[ str ] = None
    ) -> Union[ str, None ]:
        val = self.read( key, default )
        if val is not None:
            return str( val )
        else:
            return default

    def strread ( self, key: str, default: Optional[ str ] = None ) -> str:
        value = self.strreadNoneOk( key, default )
        if value is not None:
            return value
        else:
            raise ValueError( f"Failed to read value {key} from configuration!" )

    def intreadNoneOk (
            self, key: str, default: Optional[ int ] = None
    ) -> Union[ int, None ]:
        val = self.read( key, default )
        if val is not None:
            return int( val )
        else:
            return default

    def intread ( self, key: str, default: Optional[ int ] = None ) -> int:
        value = self.intreadNoneOk( key, default )
        if value is not None:
            return value
        else:
            raise ValueError( f"Failed to read value {key} from configuration!" )

    def floatreadNoneOk (
            self, key: str, default: Optional[ float ] = None
    ) -> Union[ float, None ]:
        val = self.read( key, default )
        if val is not None:
            return float( val )
        else:
            return default

    def floatread ( self, key: str, default: Optional[ float ] = None ) -> float:
        value = self.floatreadNoneOk( key, default )
        if value is not None:
            return value
        else:
            raise ValueError( f"Failed to read value {key} from configuration!" )

    def listread ( self, key: str, default: Optional[ list ] = None ) -> [ ]:
        value = self.read( key, default )
        if value is None:
            return [ ]
        elif isinstance( value, list ):
            return value
        else:
            raise ValueError(
                    f"Expected a list for configuration value {key} but got {type( value )}"
            )

    def dictionaryread (
            self, key: str, default: Optional[ list ] = None
    ) -> dict[ str, Any ]:
        value = self.read( key, default )
        if value is None:
            return { }
        elif isinstance( value, dict ):
            return value
        else:
            raise ValueError(
                    f"Expected a dictionary for configuration value {key} but got {type( value )}"
            )


class DictionaryConfigReader( ConfigReader ):

    def __init__ ( self, dictionary: { }, force_keys_lowercase : Optional[bool] = True):
        self.dictionary = dictionary
        super().__init__( self.reader, force_keys_lowercase )

    def reader ( self, key: str, default=None, force_keys_lowercase : Optional[bool] = True):
        return dictread( self.dictionary, key, default, force_keys_lowercase )


def forceread ( dictionary, key: str, force_keys_lowercase : Optional[bool] = True):
    return DictionaryConfigReader( dictionary, force_keys_lowercase ).forceread( key )


def boolreadNoneOk (
        dictionary, key: str, default: Optional[ bool ] = None,
        force_keys_lowercase : Optional[bool] = True
) -> Union[ bool, None ]:
    return DictionaryConfigReader( dictionary, force_keys_lowercase ).boolreadNoneOk( key, default )


def boolread ( dictionary, key: str, default: Optional[ bool ] = None, force_keys_lowercase : Optional[bool] = True ) -> bool:
    return DictionaryConfigReader( dictionary, force_keys_lowercase ).boolread( key, default )


def intreadNoneOk (
        dictionary, key: str, default: Optional[ int ] = None,
        force_keys_lowercase : Optional[bool] = True
) -> Union[ int, None ]:
    return DictionaryConfigReader( dictionary, force_keys_lowercase ).intreadNoneOk( key, default )


def intread ( dictionary, key: str, default: Optional[ int ] = None, force_keys_lowercase : Optional[bool] = True ) -> int:
    return DictionaryConfigReader( dictionary, force_keys_lowercase ).intread( key, default )


def floatreadNoneOk (
        dictionary, key: str, default: Optional[ float ] = None,
        force_keys_lowercase : Optional[bool] = True
) -> Union[ float, None ]:
    return DictionaryConfigReader( dictionary, force_keys_lowercase ).floatreadNoneOk( key, default )


def floatread ( dictionary, key: str, default: Optional[ float ] = None, force_keys_lowercase : Optional[bool] = True ) -> float:
    return DictionaryConfigReader( dictionary, force_keys_lowercase ).floatread( key, default )


def listread ( dictionary, key: str, default: Optional[ list ] = None, force_keys_lowercase : Optional[bool] = True ) -> [ ]:
    return DictionaryConfigReader( dictionary, force_keys_lowercase ).listread( key, default )


def dictionaryread ( dictionary, key: str, default: Optional[ list ] = None, force_keys_lowercase : Optional[bool] = True ) -> dict[
    str, Any ]:
    return DictionaryConfigReader( dictionary, force_keys_lowercase ).dictionaryread( key, default )


class Config:
    c: ClassVar[ "Config" ] = None

    def __init__ (
            self,
            filename: str = None,
            optional_config: bool = False,
            forceDictionary: { } = None,
            force_keys_lowercase : Optional[bool] = True,
            first_try_directory : Optional[str] = None,
    ):
        self.force_keys_lowercase = force_keys_lowercase

        if filename is None:
            filename = DEFAULT_CONFIG

        self.filename = filename
        self.full_file_name = None
        self.first_try_directory = first_try_directory
        self.readCommandLine()

        if not forceDictionary:
            try:
               if self.first_try_directory:
                   full_path = Path( first_try_directory ) / filename
                   try:
                       with open( full_path ) as source:
                           self.read_from_file( source )
                           self.full_file_name = full_path
                   except FileNotFoundError:
                       with open( self.filename ) as source:
                           self.read_from_file( source )
                           self.full_file_name = Path( os.getcwd() ) / self.filename
               else:
                   with open( self.filename ) as source:
                      self.read_from_file( source )
                      self.full_file_name = Path( os.getcwd() ) / self.filename

            except Exception as e:
                if optional_config:
                    self.config = { }
                    self.unmodified_config = { }
                else:
                    raise e
        else:
            self.config = forceDictionary
            self.unmodified_config = self.config
            if self.force_keys_lowercase:
                self.config = convert_keys_to_lowercase(self.config)

    def read_from_file ( self, source):
        self.config = yaml.load( source, Loader=yaml.FullLoader )
        self.unmodified_config = self.config
        if self.force_keys_lowercase:
            self.config = convert_keys_to_lowercase( self.config )

    def merge_dictionary ( self, dictionary: dict[ str, Any ] ):
        self.config = command_to_config.merge_dictionaries( self.config, dictionary )

    def blockFor ( self, fromBlock: str = None, force_keys_lowercase : Optional[bool|None] = None ) -> { }:
        if force_keys_lowercase is None:
            force_keys_lowercase = self.force_keys_lowercase
        if not fromBlock:
            return self.config if force_keys_lowercase else self.unmodified_config
        else:
            if force_keys_lowercase:
                fromBlock = fromBlock.lower()
            config_base = self.config if force_keys_lowercase else self.unmodified_config
            if fromBlock in config_base:
                return config_base[ fromBlock ]
            else:
                return { }

    def value ( self, key: str, default=None, fromBlock: str = None, force_keys_lowercase : Optional[bool|None] = None) -> Any:
        return dictread( self.blockFor( fromBlock, force_keys_lowercase ), key, default, force_keys_lowercase if force_keys_lowercase is not None else self.force_keys_lowercase )

    def boolValueNoneOk (
            self, key: str, default: Optional[ bool ] = None, fromBlock: str = None
    ) -> Union[ bool, None ]:
        return boolreadNoneOk( self.blockFor( fromBlock ), key, default, self.force_keys_lowercase )

    def boolValue (
            self, key: str, default: Optional[ bool ] = None, fromBlock: str = None
    ) -> bool:
        return boolread( self.blockFor( fromBlock ), key, default, self.force_keys_lowercase )

    def strValueNoneOk (
            self, key: str, default: Optional[ str ] = None, fromBlock: str = None
    ) -> Union[ str, None ]:
        return strreadNoneOk( self.blockFor( fromBlock ), key, default, self.force_keys_lowercase )

    def strValue (
            self, key: str, default: Optional[ str ] = None, fromBlock: str = None
    ) -> str:
        return strread( self.blockFor( fromBlock ), key, default, self.force_keys_lowercase )

    def intValueNoneOk (
            self, key: str, default: Optional[ int ] = None, fromBlock: str = None
    ) -> Union[ int, None ]:
        return intreadNoneOk( self.blockFor( fromBlock ), key, default, self.force_keys_lowercase )

    def intValue (
            self, key: str, default: Optional[ int ] = None, fromBlock: str = None
    ) -> int:
        return intread( self.blockFor( fromBlock ), key, default, self.force_keys_lowercase )

    def floatValueNoneOk (
            self, key: str, default: Optional[ float ] = None, fromBlock: str = None
    ) -> Union[ float, None ]:
        return floatreadNoneOk( self.blockFor( fromBlock ), key, default, self.force_keys_lowercase )

    def floatValue (
            self, key: str, default: Optional[ float ] = None, fromBlock: str = None
    ) -> float:
        return floatread( self.blockFor( fromBlock ), key, default, self.force_keys_lowercase )

    def listValue (
            self, key: str, default: Optional[ list ] = None, fromBlock: str = None
    ) -> [ ]:
        return listread( self.blockFor( fromBlock ), key, default, self.force_keys_lowercase )

    def dictionaryValue (
            self, key: str, default: Optional[ dict ] = None, fromBlock: str = None
    ) -> dict[ str, Any ]:
        return dictionaryread( self.blockFor( fromBlock ), key, default, self.force_keys_lowercase )

    @staticmethod
    def get ( key: str, default=None, fromBlock: str = None):
        return Config.c.value( key, default, fromBlock )

    @staticmethod
    def getMandatory ( key: str, fromBlock: str = None ):
        value = Config.c.value( key, None, fromBlock )
        if value is None:
            raise ValueError(
                    f"Failed to read value {key} from configuration! (block = {fromBlock})"
            )
        return value

    @staticmethod
    def getBoolNoneOk (
            key: str, default: Optional[ bool ] = None, fromBlock: str = None
    ) -> Union[ bool, None ]:
        return Config.c.boolValueNoneOk( key, default, fromBlock )

    @staticmethod
    def getBool (
            key: str, default: Optional[ bool ] = None, fromBlock: str = None
    ) -> Union[ bool, None ]:
        return Config.c.boolValue( key, default, fromBlock )

    @staticmethod
    def getIntNoneOk (
            key: str, default: Optional[ int ] = None, fromBlock: str = None
    ) -> Union[ int, None ]:
        return Config.c.intValueNoneOk( key, default, fromBlock )

    @staticmethod
    def getInt ( key: str, default: Optional[ int ] = None, fromBlock: str = None
                 ) -> int:
        return Config.c.intValue( key, default, fromBlock )

    @staticmethod
    def getFloatNoneOk (
            key: str, default: Optional[ float ] = None, fromBlock: str = None
    ) -> Union[ float, None ]:
        return Config.c.floatValueNoneOk( key, default, fromBlock )

    @staticmethod
    def getFloat (
            key: str, default: Optional[ float ] = None, fromBlock: str = None
    ) -> float:
        return Config.c.floatValue( key, default, fromBlock )

    @staticmethod
    def getList ( key: str, default: Optional[ list ] = None, fromBlock: str = None
                  ) -> [ ]:
        return Config.c.listValue( key, default, fromBlock )

    @staticmethod
    def getDictionary ( key: str, default: Optional[ dict ] = None,
                        fromBlock: str = None
                        ) -> dict[ str, Any ]:
        return Config.c.dictionaryValue( key, default, fromBlock )

    def readCommandLine ( self ):
        parser = gentleargparser.GentlerArgParser(
                description="Generic UpDryTwist Command Parser",
                conflict_handler="resolve"
        )
        parser.throwExceptions = False
        parser.add_argument( "--config", help="Path to configuration file",
                             default=None )
        try:
            args = parser.parse_args()
            if "config" in vars( args ):
                fileName = vars( args )[ "config" ]
                if fileName is not None:
                    self.filename = fileName
        except Exception as e:
            _LOGGER.debug(
                    f"Encountered unrecognized command-line arguments but continuing on ({e})."
            )


class CannedConfig( Config ):
    """
    Used to create a canned configuration that can be passed around.  Mostly for unit testing.
    """

    def __init__ ( self, cannedConfig: { }, force_keys_lowercase : Optional[bool] = True):
        super().__init__( filename=None,
                          optional_config=False,
                          forceDictionary=cannedConfig,
                          force_keys_lowercase=force_keys_lowercase )


def getConfig () -> Config:
    return Config.c


def loadConfig ( optional_config: bool = False,
                 merge_command_line : Optional[bool] = True,
                 merge_environment : Optional[bool] = True,
                 force_keys_lowercase : Optional[bool] = True,
                 first_try_directory : Optional[str] = None):
    try:
        Config.c = Config(  filename=None,
                            optional_config=optional_config,
                            force_keys_lowercase=force_keys_lowercase,
                            first_try_directory=first_try_directory)
        if merge_command_line:
            command_line_dictionary = command_to_config.command_line_as_config_dictionary(force_keys_lowercase)
            Config.c.merge_dictionary(command_line_dictionary)
        if merge_environment:
            environment_dictionary = command_to_config.environment_variables_as_config_dictionary(force_keys_lowercase=force_keys_lowercase)
            Config.c.merge_dictionary(environment_dictionary)
    except Exception as e:
        print(
                "Cannot load configuration from file {}: {}".format( DEFAULT_CONFIG,
                                                                     str( e ) )
        )
        sys.exit( 2 )


class LoggingConfiguration:

    def __init__ ( self ):
        pass

    @staticmethod
    def initLogging (
            config: Config, loggingBlock: str = "Logging", baseConfigBlock: str = None
    ):
        loggingConfig = config.value( loggingBlock, None, force_keys_lowercase=False )
        incremental = dictread( loggingConfig, "incremental", False )

        # Clean all handlers out of root . . . need this for testing when we reinitialize the handlers
        root = logging.getLogger()
        for h in list( root.handlers ):
            root.removeHandler( h )

        if incremental or not loggingConfig:
            # if the configuration is incremental, or missing, we set up most of the logging
            # in particular, we need to manage formatter and handler

            logFile = config.value( "logfile", DEFAULT_LOGFILE, baseConfigBlock )
            logFormat = config.value( "logformat", DEFAULT_LOGFORMAT, baseConfigBlock )
            logLevel = config.value( "loglevel", DEFAULT_LOGLEVEL, baseConfigBlock )
            logToConsole = config.value( "logToConsole", False, baseConfigBlock )
            logToFile = config.value( "logToFile", True, baseConfigBlock )

            root = logging.getLogger()
            root.setLevel( logLevel )

            if logToFile:
                handler = logging.FileHandler( logFile )
                # handler.setLevel( logLevel )
                handler.setFormatter( logging.Formatter( logFormat ) )
                root.addHandler( handler )

            if logToConsole:
                handler = logging.StreamHandler( sys.stdout )
                # handler.setLevel( logLevel )
                handler.setFormatter( logging.Formatter( logFormat ) )
                root.addHandler( handler )

        if loggingConfig:
            logging.config.dictConfig( loggingConfig )


def initialize ( optional_config=False,
                 merge_command_line : Optional[bool] = True,
                 merge_environment : Optional[bool] = True,
                 force_keys_lowercase : Optional[bool] = True,
                 first_try_directory : Optional[str] = None):
    loadConfig( optional_config, merge_command_line, merge_environment, force_keys_lowercase, first_try_directory)
    LoggingConfiguration().initLogging( Config.c )
    logger = logging.getLogger( __name__ )
    logger.info( f"Using updrytwist version {__version__} (from {__name__})" )
    logger.info( f"Using configuration file {Config.c.full_file_name} with forced lower-case {force_keys_lowercase}" )
