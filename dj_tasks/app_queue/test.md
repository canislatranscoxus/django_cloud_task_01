curl -i -X POST http://127.0.0.1:8000/handler_animal/   \
-H "Content-Type: application/json"                     \
-d '{ "animal": "cat", "name":"Little Paws", "age": 2 }'        