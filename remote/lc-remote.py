import argparse

from remote.modules.lcremote import LcRemote


def setup_args():
    parser = argparse.ArgumentParser(description="The NAS-Control remote.")

    parser.add_argument()

    return parser


if __name__ == '__main__':
    #parser = setup_args()
    #args = parser.parse_args()
    server = LcRemote()
    server.run()
