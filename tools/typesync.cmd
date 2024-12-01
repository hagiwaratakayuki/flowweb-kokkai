

python -m tools.sync_model
python -m tools.api_server.create_responsetype
python -m tools.api_server.to_jsonschema

tools\call_json2ts.cmd
tools\call_sync.cmd
