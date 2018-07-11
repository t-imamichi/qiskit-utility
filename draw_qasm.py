#!/usr/bin/env python
# coding: utf-8

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

'''
Draw a QASM circuit based on matplotlib_circuit_drawer.
Requires qiskit-terra 0.5.5 or later.

Examples:
  $ python draw_qasm.py -i tmp.qasm -o tmp.pdf  # default style
  $ python draw_qasm.py -i tmp.qasm -o tmp.pdf --style composer.json  # QX composer style
'''

import json
from argparse import ArgumentParser

import matplotlib

matplotlib.use('module://ipykernel.pylab.backend_inline')  # workaround to avoid redundant draw path
from qiskit.tools.visualization._circuit_visualization import MatplotlibDrawer


def options():
    parser = ArgumentParser()
    parser.add_argument('-i', '--qasm', action='store', help='input QASM file')
    parser.add_argument('-s', '--style', action='store', help='style file')
    parser.add_argument('--scale', action='store', help='scaling factor', type=float, default=0.7)
    parser.add_argument('-o', '--out', action='store', help='output figure file (pdf, png or svg)')
    parser.add_argument('-j', '--json', action='store', help='output JSON file of AST')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
    args = parser.parse_args()
    if args.verbose:
        print('options:', args)
    if not args.qasm:
        parser.print_usage()
    return args


def main():
    args = options()
    if not args.qasm:
        return
    drawer = MatplotlibDrawer(style=args.style, scale=args.scale)
    drawer.load_qasm_file(args.qasm)
    # output json
    if args.json:
        with open(args.json, 'w') as outfile:
            json.dump(drawer.ast, outfile, sort_keys=True, indent=2)
    # draw quantum circuit
    drawer.draw(args.out)


if __name__ == '__main__':
    main()
