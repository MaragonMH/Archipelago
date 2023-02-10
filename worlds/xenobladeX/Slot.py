from typing import Dict

def generate_slot_data(base_id: int, max_type_count: int) -> Dict[str, object]:
	slot_data: Dict[str, object] = {}
	slot_data["base_id"] = base_id
	slot_data["max_type_count"] = max_type_count
	return slot_data