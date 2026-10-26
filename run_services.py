mkdir Gym web
cd Gym web
poetry run uvicorn main:app --reload
cd ..


mkdir api_gateway
cd api_gateway
poetry run uvicorn main:app --reload
cd ..


mkdir auth_service
cd auth_service
poetry run uvicorn main:app --reload
cd ..


mkdir membership_service
cd membership_service
poetry run uvicorn main:app --reload
cd ..


mkdir attendance_service
cd attendance_service
poetry run uvicorn main:app --reload
cd ..


mkdir inventory_service
cd inventory_service
poetry run uvicorn main:app --reload
cd ..


mkdir order_service
cd order_service
poetry run uvicorn main:app --reload
cd ..


mkdir salary_service
cd salary_service
poetry run uvicorn main:app --reload
cd ..


mkdir diet_service
cd diet_service
poetry run uvicorn main:app --reload
cd ..


mkdir workout_service
cd workout_service
poetry run uvicorn main:app --reload
cd ..


mkdir payment_service
cd payment_service
poetry run uvicorn main:app --reload
cd ..


mkdir search_service
cd search_service
poetry run uvicorn main:app --reload
cd ..


mkdir setting_service
cd setting_service
poetry run uvicorn main:app --reload
cd ..


mkdir feedback_service
cd feedback_service
poetry run uvicorn main:app --reload
cd ..
