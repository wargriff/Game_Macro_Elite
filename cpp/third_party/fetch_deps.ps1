# Telecharge httplib + nlohmann/json (headers uniquement)
$ErrorActionPreference = 'Stop'
$Out = Join-Path $PSScriptRoot 'include'
New-Item -ItemType Directory -Path $Out -Force | Out-Null

$files = @{
    'httplib.h' = 'https://raw.githubusercontent.com/yhirose/cpp-httplib/v0.15.3/httplib.h'
    'json.hpp'  = 'https://raw.githubusercontent.com/nlohmann/json/v3.11.3/single_include/nlohmann/json.hpp'
}

foreach ($name in $files.Keys) {
    $dest = Join-Path $Out $name
    if ($name -eq 'json.hpp') {
        $dir = Split-Path $dest -Parent
        New-Item -ItemType Directory -Path (Join-Path $dir 'nlohmann') -Force | Out-Null
        $dest = Join-Path $dir 'nlohmann\json.hpp'
    }
    Write-Host "Download $name"
    Invoke-WebRequest -Uri $files[$name] -OutFile $dest -UseBasicParsing
}

Write-Host "OK -> cpp/third_party/include/"
