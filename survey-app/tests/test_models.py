import sqlite3

import pytest
from sqlalchemy import inspect

from models import SurveyResponse, db


class TestSurveyResponse:
    def test_create_response(self, app, db_session):
        response = SurveyResponse(
            age_group="20代",
            favorite_food="寿司",
            natto_frequency="毎日",
            region="関東",
            favorite_movie="千と千尋の神隠し",
        )
        db_session.add(response)
        db_session.commit()

        saved = SurveyResponse.query.first()
        assert saved is not None
        assert saved.age_group == "20代"
        assert saved.favorite_food == "寿司"
        assert saved.natto_frequency == "毎日"
        assert saved.region == "関東"
        assert saved.favorite_movie == "千と千尋の神隠し"
        assert saved.created_at is not None

    def test_to_dict(self, app, db_session):
        response = SurveyResponse(
            age_group="30代",
            favorite_food="ラーメン",
            natto_frequency="週に数回",
            region="近畿",
            favorite_movie="君の名は。",
        )
        db_session.add(response)
        db_session.commit()

        data = response.to_dict()
        assert data["age_group"] == "30代"
        assert data["favorite_food"] == "ラーメン"
        assert data["natto_frequency"] == "週に数回"
        assert data["region"] == "近畿"
        assert data["favorite_movie"] == "君の名は。"
        assert "id" in data
        assert "created_at" in data

    def test_multiple_responses(self, app, db_session):
        for i in range(3):
            db_session.add(
                SurveyResponse(
                    age_group="40代",
                    favorite_food="カレー",
                    natto_frequency="月に数回",
                    region="中部",
                    favorite_movie=f"映画{i}",
                )
            )
        db_session.commit()

        assert SurveyResponse.query.count() == 3


class TestDatabaseSchema:
    def test_production_db_has_all_columns(self, app):
        """本番DBのスキーマがモデル定義と一致するか検証する"""
        import os
        db_path = os.path.join(os.path.dirname(__file__), "..", "instance", "survey.db")
        if not os.path.exists(db_path):
            pytest.skip("本番DBファイルが存在しません")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(survey_responses)")
        db_columns = {row[1] for row in cursor.fetchall()}
        conn.close()

        model_columns = {c.key for c in inspect(SurveyResponse).mapper.column_attrs}

        missing = model_columns - db_columns
        assert not missing, f"本番DBに以下のカラムがありません: {missing}"
