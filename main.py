from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import markdown

app = FastAPI()

MAX_INPUT_LENGTH = 100000

class MarkdownRequest(BaseModel):
    text: str = Field(..., example="## Sample Markdown\nThis is *italic* and **bold**.")

@app.post("/convert")
def convert_markdown(request: MarkdownRequest):
    md_text = request.text.strip()

    # Edge Case: Empty or whitespace-only input
    if not md_text:
        raise HTTPException(
            status_code=400,
            detail="Markdown input is empty or only contains whitespace."
        )

    # Edge Case: Input too long
    if len(md_text) > MAX_INPUT_LENGTH:
        raise HTTPException(
            status_code=413,
            detail=f"Markdown input too large (>{MAX_INPUT_LENGTH} characters)."
        )

    try:
        html = markdown.markdown(md_text)
        return {
            "success": True,
            "html": html,
            "message": "Conversion successful."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while converting Markdown to HTML."
        )
