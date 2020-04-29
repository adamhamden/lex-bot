import boto3
import uuid
import pprint


class LexBotPlayer:

    def __init__(self):

        self.model_client = boto3.client('lex-models')
        self.runtime_client = boto3.client('lex-runtime')

    def start_bot(self, bot_name, bot_alias):

        self._create_bot_alias(bot_name, bot_alias)
        user_id = self._create_new_session(bot_name, bot_alias)
        self.post_text(bot_name, bot_alias, user_id, input(">>> "))

    def post_text(self, bot_name, bot_alias, user_id, message):

        if not self._bot_exists(bot_name):
            print("ERROR: The bot {} does not exist".format(bot_name))
            return

        aliases = self._get_bot_aliases(bot_name)

        if bot_alias not in aliases:
            print("ERROR: The alias {} does not exist".format(bot_alias))
            return

        post_info = {'botName': bot_name,
                     'botAlias': bot_alias,
                     'userId': user_id,
                     'inputText': message}

        response = self.runtime_client.post_text(**post_info)

        if response['dialogState'] == "ElicitSlot":

            print(response['message'])
            user_response = str(input(">>> "))
            self.post_text(bot_name, bot_alias, user_id, user_response)

        elif response['dialogState'] == "ReadyForFulfillment":

            session_info = {'botName': bot_name,
                            'botAlias': bot_alias,
                            'userId': user_id}
            session_response = self.runtime_client.get_session(**session_info)
            pprint.pprint(session_response)

    def _bot_exists(self, bot_name, version='$LATEST'):

        try:
            self.model_client.get_bot(name=bot_name, versionOrAlias=version)
            bot_exists = True
        except self.model_client.exceptions.NotFoundException:
            bot_exists = False

        return bot_exists

    def _get_bot_aliases(self, bot_name):

        if not self._bot_exists(bot_name):
            print("ERROR: The bot {} does not exist".format(bot_name))
            return

        response = self.model_client.get_bot_aliases(botName=bot_name)

        alias_list = []

        for alias in response['BotAliases']:
            alias_list.append(alias['name'])

        return alias_list

    def _create_bot_alias(self, bot_name, alias_name, version='$LATEST'):

        alias_info = {'name': alias_name,
                      'botName': bot_name,
                      'botVersion': version}

        # check if alias exists
        try:
            response = self.model_client.get_bot_alias(name=alias_name, botName=bot_name)
            alias_info['checksum'] = response['checksum']
        except self.model_client.exceptions.NotFoundException:
            pass

        self.model_client.put_bot_alias(**alias_info)

    def _create_new_session(self, bot_name, bot_alias, user_id=None):

        if not self._bot_exists(bot_name):
            print("ERROR: The bot {} does not exist".format(bot_name))
            return

        if not user_id:
            user_id = str(uuid.uuid4())

        aliases = self._get_bot_aliases(bot_name)

        if bot_alias not in aliases:
            print("ERROR: The alias {} does not exist".format(bot_alias))
            return

        session_info = {'botName': bot_name,
                        'botAlias': bot_alias,
                        'userId': user_id}

        response = self.runtime_client.put_session(**session_info)

        print("Successfully created session. sessionID: {}, userId: {}".format(response['sessionId'], user_id))

        return user_id


