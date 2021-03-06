#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012, 2013, 2014, 2017 SMHI
#
# Author(s):
#
#   Martin Raspaud <martin.raspaud@smhi.se>
#   Janne Kotro <janne.kotro@fmi.fi>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Receiver for 2met messages, through zeromq.

Outputs messages with the following metadata:
satellite, format, start_time, end_time, filename, uri, type, orbit_number, [instrument, number]

"""
import logging
from pytroll_collectors.scisys import receive_from_zmq

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="GMC host")
    parser.add_argument("port", help="Port to listen to", type=int)
    parser.add_argument("-s", "--station", help="Name of the station",
                        default="unknown")
    parser.add_argument("-x", "--excluded_satellites", nargs='*',
                        help="List of platform names to exclude",
                        default=[])
    parser.add_argument("-e", "--environment",
                        help="Name of the environment (e.g. dev, test, oper)",
                        default="dev")
    parser.add_argument("-l", "--log", help="File to log to", default=None)
    parser.add_argument("-f", "--ftp_prefix", dest="ftp_prefix",
                        type=str,
                        help="FTP path prefix for message uri")
    parser.add_argument("-t", "--target_server", dest="target_server",
                        type=str,
                        help="Name of the target server. "
                        "In case of multiple dispatches in GMC.")
    parser.add_argument("-T", "--topic_postfix",
                        dest="topic_postfix",
                        type=str,
                        help="Publish topic postfix. "
                             "Prefix will be /format/data_processing_level/")

    opts = parser.parse_args()
    no_sats = opts.excluded_satellites

    if opts.log:
        import logging.handlers
        handler = logging.handlers.TimedRotatingFileHandler(opts.log,
                                                            "midnight",
                                                            backupCount=7)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(logging.Formatter("[%(levelname)s: %(asctime)s :"
                                           " %(name)s] %(message)s",
                                           '%Y-%m-%d %H:%M:%S'))
    handler.setLevel(logging.DEBUG)
    logging.getLogger('').setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(handler)
    logging.getLogger("posttroll").setLevel(logging.INFO)
    logger = logging.getLogger("receiver")

    try:
        receive_from_zmq(opts.host, opts.port,
                         opts.station, opts.environment, no_sats,
                         opts.target_server, opts.ftp_prefix,
                         opts.topic_postfix, 1)
    except KeyboardInterrupt:
        pass
    except:
        logger.exception("Something wrong happened...")
    finally:
        print("Thank you for using pytroll/receiver."
              " See you soon on pytroll.org!")
