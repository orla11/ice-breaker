from flask import Flask, request, jsonify

from ice_breaker import ice_break

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    name = request.form["name"]
    person_info, profile_pic_url = ice_break(name)

    return jsonify(
        {
            "summary": person_info.summary,
            "facts": person_info.facts,
            "ice_breakers": person_info.ice_breakers,
            "picture_url": profile_pic_url,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
