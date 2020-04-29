README
======

A wrapper for AWS Lex that allows you to create, import, and run bot from a python interface.

Overview
--------

A Lex Bot has three major components
- `Bot` is the main component that carries out the conversation.
- `Intent` represents an action that the user wants to perform. You create a bot to support one or more related intents. For example, you might create a bot that asks you how you feel.
- `Slot` is where information collected from the information is stored. Each slot has a type that presents constraints on the value that can be filled. 

Setup
----------

1. Clone this repository into your desired directory.

       git clone git@github.com:adamhamden/lex-bot.git

1. Ensure installation of required packages

       python3 -m pip install -r requirements.txt
       
Examples
---------
Note: The examples assume you have the AWS credentials set up. If not already done go here https://docs.aws.amazon.com/lex/latest/dg/getting-started.html

- There are a few examples to guide you through importing a bot, creating you own, or running an existing bot. The assets folder contains a json encoding of a fully-functional bot for reference.

- Start with `import_bot_example.py` which will guide you through the process of uploading the json file `HowAreYouBot.json` into AWS
- You can then run the bot using the `play_bot_example.py`

- Once you are comfortable with the interface, use the `create_bot_example.py` to create a bot from scratch with custom intents and slots