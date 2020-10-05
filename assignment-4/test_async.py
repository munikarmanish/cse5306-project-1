# author: Hamza Reza Pavel, Manish Munikar

from client import AsyncRPC


def main():
    print("\nasync request for calculate_pi")
    pi_rpc = AsyncRPC("calculate_pi", args=[])
    pi_rpc.invoke()

    print("\nasync request for add(1, 2)")
    add_rpc = AsyncRPC("add", args=[1, 2])
    add_rpc.invoke()

    print("\nfetching results for calculate_pi")
    print(pi_rpc.get_result())

    print("\nfetching results for add(1, 2)")
    print(add_rpc.get_result())


if __name__ == "__main__":
    main()