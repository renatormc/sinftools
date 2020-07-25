function Add-EnvPath {
    param(
        [Parameter(Mandatory = $true)]
        [string] 
        $Path,

        [Parameter(Mandatory = $false)]
        [ValidateSet('Machine', 'User', 'Session')]
        [string] $Container = 'Session'
    )

    if ($Container -ne 'Session') {
        $containerMapping = @{
            Machine = [EnvironmentVariableTarget]::Machine
            User    = [EnvironmentVariableTarget]::User
        }
        $containerType = $containerMapping[$Container]

        $persistedPaths = [Environment]::GetEnvironmentVariable('Path', $containerType) -split ';'
        if ($persistedPaths -notcontains $Path) {
            $persistedPaths = $persistedPaths + $Path | Where-Object { $_ }
            [Environment]::SetEnvironmentVariable('Path', $persistedPaths -join ';', $containerType)
        }
    }

    $envPaths = $env:Path -split ';'
    if ($envPaths -notcontains $Path) {
        $envPaths = $envPaths + $Path | Where-Object { $_ }
        $env:Path = $envPaths -join ';'
    }
}


if($args.Count -lt 1){
    throw "Não foi informada a pasta"
}

if (-Not (Test-Path $args[0] -PathType Container)){
    throw "A pasta informada não existe"
}
# Write-Host $args[0]
$options = [System.Management.Automation.Host.ChoiceDescription[]] @("&Todos os usuários", "&Somente eu")
[int]$defaultchoice = 1
$container = $host.UI.PromptForChoice("Selecione o contexto" , $Info , $Options, $defaultchoice)
switch ($container) {
    0 { 
        $container = "Machine"
     }
    1 {
        $container = "User"
    }
}
try {
    Add-EnvPath $args[0] -Container $container
    Write-Host "Pasta adicionada ao path. Se houver algum console aberto o reinicie para que a mudança tenha efeito neles."
}
catch {
    Write-Host "An error occurred:"
    Write-Host $_
}



