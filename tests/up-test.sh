# saúde
curl -s http://localhost:8000/healthz; echo
curl -s http://localhost:8000/readyz; echo

## criar veículos
#curl -s -X POST http://localhost:8000/vehicles \
#  -H "Content-Type: application/json" \
#  -d '{"brand":"Honda","model":"Civic","year":2019,"color":"Preto","price":78000}'; echo

# listar disponíveis
curl -s "http://localhost:8000/vehicles?status=available"; echo

# reservar (troque {ID})
curl -s -X POST "http://localhost:8000/vehicles/00b66ab5-60c6-42ec-85cc-6ea6ce094923/reserve" \
  -H "Content-Type: application/json" \
  -d '{"reserved_by":"kaneda"}'; echo

# vender (troque {ID})
curl -s -X POST "http://localhost:8000/vehicles/2d637e93-8d4b-40e4-8c53-846cc6cb3941/sell"; echo

# conferir vendidos
curl -s "http://localhost:8000/vehicles?status=sold"; echo
