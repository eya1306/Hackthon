from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from langchain_core.messages import HumanMessage
from agent.graph import graph



app = FastAPI(title="yidek")

@app.post("/ainvoke")
def graph_stream(user_input):
        # Process the query using graph.astream
    user_input_message = HumanMessage(content=user_input)


    for event in graph.stream(
            {"messages": [user_input_message], "user_id":"testid","message_id":"12","message_text":user_input, "summary_text":""},
            stream_mode="values",
        ):
        print(f"Processed event: {event}")
            
    return event




# To run the app, use: uvicorn app.main:app --reload
