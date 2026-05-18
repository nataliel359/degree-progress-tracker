from fastapi import APIRouter
from app.services.progress_service import generate_progress
from app.services.mock_data import create_mock_data

router = APIRouter()

@router.get("/progress")
def get_progress():
    student, main_degree, second_degree = create_mock_data()
    main_progress = generate_progress(student, main_degree)
    second_progress = generate_progress(student, second_degree)
    return {
        "student": student.name,
        "major": main_progress,
        "minor": second_progress
    }