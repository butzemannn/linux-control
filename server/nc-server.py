#!/usr/bin/env python3

import argparse

def setup_args():
    parser = argparse.ArgumentParser(description="The NAS-Control server.")

    parser.add_argument()

    return parser


if __name__ == '__main__':
    parser = setup_args()
    args = parser.parse_args()