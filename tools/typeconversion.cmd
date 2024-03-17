cd .\processer

cd .\online_server
python -m tools.to_jsonschema
cd ..\
json2ts -i ./schema/*.json  -o interface/src/lib/ml_api/api_types/
json2ts -i ./schema/kokkai/*.json  -o interface/src/lib/ml_api/api_types/kokkai
