"""Config parser to get the configuration for each of the packages being wrapped
by acorn.
"""
packages = {}
"""dict: keys are package names, values are ConfigParser() instances with
configuration information for each package.
"""

def _package_path(package):
    """Returns the full path to the default package configuration file.

    Args:
    package (str): name of the python package to return a path for.    
    """
    from acorn.utility import reporoot
    from os import path
    return path.join(reporoot, "acorn", "config", "{}.cfg".format(package))

def _read_single(parser, filepath):
    """Reads a single config file into the parser, silently failing if the file
    does not exist.

    Args:
    parser (ConfigParser): parser to read the file into.
    filepath (str): full path to the config file.
    """
    from os import path
    global packages
    if path.isfile(filepath):
        parser.readfp(open(filepath))

def settings(package, reload_=False):
    """Returns the config settings for the specified package.

    Args:
        package (str): name of the python package to get settings for.
    """
    global packages
    if package not in packages or reload_:
        from os import path
        try:
            from configparser import ConfigParser
        except ImportError:
            #py3 rename of the module to lower case.
            from ConfigParser import ConfigParser
            
        result = ConfigParser()
        if package != "acorn":
            confpath = _package_path(package)
            _read_single(result, confpath)
        _read_single(result, _package_path("acorn"))
        packages[package] = result

    return packages[package]

def _descriptor_path(package):
    """Returns the full path to the default package configuration file.

    Args:
    package (str): name of the python package to return a path for.    
    """
    from acorn.utility import reporoot
    from os import path
    return path.join(reporoot, "acorn", "config", "{}.json".format(package))

def descriptors(package):
    """Returns a dictionary of descriptors deserialized from JSON for the
    specified package.

    Args:
        package (str): name of the python package to get settings for.
    """
    from os import path
    dpath = _descriptor_path(package)
    if path.isfile(dpath):
        import json
        with open(dpath) as f:
            jdb = json.load(f)
        return jdb
    else:
        return None