from modules import LexSlotManager
from modules import LexIntentManager
from modules import LexBotManager

# create slot manager
slot_manager = LexSlotManager()

# print existing slots for reference
slot_manager.print_slots()

# create a new slot
slot_manager.create_new_synonym_slot("salty_spicy",
                                     values_list=[
                                      {'value': 'salty', 'synonyms': ['salted', 'saline']},
                                      {'value': 'spicy', 'synonyms': ['hot', 'flaming']}
                                     ])

# print slots to see new slots added
slot_manager.print_slots()

# create intent manager
intent_manager = LexIntentManager()

# print existing slots
intent_manager.print_intents()

# create new intent with existing slots
intent_manager.create_new_intent("TasteIt",
                                 description="n/a",
                                 sample_utterances=["I just ate", "I had lunch"],
                                 slot_types=["salty_spicy"])

# print intents to see new intents added
intent_manager.print_intents()

# create bot manager
bot_manager = LexBotManager()

# print existing bots
bot_manager.print_bots()

# create new bot with existing intents
bot_manager.create_new_bot('tasting_bot', intents=['TasteIt'])

# print bots to see new bot added and build status
bot_manager.print_bots()




