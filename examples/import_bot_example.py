from modules import LexBotImporter

# create the importer object
importer = LexBotImporter()

# import bot by providing json encoding
importer.import_bot("../assets/HowAreYouBot.json")