from flask import Flask, request, jsonify

from ice_breaker.ice_breaker import ice_break

app = Flask(__name__)


def process():
    name = request.form["name"]
    person_info, profile_pic_url = ice_break(name)

    return jsonify(
        {
            "summary": person_info.summary,
            "interests": person_info.interests,
            "facts": person_info.facts,
            "ice_breakers": person_info.ice_breakers,
            "picture_url": profile_pic_url,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
