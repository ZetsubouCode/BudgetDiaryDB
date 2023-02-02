#!./venv/Scripts/python
source ./venv/Scripts/activate
pip install -r requirements.txt
./venv/Scripts/python.exe -m uvicorn budgetdiary:app --host 0.0.0.0 --port 55001 --reload