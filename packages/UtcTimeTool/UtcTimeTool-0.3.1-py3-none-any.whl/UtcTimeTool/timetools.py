def getOrginalZone(time: str) -> str:
    """returns time zone without UTC"""
    return time.split("UTC")[-1]

def getUtcTime(time: str) -> str:
    """returns time zone with UTC"""
    return "UTC" + time

