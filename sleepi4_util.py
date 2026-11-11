import configparser
import sys


PROGRAM_VERSION = '1.0'

DEFAULT_I2C_ADDRESS = '0x6E'
DEFAULT_I2C_BUS = '1'

USAGE = """
Usage: sleepi4ctl COMMAND [OPTION...]

Commands:
    -g, get PARAMETER [<CHANNEL>]            get sleepi4 parameter
    
    -s, set PARAMETER [<CHANNEL>] <VALUE>    set sleepi4 parameter
    
    -h, help                                 display help and exit
    
    -v, version                              display version and exit
"""

GET_USAGE = """
Get Command Usage:
    sleepi4ctl get PARAMETER [<CHANNEL>]

Get Command Parameters:
"""

GET_PARAMETERS = {
    'extin': '<1|2>                 external input state',
    'extin-count': '<1|2>           time of external input is detected [Sec]',
    'extin-powerdown': '<1|2>       external input power down enable flag',
    'extin-trigger': '<1|2>         external input trigger',
    'extout': '<1|2>                external output state',
    'restart': '                    auto restart',
    'ri-trigger': '                 ring indicator trigger',
    'switch': '                     push switch state',
    'switch-count': '               time of push switch is pressed [Sec]',
    'sleep-timeout': '              sleep timeout [Sec]',
    'watchdog-timeout': '           watchdog timeout [Sec]',
    'watchdog-boot-timeout': '      watchdog timeout when boot [Sec]',
    'voltage': '<1|2|active|all>    power supply voltage [mV]',
    'voltage ': '                   same as active',
    'current': '                    supply current [mA]',
    'power': '                      supply power [mW]',
    'energy': '                     supply energy [mWh]',
    'measurement-interval': '       voltage measurement interval [Sec]',
    'restore-voltage': '<1|2>       voltage to detect powering [mV]',
    'uvlo': '<1|2>                  under voltage lock out',
    'wakeup-flag': '                wakeup status flag',
    'wakeup-status': '              wakeup status',
}

SET_USAGE = """
Set Command Usage:
    sleepi4ctl set PARAMETER [<CHANNEL>] <VALUE>

Set Command Parameters and Values:
"""

SET_PARAMETERS = {
    'extin-powerdown': '<1|2> <0|1>       external input power down enable',
    'extin-trigger': '<1|2> <0|1>         external input trigger',
    'extout': '<1|2> <0|1>                external output state',
    'restart': '<0|1>                     auto restart',
    'ri-trigger': '<0|1>                  ring indicator trigger',
    'sleep-timeout': '<0..255>            sleep timeout [Sec]',
    'watchdog-timeout': '<0..255>         watchdog timeout [Sec]',
    'watchdog-boot-timeout': '<0..255>    watchdog timeout when boot [Sec]',
    'energy': '<0>                        supply energy [mWh] (zero clear)',
    'measurement-interval': '<0..255>     voltage measurement interval [Sec]',
    'restore-voltage': '<1|2> <0..48000>  voltage to detect powering [mV]',
    'uvlo': '<1|2> <0|1>                  under voltage lock out',
}

SET_RANGES = {
    'extin-powerdown': (0, 1),
    'extin-trigger': (0, 1),
    'extout': (0, 1),
    'restart': (0, 1),
    'ri-trigger': (0, 1),
    'sleep-timeout': (0, 255),
    'watchdog-timeout': (0, 255),
    'watchdog-boot-timeout': (0, 255),
    'energy': (0, 0),
    'measurement-interval': (0, 255),
    'restore-voltage': (0, 48000),
    'uvlo': (0, 1),
}


def _generate_get_usage():
    usage = GET_USAGE
    for key, val in sorted(GET_PARAMETERS.items()):
        usage += f"    {key} {val}\n"
    return usage


def _generate_set_usage():
    usage = SET_USAGE
    for key, val in sorted(SET_PARAMETERS.items()):
        usage += f"    {key} {val}\n"
    return usage


def help(command):
    if command == 'get':
        help_text = _generate_get_usage()
    elif command == 'set':
        help_text = _generate_set_usage()
    else:
        help_text = USAGE
        help_text += _generate_get_usage()
        help_text += _generate_set_usage()
    return help_text


def version():
    return f"sleepi4ctl version {PROGRAM_VERSION}"


def parse_environment(path):
    parser = configparser.ConfigParser()
    parser.read_dict({'DEFAULT': {
        'I2C_ADDRESS': DEFAULT_I2C_ADDRESS,
        'I2C_BUS': DEFAULT_I2C_BUS,
    }})
    
    with open(path, 'r') as file:
        string = file.read()
    
    parser.read_string('[env]' + string)
    env = parser['env']
    
    return env


class Value:
    def __init__(self, regs, props):
        self.reg = regs[props['name']]
    
    def write(self, val):
        self.reg.value = val
     
    def read(self):
        return self.reg.value


class AllValues(Value):
    def __init__(self, regs, props):
        self.regs = []
        for name in props['names']:
            self.regs.append(regs[name])
    
    def read(self):
        return " ".join(str(reg.read()) for reg in self.regs)


class MaxInValues(Value):
    def __init__(self, regs, props):
        self.regs = []
        for name in props['names']:
            self.regs.append(regs[name])
    
    def read(self):
        return max(reg.read() for reg in self.regs)


class Flag:
    def __init__(self, regs, props):
        self.reg = regs[props['name']]
        self.flag = props['flag']
    
    def write(self, val):
        self.reg.flags[self.flag] = val
    
    def read(self):
        return self.reg.flags[self.flag]


class WakeupFlags(Value):
    def read(self):
        names = (
            'poweron',
            'watchdog',
            'alarm',
            'switch',
            'extin1',
            'ri',
            'restoration1',
            'uvlo1',
            '',
            '',
            '',
            '',
            'extin2',
            '',
            'restoration2',
            'uvlo2'
        )
        active_flags = [name for i, name in enumerate(names) if name and (self.reg.value & (1 << i))]
        return " ".join(active_flags)
    

class Sleepi4Cli:
    
    def __init__(self, sleepi4):
        self.sleepi4 = sleepi4
        self.table = {
            'extin': {
                '1': {
                    'class': Flag,
                    'properties': {
                        'name': 'input_status',
                        'flag': 'ei1'
                    }
                },
                '2': {
                    'class': Flag,
                    'properties': {
                        'name': 'input_status',
                        'flag': 'ei2'
                    }
                }
            },
            'extin-count': {
                '1': {
                    'class': Value,
                    'properties': {
                        'name': 'external_input_count1'
                    }
                },
                '2': {
                    'class': Value,
                    'properties': {
                        'name': 'external_input_count2'
                    }
                }
            },
            'extin-powerdown': {
                '1': {
                    'class': Flag,
                    'properties': {
                        'name': 'input_control',
                        'flag': 'ei1pde'
                    }
                },
                '2': {
                    'class': Flag,
                    'properties': {
                        'name': 'input_control',
                        'flag': 'ei2pde'
                    }
                }
            },
            'extin-trigger': {
                '1': {
                    'class': Flag,
                    'properties': {
                        'name': 'input_control',
                        'flag': 'ei1trg'
                    }
                },
                '2': {
                    'class': Flag,
                    'properties': {
                        'name': 'input_control',
                        'flag': 'ei2trg'
                    }
                }
            },
            'extout': {
                '1': {
                    'class': Flag,
                    'properties': {
                        'name': 'output_control',
                        'flag': 'eo1'
                    }
                },
                '2': {
                    'class': Flag,
                    'properties': {
                        'name': 'output_control',
                        'flag': 'eo2'
                    }
                }
            },
            'restart': {
                None: {
                    'class': Flag,
                    'properties': {
                        'name': 'wakeup_control',
                        'flag': 'rste'
                    }
                }
            },
            'ri-trigger': {
                None: {
                    'class': Flag,
                    'properties': {
                        'name': 'input_control',
                        'flag': 'ritrg'
                    }
                }
            },
            'switch': {
                None: {
                    'class': Flag,
                    'properties': {
                        'name': 'input_status',
                        'flag': 'sw'
                    }
                }
            },
            'switch-count': {
                None: {
                    'class': Value,
                    'properties': {
                        'name': 'push_switch_count'
                    }
                }
            },
            'sleep-timeout': {
                None: {
                    'class': Value,
                    'properties': {
                        'name': 'sleep_timeout'
                    }
                }
            },
            'watchdog-timeout': {
                None: {
                    'class': Value,
                    'properties': {
                        'name': 'watchdog_timeout'
                    }
                }
            },
            'watchdog-boot-timeout': {
                None: {
                    'class': Value,
                    'properties': {
                        'name': 'initial_watchdog_timeout'
                    }
                }
            },
            'voltage': {
                None: {
                    'class': MaxInValues,
                    'properties': {
                        'names': ['voltage1', 'voltage2']
                    }
                },
                'active': {
                    'class': MaxInValues,
                    'properties': {
                        'names': ['voltage1', 'voltage2']
                    }
                },
                'all': {
                    'class': AllValues,
                    'properties': {
                        'names': ['voltage1', 'voltage2']
                    }
                },
                '1': {
                    'class': Value,
                    'properties': {
                        'name': 'voltage1'
                    }
                },
                '2': {
                    'class': Value,
                    'properties': {
                        'name': 'voltage2'
                    }
                }
            },
            'restore-voltage': {
                '1': {
                    'class': Value,
                    'properties': {
                        'name': 'restore_voltage1'
                    }
                },
                '2': {
                    'class': Value,
                    'properties': {
                        'name': 'restore_voltage2'
                    }
                }
            },
            'measurement-interval': {
                None: {
                    'class': Value,
                    'properties': {
                        'name': 'adc_interval'
                    }
                }
            },
            'uvlo': {
                '1': {
                    'class': Flag,
                    'properties': {
                        'name': 'wakeup_control',
                        'flag': 'uvlo1'
                    }
                },
                '2': {
                    'class': Flag,
                    'properties': {
                        'name': 'wakeup_control',
                        'flag': 'uvlo2'
                    }
                }
            },
            'wakeup-status': {
                None: {
                    'class': Value,
                    'properties': {
                        'name': 'wakeup_status'
                    }
                }
            },
            'wakeup-flag': {
                None: {
                    'class': WakeupFlags,
                    'properties': {
                        'name': 'wakeup_status'
                    }
                }
            },
            'current': {
                None: {
                    'class': Value,
                    'properties': {
                        'name': 'current'
                    }
                }
            },
            'power': {
                None: {
                    'class': Value,
                    'properties': {
                        'name': 'power'
                    }
                }
            },
            'energy': {
                None: {
                    'class': Value,
                    'properties': {
                        'name': 'energy'
                    }
                }
            }
        }
        
    def version(self):
        return version()
    
    def set(self, params):
        if len(params) < 2:
            raise ValueError("missing argument")
        name = params[0]
        if name not in SET_PARAMETERS.keys():
            raise ValueError(f"invalid argument: {name}")
        dic = self.table[name]
        if len(dic) > 1:
            if len(params) <= 1:
                raise ValueError("missing channel")
            if len(params) <= 2:
                raise ValueError("missing value")
            ch = params[1]
            if params[2] is not None:
                val = int(params[2])
            else:
                val = 0
        else:
            ch = None
            if params[1] is not None:
                val = int(params[1])
            else:
                val = 0
        if not ch in dic:
            raise ValueError(f"invalid channel: {ch}")
        low, high = SET_RANGES[name]
        if not low <= val <= high:
            raise ValueError(f"value out of range: {val}")
        cls = dic[ch]['class']
        props = dic[ch]['properties']
        obj = cls(self.sleepi4.registers, props)
        obj.write(val)
    
    def get(self, params):
        if len(params) < 1:
            raise ValueError("missing argument")
        name = params[0]
        if name not in GET_PARAMETERS.keys():
            raise ValueError(f"invalid argument: {name}")
        dic = self.table[name]
        if len(dic) > 1:
            if len(params) <= 1:
                if not None in dic:
                    raise ValueError("missing channel")
                ch = None
            else:
                ch = params[1]
        else:
            ch = None
        if not ch in dic:
            raise ValueError(f"invalid channel: {ch}")
        cls = dic[ch]['class']
        props = dic[ch]['properties']
        obj = cls(self.sleepi4.registers, props)
        return obj.read()
    
    def help(self, params=['all']):
        return help(params[0])



