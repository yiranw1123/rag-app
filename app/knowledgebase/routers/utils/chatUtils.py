import json

async def format_chat_history(history):
    formatted_messages = []
    for message_str in history:
        # Assuming each message is a JSON string; parse it
        message = json.loads(message_str)
        
        # Determine the sender based on the type of the message
        sender = "assistant" if message.get("type") == "ai" else "me"
        
        # Extract the content of the message
        content = message.get("data", {}).get("content", "")
        
        # Append formatted message to the list
        formatted_messages.append({"sender": sender, "text": content})

    return list(reversed(formatted_messages))