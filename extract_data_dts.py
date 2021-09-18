#!/usr/bin/env python3

import argparse
import struct


def parse_args():
    parser = argparse.ArgumentParser(
        description='Extract data files from DTS FIT image')
    parser.add_argument('dts', type=str,
                        help='DST input file')
    return parser.parse_args()


def main():
    args = parse_args()
    description = None
    with open(args.dts) as f:
        for line in f:
            if 'description' in line:
                description = line.split('=')[-1].strip()
                description = description.replace(';', '').replace('"', '')
            if 'data' in line:
                data = line.strip()
                data = data[len('data = '):]
                data_type = data[0]
                data = data[1:-2]
                if data_type == '[':
                    data = bytes.fromhex(data.replace(' ', ''))
                elif data_type == '<':
                    data = bytes().join(
                        [struct.pack('>I', int(a, 16)) for a in data.split()])
                else:
                    raise ValueError(f'unknown data type {data_type}')
                print('Writing', description)
                with open(description, 'wb') as data_f:
                    data_f.write(data)


if __name__ == '__main__':
    main()
