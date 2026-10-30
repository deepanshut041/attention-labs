"""Declare implementation boundaries without simulating attention results."""
def pending_result(mechanism: str, config: dict) -> dict:
    if mechanism not in config["scope"]["mechanisms"]:
        raise ValueError("Mechanism is outside this project's single-head scope")
    return {"project": config["project_id"], "mechanism": mechanism,
            "status": "not_implemented", "implemented_mechanisms": [],
            "message": "Implement and independently test this mechanism in its project phase."}
