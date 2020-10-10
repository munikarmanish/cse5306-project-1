# author: Hamza Reza Pavel, Manish Munikar

import time

from client import AsyncRPC


def main():
    print("async request for calculate_pi")
    pi_rpc = AsyncRPC("calculate_pi", args=[])
    pi_rpc.invoke()

    print("async request for add(1, 2)")
    add_rpc = AsyncRPC("add", args=[1, 2])
    add_rpc.invoke()

    print("\ndoing sth else...\n")
    time.sleep(1)

    print("fetching results for calculate_pi = {}".format(pi_rpc.get_result()))
    print("fetching results for add(1, 2) = {}".format(add_rpc.get_result()))


if __name__ == "__main__":
    main()
