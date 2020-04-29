import boto3
from prettytable import PrettyTable


class LexIntentManager:

    def __init__(self):

        self.client = boto3.client('lex-models')

    def create_new_intent(self, intent_name, description="n/a", sample_utterances=[], slot_types=[]):

        intent_info = {'name': intent_name,
                       'description': description,
                       'sampleUtterances': sample_utterances,
                       'fulfillmentActivity': {'type':'ReturnIntent'}}

        try:
            response = self.client.get_slot_type(name=intent_name, version='$LATEST')
            intent_info['checksum'] = response['checksum']
        except self.client.exceptions.NotFoundException:
            pass

        slots_info = self._slot_type_constructor(slot_types)
        intent_info['slots'] = slots_info
        self.client.put_intent(**intent_info)

        print("Successfully created intent {}".format(intent_name))

    def get_intent_list(self):

        response = self.client.get_intents()

        intent_list = []

        for intent in response['intents']:

            intent_list.append(intent['name'])

    def print_intents(self):

        response = self.client.get_intents()

        table = PrettyTable()
        table.field_names = ['intent_name', 'description', 'version']

        for intent in response['intents']:
            try:
                table.add_row([intent['name'], intent['description'], intent['version']])
            except KeyError:
                table.add_row([intent['name'], "n/a", intent['version']])

        print(table)

    @staticmethod
    def _slot_type_constructor(slot_types):

        slots_info = []

        for slot_type in slot_types:
            slot_name = "sample_" + slot_type
            slot_required = input("Will the slot {} be required [Required / Optional]: ".format(slot_type))
            slot_version = '$LATEST'
            slot_prompt = str(input("Provide an elicitation prompt for slot {}: ".format(slot_type)))
            slot_max_attempts = int(input("What is the max attempts to allow when filling slot {}: ".format(slot_type)))
            slot_sample_utterances = []
            while True:
                slot_sample_utterances.append(
                    str(input("Please enter a sample utterance for slot {}: ".format(slot_type))).replace("this",
                                                                                                          "{" + slot_name + "}"))
                if input("Would you like to add another utterance [True / False]: ") == "False":
                    break

            print("{} - req: {} - prompt: {} - max_attempt: {} - sampleUtterances {}".format(slot_type, slot_required,
                                                                                             slot_prompt,
                                                                                             slot_max_attempts,
                                                                                             slot_sample_utterances))
            slot_info = {'name': slot_name,
                         'slotConstraint': slot_required,
                         'slotType': slot_type,
                         'slotTypeVersion': slot_version,
                         'valueElicitationPrompt': {
                             'messages': [
                                 {
                                     'contentType': 'PlainText',
                                     'content': slot_prompt,
                                 },
                             ],
                             'maxAttempts': slot_max_attempts,
                         },
                         'sampleUtterances': slot_sample_utterances
                         }
            slots_info.append(slot_info)

        return slots_info

