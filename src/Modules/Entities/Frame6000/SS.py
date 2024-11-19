from dataclasses import dataclass
@dataclass
class SS:
    safeCircClosed = 0
    scannersMuted = 0
    frontEStopsPressed = 0
    rearEStopsPressed = 0
    frontBumperNotTriggered = 0
    rearBumperNotTriggered = 0
    frontScannerSafetyZoneNotViolated = 0
    rearScannerSafetyZoneNotViolated = 0
    frontScannerWarningZoneNotViolated = 0
    rearScannerWarningZoneNotViolated = 0
    scannersActiveZones = 0
    agvVelocityActiveZone = 0