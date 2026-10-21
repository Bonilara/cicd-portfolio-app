import os
from flask import Flask, jsonify, abort
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

ITEMS = {1: "alpha", 2: "beta"}


@app.get("/")
def root():
    return jsonify(status="ok-v2")


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/items/<int:item_id>")
def get_item(item_id):
    if item_id not in ITEMS:
        abort(404)
    return jsonify(id=item_id, name=ITEMS[item_id])

_client = None

def _get_secret(name):
    global _client
    if _client is None:
        _client = SecretClient(
            vault_url=os.environ["KEY_VAULT_URL"],
            credential=DefaultAzureCredential(),
        )
    return _client.get_secret(name).value


@app.get("/secret-check")
def secret_check():
    try:
        return jsonify(secret_loaded=bool(_get_secret("demo-api-key")))
    except Exception:
        app.logger.exception("Key Vault read failed")
        return jsonify(secret_loaded=False), 503