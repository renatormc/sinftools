function Set-EnvironmentVariable {
    param
    (
        [Parameter(Mandatory = $true)]
        [String]
        $Name,
    
        [Parameter(Mandatory = $true)]
        [String]
        $Value,
    
        [Parameter(Mandatory = $true)]
        [EnvironmentVariableTarget]
        $Target
    )
    [System.Environment]::SetEnvironmentVariable($Name, $Value, $Target)
}

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

function Remove-EnvPath {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Path,

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
        if ($persistedPaths -contains $Path) {
            $persistedPaths = $persistedPaths | Where-Object { $_ -and $_ -ne $Path }
            [Environment]::SetEnvironmentVariable('Path', $persistedPaths -join ';', $containerType)
        }
    }

    $envPaths = $env:Path -split ';'
    if ($envPaths -contains $Path) {
        $envPaths = $envPaths | Where-Object { $_ -and $_ -ne $Path }
        $env:Path = $envPaths -join ';'
    }
}

function Get-EnvPath {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet('Machine', 'User')]
        [string] $Container
    )

    $containerMapping = @{
        Machine = [EnvironmentVariableTarget]::Machine
        User    = [EnvironmentVariableTarget]::User
    }
    $containerType = $containerMapping[$Container]

    [Environment]::GetEnvironmentVariable('Path', $containerType) -split ';' |
    Where-Object { $_ }
}


Set-EnvironmentVariable -Name "SINFTOOLS" -Value $PSScriptRoot -Target Machine


$env:Path -split ';' | ForEach-Object {
    if ($_.Contains("sinftools\scripts")) {
        Remove-EnvPath $_ -Container "Machine"
        Remove-EnvPath $_ -Container "User"
        Remove-EnvPath $_ -Container "Session"
    }
}


Add-EnvPath (Join-Path -Path $PSScriptRoot -ChildPath "scripts") -Container "Machine"

Write-Host "Sua máquina foi configurada para uso do SINFTOOLS. Bom uso!!"



