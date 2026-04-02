import datetime
import uuid
import pytest


def test_base_model_inheritance():
    from app.models import Player

    model_id = uuid.uuid4()
    created_at = datetime.datetime(1, 1, 1)
    updated_at = datetime.datetime(1, 1, 1)
    image_url = "https://example.com/image.png"
    model = Player(
        user_id=model_id,
        username="John",
        rating=10,
        draws=0,
        losses=0,
        wins=0,
        image_url=image_url,
        created_at=created_at,
        updated_at=updated_at,
    )

    assert model.user_id == model_id
    assert model.username == "John"
    assert model.rating == 10
    assert model.draws == 0
    assert model.losses == 0
    assert model.wins == 0
    assert model.image_url == image_url
    assert model.created_at == created_at
    assert model.updated_at == updated_at


# Missing field: wins
def test_base_model_error():
    from app.models import Player

    with pytest.raises(ValueError):
        Player.from_row(
            {
                "id": uuid.uuid7(),
                "username": "John",
                "rating": 10,
                "created_at": "1",
                "updated_at": "1",
                "draws": 0,
                "losses": 0,
            }
        )


def test_generate_updated_fields():
    from app.utils import generate_updated_fields

    update_data = {"username": "John", "rating": 10, "draws": 0, "losses": 0}
    fields = generate_updated_fields(update_data)

    assert fields == ["username = $1", "rating = $2", "draws = $3", "losses = $4"]
