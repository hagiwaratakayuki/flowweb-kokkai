REM need call from project top
CALL .\tools\emurater_env.cmd
cd .\api_server
uvicorn main:app --reload