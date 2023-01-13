# FastApi
Sample Fast Api

1.Create Virtual Env using python -m venv env
2.Install Require dependency using pip install -r requirement.txt
3.for running app run this command uvicorn main:app --reload

for Migrations

Please run Below command
alembic init migrations ->this will create env file we need to give database url
create migrations file 
alembic revision --autogenerate -m "add models"




