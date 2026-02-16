from fastmcp import FastMCP

mcp = FastMCP("ThreatModelingMCP")


@mcp.tool
def classify_risk(likelihood: float, impact: float) -> dict:
    score = round(likelihood * impact * 10, 2)
    if score >= 7:
        level = "high"
    elif score >= 4:
        level = "medium"
    else:
        level = "low"
    return {"risk_score": score, "risk_level": level}


@mcp.resource("threat://frameworks")
def frameworks() -> list[str]:
    return ["STRIDE", "LINDDUN", "PASTA", "DREAD"]


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8004)
