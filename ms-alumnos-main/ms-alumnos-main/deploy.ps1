# ===========================
# DEPLOY TOTAL DEL ECOSISTEMA
# ===========================

Write-Host "🔧 Iniciando deploy de Traefik..." -ForegroundColor Cyan
docker stack deploy -c traefik/docker-traefik.yml traefik

Write-Host "🚀 Deploy de alumnos-service..." -ForegroundColor Cyan
docker stack deploy -c PRUEBA/docker/docker-compose.yml alumnos

Write-Host "==============================================="
Write-Host "🟢 Deploy completo!"
Write-Host "🌐 Traefik: http://localhost:8080/dashboard"
Write-Host "📡 Alumnos-service: https://alumnos.universidad.localhost"
Write-Host "==============================================="
