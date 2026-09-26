import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from router import route_and_execute

app = FastAPI(title="Nexus Gateway")

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        data = await request.json()
        messages = data.get("messages", [])
        model = data.get("model", None)

        response = await route_and_execute(messages, req_model=model)
        
        # Returns 400 status if a guardrail violation was caught
        if "error" in response and response["error"].get("type") == "guardrail_violation":
            return JSONResponse(status_code=400, content=response)

        return JSONResponse(content=response)
    
    except Exception as e:
        print("\n" + "="*50)
        print("INTERNAL GATEWAY ERROR DETECTED:")
        traceback.print_exc()
        print("="*50 + "\n")
        
        return JSONResponse(
            status_code=500,
            content={"error": {"message": str(e), "type": "internal_server_error"}}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)