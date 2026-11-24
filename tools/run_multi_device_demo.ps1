param(
    [string]$TestPath = "tests/login/test_valid_login.py"
)

$ErrorActionPreference = "Stop"

$devices = @(
    @{ Profile = "pixel_api31"; Udid = "emulator-5554"; SystemPort = 8200; Results = "allure-results" },
    @{ Profile = "small_phone_api34"; Udid = "emulator-5556"; SystemPort = 8201; Results = "allure-results-small_phone_api34" }
)

Write-Host "Checking Android emulator availability..."
$adbOutput = @(adb devices 2>&1)
$adbExitCode = $LASTEXITCODE
if ($adbExitCode -ne 0) {
    Write-Error "Unable to execute 'adb devices'. Ensure Android SDK platform-tools are available on PATH."
    exit 1
}

$deviceStatuses = @{}
foreach ($line in $adbOutput) {
    if ($line -match '^([^\s]+)\s+(\S+)$') {
        $deviceStatuses[$matches[1]] = $matches[2]
    }
}

$missing = @($devices | Where-Object { $deviceStatuses[$_.Udid] -ne "device" })
if ($missing.Count -gt 0) {
    foreach ($device in $missing) {
        $status = if ($deviceStatuses.ContainsKey($device.Udid)) { $deviceStatuses[$device.Udid] } else { "not found" }
        Write-Error "Profile '$($device.Profile)' is unavailable: $($device.Udid) status is '$status'. Start that emulator and ensure it appears as 'device' in 'adb devices'."
    }
    exit 1
}

$pytestArgs = @($TestPath -split '\s+' | Where-Object { $_ })
$results = @()

foreach ($device in $devices) {
    Write-Host "`nRunning $TestPath on $($device.Profile) ($($device.Udid), systemPort $($device.SystemPort))..."
    & python -m pytest @pytestArgs --device $device.Profile -v
    $exitCode = $LASTEXITCODE
    $results += [pscustomobject]@{
        Profile = $device.Profile
        Udid = $device.Udid
        SystemPort = $device.SystemPort
        Status = if ($exitCode -eq 0) { "PASS" } else { "FAIL" }
        ExitCode = $exitCode
        AllureResults = $device.Results
    }
}

Write-Host "`nMulti-device demo summary"
$results | Format-Table Profile, Udid, SystemPort, Status, ExitCode, AllureResults -AutoSize
foreach ($result in $results) {
    Write-Host "$($result.Profile): allure serve $($result.AllureResults)"
}

if ($results | Where-Object { $_.ExitCode -ne 0 }) {
    exit 1
}

exit 0
