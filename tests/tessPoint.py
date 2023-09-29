from tess_point import TessPoint

@app.route("/get_star_info", methods=["GET"])
def get_star_info():
    tic_id = request.args.get("tic_id")

    # Create a TessPoint object
    tess_point = TessPoint()

    try:
        star_info = tess_point.get_star_info(tic_id)
        return jsonify(star_info)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)