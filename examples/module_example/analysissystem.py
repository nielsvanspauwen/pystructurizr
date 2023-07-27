from pystructurizr.dsl import Model
from .chatsystem import message_store
from .users import analyst

analytics = Model("Analytics")
gpt = analytics.SoftwareSystem("OpenAI GPT-4")
analysis_system = analytics.SoftwareSystem("Sentiment Analysis and Statistics System",
                                           "Provides insights to the business about support load, quality and customer sentiment, based on chat messages.")
sentiment_engine = analysis_system.Container("Sentiment Analysis Engine",
                                             "Analyzes the sentiment of customer messages.", 
                                             technology="GPT-4")
stats_compiler = analysis_system.Container("Statistics Compiler",
                                           "Analyzes the content of customer messages to identify the products/features most questioned about.", 
                                           technology="Python")
report_builder = analysis_system.Container("Report Builder",
                                           "Combines stats and sentiments into human readable reports", 
                                           technology="Python")

gpt_integration = sentiment_engine.Component(
    "GPT integration", "Anonymizes messages and uses the GPT-4 API to determine sentiment")
sentiment_store = sentiment_engine.Component(
    "Sentiment Store", "Stores sentiment for each conversation.", tags=["database"])
gpt_integration.uses(message_store, "Retrieve recent conversations")
gpt_integration.uses(
    gpt, "Sends/receives anonymized messages", technology="REST API")
gpt_integration.uses(sentiment_store, "Stores sentiment score")

topic_analyzer = stats_compiler.Component(
    "Topic Analyzer", "Determines which product and feature a conversation is about")
stats_compiler_comp = stats_compiler.Component(
    "Statistics Compiler", "Computes all kind of useful stats")
stats_store = stats_compiler.Component(
    "Stats Store", "Column-oriented database optimized for statistics", tags=["database"])
topic_analyzer.uses(message_store, "Retrieve recent conversations")
topic_analyzer.uses(stats_compiler_comp, "Notification")
stats_compiler_comp.uses(stats_store, "Stores data")

sentiment_engine.uses(message_store, "Retrieve recent conversations")
stats_compiler.uses(message_store, "Retrieve recent conversations")
report_builder.uses(stats_store, "Get data")
report_builder.uses(sentiment_store, "Get data")
analyst.uses(report_builder, "Analyze and report")
