import json

from models import SurveyResponse


class TestSurveyPage:
    def test_get_survey(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "アンケート" in response.data.decode("utf-8")

    def test_survey_contains_form(self, client):
        response = client.get("/")
        html = response.data.decode("utf-8")
        assert "age_group" in html
        assert "favorite_food" in html
        assert "favorite_movie" in html


class TestSubmit:
    def test_submit_valid(self, client, db_session):
        response = client.post(
            "/submit",
            data={
                "age_group": "20代",
                "favorite_food": "寿司",
                "favorite_movie": "千と千尋の神隠し",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "ありがとう" in response.data.decode("utf-8")
        assert SurveyResponse.query.count() == 1

    def test_submit_missing_age(self, client):
        response = client.post(
            "/submit",
            data={
                "age_group": "",
                "favorite_food": "寿司",
                "favorite_movie": "映画",
            },
        )
        assert response.status_code == 200
        assert "年齢層を選択" in response.data.decode("utf-8")

    def test_submit_missing_food(self, client):
        response = client.post(
            "/submit",
            data={
                "age_group": "20代",
                "favorite_food": "",
                "favorite_movie": "映画",
            },
        )
        assert response.status_code == 200
        assert "好きな食べ物を選択" in response.data.decode("utf-8")

    def test_submit_missing_movie(self, client):
        response = client.post(
            "/submit",
            data={
                "age_group": "20代",
                "favorite_food": "寿司",
                "favorite_movie": "",
            },
        )
        assert response.status_code == 200
        assert "好きな映画を入力" in response.data.decode("utf-8")

    def test_submit_invalid_age_group(self, client):
        response = client.post(
            "/submit",
            data={
                "age_group": "不正な値",
                "favorite_food": "寿司",
                "favorite_movie": "映画",
            },
        )
        assert response.status_code == 200
        assert "年齢層を選択" in response.data.decode("utf-8")

    def test_submit_invalid_food(self, client):
        response = client.post(
            "/submit",
            data={
                "age_group": "20代",
                "favorite_food": "不正な値",
                "favorite_movie": "映画",
            },
        )
        assert response.status_code == 200
        assert "好きな食べ物を選択" in response.data.decode("utf-8")

    def test_submit_movie_too_long(self, client):
        response = client.post(
            "/submit",
            data={
                "age_group": "20代",
                "favorite_food": "寿司",
                "favorite_movie": "あ" * 201,
            },
        )
        assert response.status_code == 200
        assert "200文字以内" in response.data.decode("utf-8")


class TestResults:
    def test_get_results_page(self, client):
        response = client.get("/results")
        assert response.status_code == 200
        assert "集計結果" in response.data.decode("utf-8")

    def test_api_results_empty(self, client):
        response = client.get("/api/results")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["total"] == 0

    def test_api_results_with_data(self, client, db_session):
        db_session.add(
            SurveyResponse(
                age_group="20代",
                favorite_food="寿司",
                favorite_movie="千と千尋の神隠し",
            )
        )
        db_session.add(
            SurveyResponse(
                age_group="30代",
                favorite_food="ラーメン",
                favorite_movie="君の名は。",
            )
        )
        db_session.commit()

        response = client.get("/api/results")
        data = json.loads(response.data)
        assert data["total"] == 2
        assert data["age_groups"]["20代"] == 1
        assert data["age_groups"]["30代"] == 1
        assert data["favorite_foods"]["寿司"] == 1
        assert "千と千尋の神隠し" in data["favorite_movies"]


class TestThanks:
    def test_get_thanks(self, client):
        response = client.get("/thanks")
        assert response.status_code == 200
        assert "ありがとう" in response.data.decode("utf-8")


class TestSecurityHeaders:
    def test_security_headers(self, client):
        response = client.get("/")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
