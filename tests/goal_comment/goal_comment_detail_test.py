import pytest


@pytest.mark.django_db
def test_goal_comment_detail(user_factory, get_auth_client, board_participant_factory, goal_comment_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    goal_comment = goal_comment_factory(
        goal__category__board=board_participant.board,
        goal__category__user=user,
        goal__user=user,
        user=user,
    )

    expected_response = {
        "id": goal_comment.id,
        "text": goal_comment.text,
        "goal": goal_comment.goal.id,
        "created": goal_comment.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated": goal_comment.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
    }

    auth_client = get_auth_client(user)

    response = auth_client.get(f"/goals/goal_comment/{goal_comment.id}")

    assert response.status_code == 200
    assert response.data == expected_response

