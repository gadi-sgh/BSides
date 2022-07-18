import configparser
from malApp.graph import Graph


def main():
    print('Python Graph Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    print("here")
    #greet_user(graph)
    print("here2")

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Display access token')
        print('2. List apps')
        print('3. find app')
        print('4. start app')
        print('5. stop app')
        print('6. List users (requires app-only)')


        try:
            choice = int(input())
        except ValueError:
            choice = -1

        if choice == 0:
            print('Goodbye...')
        elif choice == 1:
            display_access_token(graph)
        elif choice == 2:
            list_servicePrincipals(graph)
        elif choice == 3:
            find_app(graph)
        elif choice == 4:
            start_app(graph)
        elif choice == 5:
            stop_app(graph)
        elif choice == 6:
            list_users(graph)
        else:
            print('Invalid choice!\n')


def greet_user(graph: Graph):
    user = graph.get_user()
    print('Hello,', user['displayName'])
    # For Work/school accounts, email is in mail property
    # Personal accounts, email is in userPrincipalName
    print('Email:', user['mail'] or user['userPrincipalName'], '\n')


def display_access_token(graph: Graph):
    token = graph.get_user_token()
    print('User token:', token, '\n')


def list_inbox(graph: Graph):
    message_page = graph.get_inbox()

    # Output each message's details
    print(message_page)
    for message in message_page['value']:
        print('Message:', message['subject'])
        print('  From:', message['from']['emailAddress']['name'])
        print('  Status:', 'Read' if message['isRead'] else 'Unread')
        print('  Received:', message['receivedDateTime'])

    # If @odata.nextLink is present
    more_available = '@odata.nextLink' in message_page
    print('\nMore messages available?', more_available, '\n')



def list_users(graph: Graph):
    users_page = graph.get_users()

    # Output each users's details
    for user in users_page['value']:
        print('User:', user['displayName'])
        print('  ID:', user['id'])
        print('  Email:', user['mail'])

    # If @odata.nextLink is present
    more_available = '@odata.nextLink' in users_page
    print('\nMore users available?', more_available, '\n')


def list_apps(graph: Graph):
    list_api = graph.get_apps()
    print(list_api)

def list_servicePrincipals(graph: Graph):
    list = graph.get_servicePrincipals()
    print(list)

def find_app(graph: Graph):
    list_api = graph.get_app()
    print(list_api)

def start_app(graph: Graph):
    token = graph.get_user_token()
    return_msg = graph.enable_app(True,token)
    print(return_msg)

def stop_app(graph: Graph):
    token = graph.get_user_token()
    return_msg = graph.enable_app(False,token)
    print(return_msg)

# Run main
main()
