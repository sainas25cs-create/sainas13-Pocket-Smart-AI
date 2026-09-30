import json
from io import BytesIO
from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.entities import Recommendation, User
from app.models.schemas import (
    InteriorPlanRequest,
    JewelryPlanRequest,
    PartyPlanRequest,
)
from app.security import get_current_user
from app.services.gemini import generate_recommendation


router = APIRouter(
    prefix="/api/planners",
    tags=["Planners"],
)


def save_history(
    db: Session,
    user: User,
    planner: str,
    input_data: dict[str, Any],
    result: dict[str, Any],
) -> None:

    recommendation = Recommendation(
        user_id=user.id,
        kind=planner,
        input_json=json.dumps(
            input_data,
            ensure_ascii=False,
        ),
        result_json=json.dumps(
            result,
            ensure_ascii=False,
        ),
    )

    db.add(recommendation)
    db.commit()


@router.post("/home")
def home_planner(
    data: InteriorPlanRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    input_data = data.model_dump()

    result = generate_recommendation(
        "interior",
        input_data,
    )

    save_history(
        db,
        user,
        "home",
        input_data,
        result,
    )

    return result


@router.post("/party")
def party_planner(
    data: PartyPlanRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    input_data = data.model_dump()

    result = generate_recommendation(
        "party",
        input_data,
    )

    save_history(
        db,
        user,
        "party",
        input_data,
        result,
    )

    return result


@router.post("/jewelry")
async def jewelry_planner(
    budget: float = Form(...),
    occasion: str = Form(...),
    jewelry_type: str = Form(...),
    metal: str = Form(...),
    style: str = Form(...),
    description: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # Build planner input
    input_data = {
        "budget": budget,
        "occasion": occasion,
        "jewelry_type": jewelry_type,
        "metal": metal,
        "style": style,
        "description": description,
        "outfit_image_uploaded": False,
    }


    # Optional image validation
    if outfit_image is not None:

        allowed_types = {
            "image/png",
            "image/jpeg",
            "image/webp",
        }

        if outfit_image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Only PNG, JPEG and WebP images are supported.",
            )

        raw_data = await outfit_image.read()

        if len(raw_data) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="Image must be smaller than 5 MB.",
            )

        try:
            Image.open(
                BytesIO(raw_data)
            ).convert("RGB")

        except UnidentifiedImageError:
            raise HTTPException(
                status_code=400,
                detail="Invalid image file.",
            )

        input_data["outfit_image_uploaded"] = True


    # Generate recommendation
    try:

        result = generate_recommendation(
            "jewelry",
            input_data,
        )

    except Exception as exc:

        # Always return JSON instead of an HTML 500 page
        return {
            "source": "fallback",
            "title": "Jewelry Recommendation",
            "summary": "Unable to connect to AI right now.",
            "suggestions": [
                "Choose jewelry according to your occasion.",
                "Compare prices before purchasing.",
                "Stay within your selected budget.",
            ],
            "budget_breakdown": {
                "Jewelry": budget
            },
            "tips": [
                "Check purity and certification.",
                "Compare making charges.",
                "Keep the final purchase within budget.",
            ],
            "marketplace_searches": [],
            "error": str(exc),
        }


    # Add image status
    if outfit_image is not None:

        result["image_analysis"] = (
            "Outfit image received successfully."
        )


    # Save history safely
    try:

        save_history(
            db=db,
            user=user,
            planner="jewelry",
            input_data=input_data,
            result=result,
        )

    except Exception:
        # Do not break the recommendation
        # if history saving fails.
        db.rollback()


    return result