import pytest


@pytest.mark.django_db
def test_goal_category_create(user_factory, get_auth_client, board_participant_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)

    data = {
        "board": board_participant.board.id,
        "title": "test cat",
    }

    auth_client = get_auth_client(user)
    response = auth_client.post(
        "/goals/goal_category/create",
        data=data,
        content_type="application/json",
    )

    expected_response = {
        "id": response.data["id"],
        "title": "test cat",
        "is_deleted": False,
        "board": board_participant.board.id,
        "created": response.data["created"],
        "updated": response.data["updated"],
    }

    assert response.status_code == 201
    assert response.data == expected_response
