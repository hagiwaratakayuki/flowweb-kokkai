


python -m tools.api_server.to_jsonschema

json2ts -i ./schema/*.json  -o interface/src/lib/ml_api/api_types/
json2ts -i ./schema/kokkai/*.json  -o interface/src/lib/ml_api/api_types/kokkai
