import os
from collections import Counter

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

from config import Config
from models import AGE_GROUPS, FOOD_CHOICES, NATTO_CHOICES, REGION_CHOICES, SurveyResponse, db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    CSRFProtect(app)

    if not app.config.get("TESTING"):
        Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=["200 per day", "50 per hour"],
        )

    with app.app_context():
        os.makedirs(
            os.path.join(os.path.dirname(__file__), "instance"), exist_ok=True
        )
        db.create_all()

    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    @app.route("/")
    def survey():
        return render_template(
            "survey.html", age_groups=AGE_GROUPS, food_choices=FOOD_CHOICES,
            natto_choices=NATTO_CHOICES, region_choices=REGION_CHOICES
        )

    @app.route("/submit", methods=["POST"])
    def submit():
        age_group = request.form.get("age_group", "").strip()
        favorite_food = request.form.get("favorite_food", "").strip()
        natto_frequency = request.form.get("natto_frequency", "").strip()
        region = request.form.get("region", "").strip()
        favorite_movie = request.form.get("favorite_movie", "").strip()

        errors = []
        if age_group not in AGE_GROUPS:
            errors.append("年齢層を選択してください。")
        if favorite_food not in FOOD_CHOICES:
            errors.append("好きな食べ物を選択してください。")
        if natto_frequency not in NATTO_CHOICES:
            errors.append("納豆を食べる頻度を選択してください。")
        if region not in REGION_CHOICES:
            errors.append("お住まいの地方を選択してください。")
        if not favorite_movie:
            errors.append("好きな映画を入力してください。")
        if len(favorite_movie) > 200:
            errors.append("好きな映画は200文字以内で入力してください。")

        if errors:
            return render_template(
                "survey.html",
                age_groups=AGE_GROUPS,
                food_choices=FOOD_CHOICES,
                natto_choices=NATTO_CHOICES,
                region_choices=REGION_CHOICES,
                errors=errors,
                age_group=age_group,
                favorite_food=favorite_food,
                natto_frequency=natto_frequency,
                region=region,
                favorite_movie=favorite_movie,
            )

        response = SurveyResponse(
            age_group=age_group,
            favorite_food=favorite_food,
            natto_frequency=natto_frequency,
            region=region,
            favorite_movie=favorite_movie,
        )
        db.session.add(response)
        db.session.commit()

        return redirect(url_for("thanks"))

    @app.route("/thanks")
    def thanks():
        return render_template("thanks.html")

    @app.route("/results")
    def results():
        return render_template("results.html")

    @app.route("/api/results")
    def api_results():
        responses = SurveyResponse.query.all()

        age_counter = Counter(r.age_group for r in responses)
        age_data = {group: age_counter.get(group, 0) for group in AGE_GROUPS}

        food_counter = Counter(r.favorite_food for r in responses)
        food_data = {food: food_counter.get(food, 0) for food in FOOD_CHOICES}

        natto_counter = Counter(r.natto_frequency for r in responses if r.natto_frequency)
        natto_data = {choice: natto_counter.get(choice, 0) for choice in NATTO_CHOICES}

        region_counter = Counter(r.region for r in responses if r.region)
        region_data = {region: region_counter.get(region, 0) for region in REGION_CHOICES}

        movies = [r.favorite_movie for r in responses]

        return jsonify(
            {
                "total": len(responses),
                "age_groups": age_data,
                "favorite_foods": food_data,
                "natto_frequency": natto_data,
                "regions": region_data,
                "favorite_movies": movies,
            }
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
