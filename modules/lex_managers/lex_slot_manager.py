import boto3
from prettytable import PrettyTable


class LexSlotManager:

    def __init__(self):

        self.client = boto3.client('lex-models')

    def create_new_synonym_slot(self, slot_name, description="n/a", values_list=[], strategy="ORIGINAL_VALUE"):

        slot_info = {'name': slot_name,
                     'description': description,
                     'enumerationValues': values_list,
                     'valueSelectionStrategy': strategy}

        try:
            response = self.client.get_slot_type(name=slot_name, version='$LATEST')
            slot_info['checksum'] = response['checksum']
        except self.client.exceptions.NotFoundException:
            pass

        self.client.put_slot_type(**slot_info)

        print("Successfully created slot {}".format(slot_name))

    def create_new_word_slot(self, slot_name, description="n/a", values_list=[], strategy="ORIGINAL_VALUE"):

        slot_info = {'name': slot_name,
                     'description': description,
                     'enumerationValues': values_list,
                     'valueSelectionStrategy': strategy}

        try:
            response = self.client.get_slot_type(name=slot_name, version='$LATEST')
            slot_info['checksum'] = response['checksum']
        except self.client.exceptions.NotFoundException:
            pass

        self.client.put_slot_type(**slot_info)

        print("Successfully created slot {}".format(slot_name))

    def get_slots_list(self):

        response = self.client.get_slot_types()

        slots_list = []

        for slot in response['slotTypes']:

            slots_list.extend(slot['name'])

    def print_slots(self):

        response = self.client.get_slot_types()

        table = PrettyTable()
        table.field_names = ['slot_name', 'description', 'version']

        for bot in response['slotTypes']:
            try:
                table.add_row([bot['name'], bot['description'], bot['version']])
            except KeyError:
                table.add_row([bot['name'], "n/a", bot['version']])

        print(table)



