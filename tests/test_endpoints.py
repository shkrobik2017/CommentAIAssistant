import httpx
import pytest

from app import app
from settings import settings


async def login():
    async with httpx.AsyncClient(
        app=app,
        base_url=settings.BASE_URL
    ) as client:
        login_data = {
            "username": settings.BASE_USER_USERNAME,
            "password": settings.BASE_USER_PASSWORD,
        }
        response = await client.post("/auth/token", data=login_data)
        return response.json()["access_token"]


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "request_data,expected_status",
    [
        (
            {
                "content": ""
            },
            200
        ),
        (
            {
                "assignment_description": "Task of the project is to create a simple library data managing code",
                "github_repo_url": "https://github.com/shkrobik2017/SQLAlchemyPet",
                "candidate_level": "Lead"
            },
            400
        ),
        (
            {
                "assignment_description": "Task of the project is to create a simple library data managing code",
                "github_repo_url": "https://github.com/shkrobik2017/SQLAlchemyPet",
                "candidate_level": 555
            },
            422
        )
    ]
)
async def test_generate_response_success(request_data, expected_status):
    async with httpx.AsyncClient(base_url=settings.BASE_URL, timeout=60) as client:
        response = await client.post(
            url="/upload",
            json=request_data,
            headers={"Authorization": f"Bearer {await login()}"}
        )

        assert response.status_code == expected_status
