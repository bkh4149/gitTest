from models import SurveyResponse, db


class TestSurveyResponse:
    def test_create_response(self, app, db_session):
        response = SurveyResponse(
            age_group="20代",
            favorite_food="寿司",
            favorite_movie="千と千尋の神隠し",
        )
        db_session.add(response)
        db_session.commit()

        saved = SurveyResponse.query.first()
        assert saved is not None
        assert saved.age_group == "20代"
        assert saved.favorite_food == "寿司"
        assert saved.favorite_movie == "千と千尋の神隠し"
        assert saved.created_at is not None

    def test_to_dict(self, app, db_session):
        response = SurveyResponse(
            age_group="30代",
            favorite_food="ラーメン",
            favorite_movie="君の名は。",
        )
        db_session.add(response)
        db_session.commit()

        data = response.to_dict()
        assert data["age_group"] == "30代"
        assert data["favorite_food"] == "ラーメン"
        assert data["favorite_movie"] == "君の名は。"
        assert "id" in data
        assert "created_at" in data

    def test_multiple_responses(self, app, db_session):
        for i in range(3):
            db_session.add(
                SurveyResponse(
                    age_group="40代",
                    favorite_food="カレー",
                    favorite_movie=f"映画{i}",
                )
            )
        db_session.commit()

        assert SurveyResponse.query.count() == 3
