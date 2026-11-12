"""Seed the course catalog and degree requirements from the mock curriculum.

Run from the backend directory with ``python -m scripts.seed_curriculum``.
"""

import re
import sys
from typing import Any, Dict, List, Tuple

from app.services.mock_data import create_mock_data


CATEGORY_ATTRIBUTES = {
    "required": "required_courses",
    "gen_ed": "gen_ed_courses",
    "science_breadth": "science_breadth_courses",
    "electives": "elective_courses",
}


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def build_curriculum_documents() -> Tuple[
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    List[str],
]:
    """Convert the mock programs into validated MongoDB document payloads."""
    _, *programs = create_mock_data()
    courses_by_code: Dict[str, Dict[str, Any]] = {}
    program_documents: List[Dict[str, Any]] = []
    requirement_documents: List[Dict[str, Any]] = []
    validation_errors: List[str] = []

    if not programs:
        validation_errors.append("No degree programs were found in mock_data.")

    for program in programs:
        program_name = getattr(program, "name", None)
        if not isinstance(program_name, str) or not program_name.strip():
            validation_errors.append("A degree program has a missing or invalid name.")
            continue

        normalized_name = program_name.strip()
        if normalized_name.lower().endswith("minor"):
            program_type = "minor"
        elif normalized_name.lower().endswith("major"):
            program_type = "major"
        else:
            validation_errors.append(
                f"{program_name!r} does not identify a supported major or minor."
            )
            continue

        program_id = _slugify(normalized_name)
        if not program_id:
            validation_errors.append(
                f"Could not create a stable program_id for {normalized_name!r}."
            )
            continue

        program_documents.append(
            {
                "program_id": program_id,
                "name": normalized_name,
                "program_type": program_type,
            }
        )

        for category, attribute in CATEGORY_ATTRIBUTES.items():
            category_courses = getattr(program, attribute, None)
            if not isinstance(category_courses, (set, list, tuple)):
                validation_errors.append(
                    f"{normalized_name}: category {category!r} is missing "
                    "or is not a course collection."
                )
                continue

            for course in category_courses:
                code = getattr(course, "code", None)
                name = getattr(course, "name", None)
                credits = getattr(course, "credits", None)
                if not isinstance(code, str) or not code.strip():
                    validation_errors.append(
                        f"{program_name}: a {category} course has an invalid code."
                    )
                    continue
                if not isinstance(name, str) or not name.strip():
                    validation_errors.append(
                        f"{program_name}: course {code!r} has an invalid name."
                    )
                    continue
                if isinstance(credits, bool) or not isinstance(credits, int) or credits <= 0:
                    validation_errors.append(
                        f"{program_name}: course {code!r} has invalid credits "
                        f"{credits!r}."
                    )
                    continue

                course_document = {
                    "course_id": code,
                    "code": code,
                    "name": name,
                    "credits": credits,
                }
                previous = courses_by_code.get(code)
                if previous is not None and previous != course_document:
                    validation_errors.append(
                        f"Course code {code!r} has conflicting definitions."
                    )
                else:
                    courses_by_code[code] = course_document

                requirement_documents.append(
                    {
                        "program_id": program_id,
                        "requirement_id": (
                            f"{program_id}-{category}-{_slugify(code)}"
                        ),
                        "course_code": code,
                        "category": category,
                    }
                )

    program_ids = [document["program_id"] for document in program_documents]
    if len(program_ids) != len(set(program_ids)):
        validation_errors.append("Program names produce duplicate program_id values.")

    requirement_ids = [
        (document["program_id"], document["requirement_id"])
        for document in requirement_documents
    ]
    if len(requirement_ids) != len(set(requirement_ids)):
        validation_errors.append(
            "The curriculum contains duplicate requirement identifiers."
        )

    return (
        sorted(courses_by_code.values(), key=lambda document: document["course_id"]),
        sorted(program_documents, key=lambda document: document["program_id"]),
        sorted(
            requirement_documents,
            key=lambda document: (document["program_id"], document["requirement_id"]),
        ),
        validation_errors,
    )


def _upsert_documents(
    collection: Any,
    key_fields: Tuple[str, ...],
    documents: List[Dict[str, Any]],
) -> Dict[str, int]:
    counts = {"inserted": 0, "updated": 0, "unchanged": 0}
    for document in documents:
        result = collection.update_one(
            {key: document[key] for key in key_fields},
            {"$set": document},
            upsert=True,
        )
        if result.upserted_id is not None:
            counts["inserted"] += 1
        elif result.modified_count:
            counts["updated"] += 1
        else:
            counts["unchanged"] += 1
    return counts


def main() -> int:
    courses, programs, requirements, validation_errors = build_curriculum_documents()
    if validation_errors:
        print(f"Validation errors ({len(validation_errors)}):")
        for error in validation_errors:
            print(f"- {error}")
        return 1

    print("Validation errors: none.")

    from app.db.database import database

    database.client.admin.command("ping")
    results = (
        ("courses", _upsert_documents(database["courses"], ("course_id",), courses)),
        (
            "degree programs",
            _upsert_documents(database["degree_programs"], ("program_id",), programs),
        ),
        (
            "degree requirements",
            _upsert_documents(
                database["degree_requirements"],
                ("program_id", "requirement_id"),
                requirements,
            ),
        ),
    )
    for collection_name, counts in results:
        print(
            f"{collection_name}: {counts['inserted']} inserted, "
            f"{counts['updated']} updated, {counts['unchanged']} unchanged."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())