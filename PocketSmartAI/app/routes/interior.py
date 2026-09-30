import asyncio
import os

from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel
from google import genai

load_dotenv()

router = APIRouter(
    prefix="/api/interior",
    tags=["Interior AI"],
)


class InteriorRequest(BaseModel):
    room: str
    style: str
    budget: str
    size: str
    description: str


api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def fallback_plan(request: InteriorRequest):
    return {
        "success": True,
        "result": f"""
1. Color Palette

For your {request.room}, use soft neutral colours like white, beige,
light grey or cream. Add one accent colour based on the {request.style}
style.

2. Furniture

Choose compact and practical furniture suitable for a {request.size}
room. Keep enough walking space and avoid oversized furniture.

3. Lighting

Use one main ceiling light, warm bedside lights and natural daylight.
LED lights can help reduce electricity usage.

4. Storage

Use a wardrobe with vertical storage, wall shelves and under-bed
storage wherever possible.

5. Decoration

For a {request.style} look, keep decoration simple. Add a small rug,
curtains, wall art and a few indoor plants.

6. Budget Tips

Since your budget is {request.budget}, prioritize essential furniture
first. Buy decorative items later and compare prices before purchasing.

7. Complete Interior Plan

Create a practical {request.style} {request.room} suitable for a
{request.size} space.

Your requirement:
{request.description}

Start with the bed/sofa as the main furniture piece, then arrange
storage and lighting around it. Keep the room uncluttered and maintain
good movement space.
"""
    }


async def call_gemini(prompt: str):
    if not client:
        raise Exception("GEMINI_API_KEY is not configured.")

    response = await asyncio.to_thread(
        client.models.generate_content,
        model="gemini-3.8-flash",
        contents=prompt,
    )

    return response.text


@router.post("")
async def generate_interior(request: InteriorRequest):

    prompt = f"""
You are PocketSmartAI Interior Assistant.

Create a practical personalized interior design recommendation.

Room: {request.room}
Style: {request.style}
Budget: {request.budget}
Room Size: {request.size}
Requirement: {request.description}

Use exactly these headings:

1. Color Palette
2. Furniture
3. Lighting
4. Storage
5. Decoration
6. Budget Tips
7. Complete Interior Plan

Keep the answer practical, simple and suitable for the given budget
and room size.
"""

    try:
        result = await asyncio.wait_for(
            call_gemini(prompt),
            timeout=15
        )

        return {
            "success": True,
            "result": result
        }

    except asyncio.TimeoutError:
        return fallback_plan(request)

    except Exception:
        return fallback_plan(request)