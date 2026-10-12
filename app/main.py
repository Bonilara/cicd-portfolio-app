from flask import Flask, jsonify, abort


app = Flask(__name__)

ITEMS = {1: "alpha", 2: "beta"}


@app.get("/")
def root():
    return jsonify(status="ok")


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/items/<int:item_id>")
def get_item(item_id):
    if item_id not in ITEMS:
        abort(404)
    return jsonify(id=item_id, name=ITEMS[item_id])