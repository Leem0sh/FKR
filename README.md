## How to run:
1. git clone 
2. `pip install -r requirements.txt`
3. `docker-compose -f docker-compose.yml`
4. go to `127.0.0.1:8080` where you can see Kafka interface
5. `faust -A runner worker -l info`
6. `uvicorn api:app --reload`
