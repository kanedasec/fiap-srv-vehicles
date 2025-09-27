# saúde
curl -s http://localhost:8001/healthz
echo ""
curl -s http://localhost:8001/readyz
echo ""
# listar (sem dados deve vir [])
curl -s "http://localhost:8001/vehicles?status=AVAILABLE"
echo ""
# criar
curl -s -X POST http://localhost:8001/vehicles \
  -H "Content-Type: application/json" \
  -d '{"brand":"Ford","model":"Fiesta","year":2018,"color":"blue","price":45000}'
echo ""