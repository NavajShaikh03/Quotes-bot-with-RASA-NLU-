# =============================================================================
# Quotes Recommendation Bot - Single Command Startup Script
# =============================================================================
# This script starts the entire chatbot system with ONE command:
#   .\run_bot.ps1
#
# It will:
#   1. Activate the virtual environment
#   2. Train the Rasa model automatically
#   3. Start the Rasa Action Server (port 5055)
#   4. Start the Rasa API server (port 5005) with CORS enabled
#   5. Start the Web UI server (port 5000)
#   6. Open the chatbot in your browser
# =============================================================================

param(
    [switch]$SkipTraining,
    [switch]$SkipWebUI
)

# Script configuration
$ProjectRoot = $PSScriptRoot
$VenvPath = Join-Path $ProjectRoot "venv"
$ScriptsPath = Join-Path $VenvPath "Scripts"
$ActionServerPort = 5055
$RasaServerPort = 5005
$WebUIPort = 5500

# Colors for console output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    $colorMap = @{
        "Red"    = [ConsoleColor]::Red
        "Green"  = [ConsoleColor]::Green
        "Yellow" = [ConsoleColor]::Yellow
        "Cyan"   = [ConsoleColor]::Cyan
        "White"  = [ConsoleColor]::White
    }
    Write-Host $Message -ForegroundColor $colorMap[$Color]
}

# Check if a port is in use
function Test-PortInUse {
    param([int]$Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue
    return $connection.TcpTestSucceeded
}

# Wait for a service to be ready
function Wait-ForService {
    param(
        [string]$Url,
        [int]$TimeoutSeconds = 30
    )
    $elapsed = 0
    while ($elapsed -lt $TimeoutSeconds) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                return $true
            }
        }
        catch {
            # Service not ready yet
        }
        Start-Sleep -Seconds 2
        $elapsed += 2
    }
    return $false
}

# =============================================================================
# MAIN SCRIPT
# =============================================================================

Write-ColorOutput "`n============================================================" "Cyan"
Write-ColorOutput "  Quotes Recommendation Bot - Starting Up" "Cyan"
Write-ColorOutput "============================================================`n" "Cyan"

# Step 1: Check if virtual environment exists
Write-ColorOutput "[1/6] Checking virtual environment..." "Yellow"
if (-not (Test-Path (Join-Path $VenvPath "Scripts\Activate.ps1"))) {
    Write-ColorOutput "[ERROR] Virtual environment not found at: $VenvPath" "Red"
    Write-ColorOutput "Please create one:" "Red"
    Write-ColorOutput "  python -m venv venv" "White"
    Write-ColorOutput "  .\venv\Scripts\Activate.ps1" "White"
    Write-ColorOutput "  pip install -r requirements.txt" "White"
    exit 1
}
Write-ColorOutput "  Virtual environment found.`n" "Green"

# Step 2: Check port availability
Write-ColorOutput "[2/6] Checking port availability..." "Yellow"
$portsInUse = @()

if (Test-PortInUse -Port $ActionServerPort) {
    $portsInUse += $ActionServerPort
    Write-ColorOutput "  [WARNING] Port $ActionServerPort (Action Server) is already in use!" "Yellow"
}

if (Test-PortInUse -Port $RasaServerPort) {
    $portsInUse += $RasaServerPort
    Write-ColorOutput "  [WARNING] Port $RasaServerPort (RASA API) is already in use!" "Yellow"
}

if (Test-PortInUse -Port $WebUIPort) {
    $portsInUse += $WebUIPort
    Write-ColorOutput "  [WARNING] Port $WebUIPort (Web UI) is already in use!" "Yellow"
}

if ($portsInUse.Count -gt 0) {
    Write-ColorOutput "`n  Some ports are in use. Trying to continue anyway..." "Yellow"
    Write-ColorOutput "  If servers fail to start, please stop other processes using these ports.`n" "Yellow"
}

# Step 3: Activate virtual environment and train model
Write-ColorOutput "[3/6] Training Rasa model..." "Yellow"

# Check if model already exists
$modelsPath = Join-Path $ProjectRoot "models"
$modelFiles = @()
if (Test-Path $modelsPath) {
    $modelFiles = Get-ChildItem -Path $modelsPath -Filter "*.tar.gz" -ErrorAction SilentlyContinue
}

if ($SkipTraining -and $modelFiles.Count -gt 0) {
    Write-ColorOutput "  Skipping training (model exists).`n" "Green"
}
else {
    Write-ColorOutput "  Training started... This may take a few minutes.`n" "Green"
    
    # Create training command
    $trainCommand = "cd '$ProjectRoot'; .\venv\Scripts\Activate.ps1; rasa train"
    
    # Run training in a new window (so it doesn't block)
    Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", $trainCommand -Wait
    
    Write-ColorOutput "  Training completed!`n" "Green"
}

# Step 4: Start Rasa Action Server
Write-ColorOutput "[4/6] Starting Rasa Action Server (port $ActionServerPort)..." "Yellow"

$actionServerScript = @"
cd '$ProjectRoot'
& '$(Join-Path $ScriptsPath "Activate.ps1")'
Write-Host 'Starting Rasa Action Server on port $ActionServerPort...' -ForegroundColor Green
rasa run actions --port $ActionServerPort
"@

# Check if port is available
if (-not (Test-PortInUse -Port $ActionServerPort)) {
    Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", $actionServerScript -WindowStyle Normal
    Write-ColorOutput "  Action Server started in new window.`n" "Green"
}
else {
    Write-ColorOutput "  [SKIPPED] Port $ActionServerPort is already in use. Is the Action Server already running?`n" "Yellow"
}

# Wait for action server to initialize
Write-ColorOutput "  Waiting for Action Server to initialize..." "Cyan"
Start-Sleep -Seconds 5

# Step 5: Start Rasa API Server
Write-ColorOutput "[5/6] Starting Rasa API Server (port $RasaServerPort)..." "Yellow"

$rasaServerScript = @"
cd '$ProjectRoot'
& '$(Join-Path $ScriptsPath "Activate.ps1")'
Write-Host 'Starting Rasa API Server on port $RasaServerPort with CORS enabled...' -ForegroundColor Green
rasa run --enable-api --cors '*' --port $RasaServerPort
"@

# Check if port is available
if (-not (Test-PortInUse -Port $RasaServerPort)) {
    Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", $rasaServerScript -WindowStyle Normal
    Write-ColorOutput "  Rasa API Server started in new window.`n" "Green"
}
else {
    Write-ColorOutput "  [SKIPPED] Port $RasaServerPort is already in use. Is the Rasa API Server already running?`n" "Yellow"
}

# Wait for Rasa server to initialize
Write-ColorOutput "  Waiting for Rasa API Server to initialize..." "Cyan"
Start-Sleep -Seconds 5

# Step 6: Start Web UI and open browser
if (-not $SkipWebUI) {
    Write-ColorOutput "[6/6] Starting Web UI and opening browser..." "Yellow"
    
    $webUIScript = @"
cd '$ProjectRoot'
& '$(Join-Path $ScriptsPath "Activate.ps1")'
Write-Host 'Starting Web UI on port $WebUIPort...' -ForegroundColor Green
python web_integration/chat_ui.py
"@

    # Check if port is available
    if (-not (Test-PortInUse -Port $WebUIPort)) {
        Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", $webUIScript -WindowStyle Normal
        Write-ColorOutput "  Web UI Server started in new window.`n" "Green"
    }
    else {
        Write-ColorOutput "  [SKIPPED] Port $WebUIPort is already in use. Is the Web UI already running?`n" "Yellow"
    }
    
    # Wait for web UI to start
    Start-Sleep -Seconds 3
    
    # Open browser
    Write-ColorOutput "  Opening chatbot in browser...`n" "Green"
    Start-Process "http://localhost:$WebUIPort"
}
else {
    Write-ColorOutput "[6/6] Skipping Web UI (as requested).`n" "Yellow"
}

# Final message
Write-ColorOutput "============================================================" "Cyan"
Write-ColorOutput "  Chatbot Ready!" "Green"
Write-ColorOutput "============================================================" "Cyan"
Write-ColorOutput @"

  Servers started:
    - Rasa Action Server:  http://localhost:$ActionServerPort
    - Rasa API Server:     http://localhost:$RasaServerPort
    - Web UI:              http://localhost:$WebUIPort

  If windows don't appear, check:
    - Ports 5005, 5055, and 5500 are available
    - Virtual environment is properly set up

  To stop the servers, simply close the PowerShell windows.

"@ "White"

Write-ColorOutput "Press any key to exit (servers will keep running)..." "Yellow"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
