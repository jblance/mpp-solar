#!/usr/bin/python

import logging
logger = logging.getLogger()

import mppcommands

 

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description='MPP Solar Command Utility')
    parser.add_argument('command', help='Command to run')
    parser.add_argument('-ll', '--loglevel',
        type=str,
        choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
        help='Set the logging level')
    parser.add_argument('-d', '--device', type=str, help='Serial device to communicate with', default='/dev/ttyUSB0')
    parser.add_argument('-b', '--baud', type=int, help='Baud rate for serial communications', default=2400)
    parser.add_argument('-l', '--listknown', action='store_true', help='List known commands')
    parser.add_argument('-H', '--makepretty', action='store_true', help='Display result with descriptions etc if possible')
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    

    logging.debug('command %s', args.command)
    logging.debug('Serial device used: %s, baud rate: %d', args.device, args.baud)

    mp = mppcommands.mppCommands(args.device, args.baud)
    
    if(args.listknown):
        for line in mp.getKnownCommands():
            print line
    else:
        # TODO: check if command is valid
        # maybe check if query or setter and ...
        if(args.makepretty):
            for line in mp.getResponsePretty(args.command):
                print line
        else:
            print mp.getResponse(args.command)

    
