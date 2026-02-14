from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

AGE_GROUPS = ["10代以下", "20代", "30代", "40代", "50代", "60代以上"]
FOOD_CHOICES = ["寿司", "ラーメン", "カレー", "ハンバーグ", "パスタ", "その他"]
NATTO_CHOICES = ["毎日", "週に数回", "月に数回", "ほとんど食べない", "全く食べない"]
REGION_CHOICES = ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州・沖縄"]


class SurveyResponse(db.Model):
    __tablename__ = "survey_responses"

    id = db.Column(db.Integer, primary_key=True)
    age_group = db.Column(db.String(10), nullable=False)
    favorite_food = db.Column(db.String(20), nullable=False)
    natto_frequency = db.Column(db.String(20), nullable=False, server_default="")
    region = db.Column(db.String(10), nullable=False, server_default="")
    favorite_movie = db.Column(db.String(200), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "age_group": self.age_group,
            "favorite_food": self.favorite_food,
            "natto_frequency": self.natto_frequency,
            "region": self.region,
            "favorite_movie": self.favorite_movie,
            "created_at": self.created_at.isoformat(),
        }
