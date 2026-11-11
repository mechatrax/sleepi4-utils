#!/usr/bin/env python3

import sys
from importlib import machinery, util
from pathlib import Path

import sleepi


path = Path('/usr/share/sleepi4-utils/sleepi4_util.py')

loader = machinery.SourceFileLoader(str(path), str(path))
spec = util.spec_from_file_location(str(path), path, loader=loader)
sleepi4_util = util.module_from_spec(spec)
spec.loader.exec_module(sleepi4_util)


ENVIRONMENT_FILE = '/etc/default/sleepi4'


def start(cli, env):
    cli.set(['extin-trigger', '1', '0'])
    cli.set(['extin-trigger', '2', '0'])
    cli.set(['ri-trigger', '0'])
    cli.set(['extin-powerdown', '1', env['EXTIN1_FORCED_SHUTDOWN']])
    cli.set(['extin-powerdown', '2', env['EXTIN2_FORCED_SHUTDOWN']])
    cli.set(['watchdog-timeout', env['HEARTBEAT_TIMEOUT']])
    cli.set(['watchdog-boot-timeout', env['BOOT_TIMEOUT']])
    cli.set(['restart', '1'])
    cli.set(['restore-voltage', '1', '0'])
    cli.set(['restore-voltage', '2', '0'])
    cli.set(['uvlo', '1', '0'])
    cli.set(['uvlo', '2', '0'])
    

def stop(cli, env):
    if int(env['RETRY_BOOT']) != 0:
        cli.set(['restart', '1'])
    else:
        cli.set(['restart', '0'])
    cli.set(['sleep-timeout', env['POWEROFF_DELAY']])
    cli.set(['watchdog-boot-timeout', env['BOOT_TIMEOUT']])
   
 
def halt(cli, env):
    if int(env['RETRY_BOOT']) != 0:
        cli.set(['restart', '1'])
    else:
        cli.set(['restart', '0'])
    cli.set(['sleep-timeout', '0'])
    cli.set(['watchdog-timeout', '0'])
    cli.set(['watchdog-boot-timeout', '0'])
    

def restart(cli, env):
    if int(env['RETRY_BOOT']) != 0:
        cli.set(['restart', '1'])
    else:
        cli.set(['restart', '0'])
    cli.set(['sleep-timeout', '0'])
    cli.set(['watchdog-timeout', env['BOOT_TIMEOUT']])
    

def main(env_file=ENVIRONMENT_FILE):
    arg = sys.argv[1]
    env = sleepi4_util.parse_environment(env_file)
    bus = int(env['I2C_BUS'])
    addr = int(env['I2C_ADDRESS'], 16)
    cli = sleepi4_util.Sleepi4Cli(sleepi.Sleepi4(bus, addr))
    
    if arg == 'start':
        start(cli, env)
    elif arg == 'stop':
        stop(cli, env)
    elif arg == 'halt':
        halt(cli, env)
    elif arg == 'restart':
        restart(cli, env)


if __name__ == '__main__':
    main()
