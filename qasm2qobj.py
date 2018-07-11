#!/usr/bin/env python
# coding: utf-8

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

'''
Translate a QASM file to a QOBJ file.

Examples:
  $ python qasm2qobj.py -i input.qasm -o output.qobj  # mapping for all-to-all
  $ python qasm2qobj.py -i input.qasm -o output.qobj -b ibmq_5_tenerife  # mapping for ibmq_5_tenerife
'''

import json
from qiskit import register, available_backends, load_qasm_file, compile
from argparse import ArgumentParser
import numpy as np

import Qconfig


def backends(qconsole=False):
    key = 'qconsole' if qconsole else 'qx'
    token = Qconfig.APItoken[key]
    config = Qconfig.config[key]
    url = config.get('url', None)
    hub = config.get('hub', None)
    group = config.get('group', None)
    project = config.get('project', None)
    register(token, url, hub, group, project)
    return available_backends()


def options():
    parser = ArgumentParser()
    parser.add_argument('-i', '--qasm', action='store', help='input QASM file')
    parser.add_argument('-o', '--qobj', action='store', help='output QOBJ file')
    parser.add_argument('--out-qasm', action='store', help='output QASM file')
    parser.add_argument('-b', '--backend', action='store', help='backend (default: local_qasm_simulator)',
                        default='local_qasm_simulator')
    parser.add_argument('-z', '--qconsole', action='store_true', help='Use qconsole')
    args = parser.parse_args()
    print('options:', args)
    if not args.qasm or not args.qobj:
        parser.print_help()
        quit()
    set_backends = backends(args.qconsole)
    print('backends:', set_backends)
    if args.backend not in set_backends:
        print('invalid backend: {}'.format(args.backend))
        print('available backends: {}'.format(set_backends))
        #quit()
    return args


def support_npint(val):
    if isinstance(val, (np.int32, np.int64)):
        return int(val)
    return val


def main():
    args = options()
    circuit = load_qasm_file(args.qasm, name=args.qasm)
    qobj = compile(circuit, backend=args.backend)
    with open(args.qobj, 'w') as outfile:
        json.dump(qobj, outfile, indent=2, sort_keys=True, default=support_npint)
    if args.out_qasm:
        with open(args.out_qasm, 'w') as outfile:
            outfile.write(qobj['circuits'][0]['compiled_circuit_qasm'])


if __name__ == '__main__':
    main()
