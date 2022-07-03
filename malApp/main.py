import configparser
from malApp.graph import Graph


def main():
    print('Python Graph Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Display access token')
        print('2. List my inbox')
        print('3. Send mail')
        print('4. List users (requires app-only)')
        print('5. Make a Graph call')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        if choice == 0:
            print('Goodbye...')
        elif choice == 1:
            display_access_token(graph)
        elif choice == 2:
            list_inbox(graph)
        elif choice == 3:
            send_mail(graph)
        elif choice == 4:
            list_users(graph)
        elif choice == 5:
            make_graph_call(graph)
        else:
            print('Invalid choice!\n')


def greet_user(graph: Graph):
    # TODO
    return


def display_access_token(graph: Graph):
    token = graph.get_user_token()
    print('User token:', token, '\n')


def list_inbox(graph: Graph):
    # TODO
    return


def send_mail(graph: Graph):
    # TODO®
    return


def list_users(graph: Graph):
    # TODO
    return


def make_graph_call(graph: Graph):
    # TODO
    return


# Run main
main()
