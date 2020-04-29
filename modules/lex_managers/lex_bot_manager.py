import boto3
from prettytable import PrettyTable
import pprint


class LexBotManager:

    def __init__(self):

        self.client = boto3.client('lex-models')

    def create_new_bot(self, bot_name, locale="en-US", children_directed=False, intents=[]):

        bot_info = {'name': bot_name,
                    'locale': locale,
                    'childDirected': children_directed,
                    'abortStatement': {'messages': [
                                            {
                                                'contentType': 'PlainText',
                                                'content': 'Abort statement'
                                            }
                                        ]
                                       }
                    }

        try:
            existing_bot = self.client.get_bot(name=bot_name, versionOrAlias="$LATEST")
            bot_info['checksum'] = existing_bot["checksum"]
        except self.client.exceptions.NotFoundException:
            pass

        intent_info = []

        for intent in intents:

            intent_info.append({'intentName': intent,
                                'intentVersion': '$LATEST'})

        bot_info['intents'] = intent_info
        response = self.client.put_bot(**bot_info)
        pprint.pprint(response)
        print("Successfully create bot {}".format(bot_name))

    def get_bots_list(self):

        response = self.client.get_bots()

        bots_list = []

        for bot in response['bots']:

            bots_list.extend(bot['name'])

        return bots_list

    def print_bots(self):

        response = self.client.get_bots()

        table = PrettyTable()
        table.field_names = ['bot_name', 'status', 'description', 'version']

        for bot in response['bots']:
            try:
                table.add_row([bot['name'], bot['status'], bot['description'], bot['version']])
            except KeyError:
                table.add_row([bot['name'], bot['status'], "n/a", bot['version']])

        print(table)