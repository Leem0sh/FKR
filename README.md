## What is this? 

Simple example of event-driven architecture with Kafka publish/subscribe, Redis Pub/Sub and Faust-streaming library.  


## How to run:
1. `git clone https://github.com/Leem0sh/FKR.git`
2. `pip install -r requirements.txt`
3. `docker-compose -f docker-compose.yml`
4. go to `http://127.0.0.1:8080` where you can see Kafka interface
5. `faust -A runner worker -l info`
6. `uvicorn api:app --reload`
7. `http://127.0.0.1:8000/docs`
