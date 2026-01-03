run:
	streamlit run ./main.py

# Docker commands
docker-build:
	docker build -t chilingo:latest .

docker-run:
	docker run -p 8094:8094 -v chilingo-audio:/tmp/chilingo chilingo:latest

# Shorthand
build: docker-build

docker: docker-compose-up
