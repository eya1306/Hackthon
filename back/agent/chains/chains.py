from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables.base import RunnableSerializable
from ..prompts.prompts import INTENT_RECOGNITION, REPHRASE, CATEGORIZE

def intent_recognition_chain(llm : GoogleGenerativeAI):
    """
    Create an intent detection node using a language model (LLM).

    Args:
        llm (ChatLLM): The language model to be used in the chain.

    Returns:
        intent_recognition_chain : The configured intent chain.
    """
    # Define the chat prompt for the LLM chain
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", INTENT_RECOGNITION),
            ("human", "{user_input}")
        ]
    )
    # Set up the intent chain using the conversation prompt and language model
    intent_recognition_chain = prompt | llm 

    return intent_recognition_chain

def rephrase_chain(llm : GoogleGenerativeAI):
    """
    Create an rephrasing node using a language model (LLM).

    Args:
        llm (ChatLLM): The language model to be used in the chain.

    Returns:
        rephrase_chain : The configured intent chain.
    """
    # Define the chat prompt for the LLM chain
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", REPHRASE),
            ("human", "{user_input}")
        ]
    )
    # Set up the intent chain using the conversation prompt and language model
    rephrase_chain = prompt | llm

    return rephrase_chain

def categorize_chain(llm : GoogleGenerativeAI):
    """
    Create an intent detection node using a language model (LLM).

    Args:
        llm (ChatLLM): The language model to be used in the chain.

    Returns:
        intent_recognition_chain : The configured intent chain.
    """
    # Define the chat prompt for the LLM chain
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CATEGORIZE),
            ("ai", "{summary}"),
            ("human", "{user_input}")
        ]
    )
    # Set up the intent chain using the conversation prompt and language model
    categ_chain = prompt | llm 

    return categ_chain