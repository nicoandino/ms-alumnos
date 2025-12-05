# Crear carpeta para K6
$k6Dir = "$env:LOCALAPPDATA\k6"
New-Item -ItemType Directory -Force -Path $k6Dir | Out-Null

# Descargar K6 (última versión)
$k6Version = "0.48.0"
$k6Url = "https://github.com/grafana/k6/releases/download/v$k6Version/k6-v$k6Version-windows-amd64.zip"
$k6Zip = "$k6Dir\k6.zip"

Write-Host "Descargando K6..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $k6Url -OutFile $k6Zip

# Descomprimir
Write-Host "Descomprimiendo..." -ForegroundColor Yellow
Expand-Archive -Path $k6Zip -DestinationPath $k6Dir -Force

# Mover el ejecutable
Move-Item "$k6Dir\k6-v$k6Version-windows-amd64\k6.exe" "$k6Dir\k6.exe" -Force

# Limpiar
Remove-Item $k6Zip
Remove-Item "$k6Dir\k6-v$k6Version-windows-amd64" -Recurse -Force

# Agregar al PATH permanentemente
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$k6Dir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$k6Dir", "User")
}

# Agregar al PATH de esta sesión
$env:Path += ";$k6Dir"

Write-Host "¡K6 instalado correctamente en: $k6Dir!" -ForegroundColor Green
Write-Host "Verificando instalación..." -ForegroundColor Yellow

k6 version