import boto3
import pprint
import json
import os


class LexBotImporter:

    def __init__(self):

        self.client = boto3.client('lex-models')

    def import_bot(self, bot_file=None, file_path=None):

        bot_data = self._parse_bot_file(bot_file, file_path)

        self._construct_bot(bot_data)

    @staticmethod
    def _parse_bot_file(bot_file=None, file_path=None):

        if bot_file is None:
            raise RuntimeError("ERROR: No bot file was provided")
            return

        if file_path is None:
            file_path = os.path.dirname(os.path.abspath(__file__))
            print("No filepath provided, using current file path")

        filename = os.path.join(file_path, bot_file)

        try:
            with open(filename) as f:
                bot_data = json.load(f)
        except FileNotFoundError:
            print("ERROR: Bot file was not found")
            return

        print("Successfully parsed {}".format(bot_file))

        return bot_data

    def _construct_bot(self, bot_data):

        self._import_slot_types(bot_data)
        self._import_intents(bot_data)
        self._import_bot_configurations(bot_data)

    def _import_slot_types(self, bot_data):

        for slot in bot_data['resource']['slotTypes']:

            del slot['version']

            # check if slot exists
            try:
                response = self.client.get_slot_type(name=slot['name'], version='$LATEST')
                slot['checksum'] = response['checksum']
            except self.client.exceptions.NotFoundException:
                pass

            self.client.put_slot_type(**slot)
            print("Successfully imported slot type {}".format(slot['name']))

    def _import_intents(self, bot_data):

        for intent in bot_data['resource']['intents']:

            del intent['version']

            # check if intent exists
            try:
                response = self.client.get_intent(name=intent['name'], version='$LATEST')
                intent['checksum'] = response['checksum']
            except self.client.exceptions.NotFoundException:
                pass

            self.client.put_intent(**intent)
            print("Successfully imported intent {}".format(intent['name']))

    def _import_bot_configurations(self, bot_data):

        bot = bot_data['resource']

        del bot['version']
        del bot['slotTypes']

        # check if bot exists
        try:
            response = self.client.get_bot(name=bot['name'], versionOrAlias='$LATEST')
            bot['checksum'] = response['checksum']
        except self.client.exceptions.NotFoundException:
            pass

        intent_list = []

        for intent in bot_data['resource']['intents']:

            intent_list.append({'intentName': intent['name'], 'intentVersion':'$LATEST'})

        bot['intents'] = intent_list
        response = self.client.put_bot(**bot)
        print("Successfully imported bot {}".format(bot['name']))

        pprint.pprint(response)



