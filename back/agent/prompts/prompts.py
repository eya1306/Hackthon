INTENT_RECOGNITION="""
You are an advanced AI assistant trained to recognize whether a given message is a "complaint" or "other."  
A "complaint" is a message expressing dissatisfaction or seeking resolution for an issue.  

Your task is to classify the message and return:  
- `True` if the message is a complaint.  
- `False` if the message is not a complaint.  

Here are some examples for clarity:  

1. User input: "I am unhappy with the service I received yesterday. Please fix this." --> True  

2. User input: "The delivery was late, and the item is damaged. I need a replacement." --> True  

3. User input: "Thank you for the amazing customer support!" --> False  

4. User input: "Can you provide more details about the warranty for this product?" --> False  

Now, classify the following message:  
user input: "{user_input}"  
"""

REPHRASE="""
You are an advanced AI assistant tasked with helping service handlers understand user complaints quickly and effectively.  
Your task is to analyze a complaint message and create a concise, professional summary that highlights the key issue(s) and any specific details.  
The summary should be actionable and easy for service handlers to understand without needing to refer to the original message.  

Here are some examples for clarity:  

1. Original Message: "My internet has been down for three days, and I couldn’t reach customer support after waiting on hold for an hour!" --> "The user is experiencing an internet outage lasting three days and has been unable to reach customer support after long wait times."  

2. Original Message: "I ordered a phone case, but you sent the wrong one. Also, the return process isn’t working on your website!" --> "The user received an incorrect phone case and is unable to process a return due to an issue with the website's return system."  

3. Original Message: "Why is my electricity bill so high this month? I haven’t changed my usage, and I think there’s an error in the calculation!" --> "The user is questioning an unusually high electricity bill and suspects a calculation error."  

4. Original Message: "The product broke after two uses, and when I called for a warranty claim, I was told it’s not covered!" --> "The user’s product broke after minimal use, and their warranty claim was denied."  

Now, summarize the following complaint for the service handler:  
User Input: "{user_input}"  
"""

CATEGORIZE=""" You are an advanced AI assistant responsible for categorizing user complaints into predefined labels to help service handlers prioritize and respond effectively.
Your task is to analyze the refined summary of a user’s complaint and their input, then assign the appropriate category label from the following:

Technique: For technical issues, such as system malfunctions, software bugs, or hardware defects.
Logistique: For shipping, delivery, inventory, or supply chain-related issues.
Commercial: For billing, payment, or customer service-related concerns.
Marketing: For questions or complaints related to promotions, advertisements, or branding.
Here are some examples for clarity:

Refined Summary: "The user is experiencing an internet outage lasting three days and has been unable to reach customer support after long wait times." -->  Technique

Refined Summary: "The user received an incorrect phone case and is unable to process a return due to an issue with the website's return system." -->  Logistique

Refined Summary: "The user is questioning an unusually high electricity bill and suspects a calculation error." -->  Commercial

Refined Summary: "The user wants more details about a promotional offer they saw online." -->  Marketing

Now, assign the appropriate category label:
Refined Summary: "{summary}"
User Input: "{user_input}"
"""