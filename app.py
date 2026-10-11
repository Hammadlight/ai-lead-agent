from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from agent import process_lead

app = FastAPI(
    title="AI Lead Agent",
    version="1.0.0",
    description="AI-powered CRM Lead Qualification Agent"
)


class Lead(BaseModel):
    name: str
    email: EmailStr
    company: str
    employees: int | None = None
    budget: float | None = None
    message: str


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "AI Lead Agent"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/lead")
async def receive_lead(lead: Lead):
    """
    Receives a lead from a website form.
    Sends it to the AI Agent.
    """

    try:
        result = process_lead(lead.model_dump())

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )