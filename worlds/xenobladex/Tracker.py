from typing import TYPE_CHECKING, Any, Optional

from Options import Option


if TYPE_CHECKING:
    from . import XenobladeXWorld


def prepare_tracker(world: "XenobladeXWorld") -> None:
    re_gen_passthrough = getattr(world.multiworld, "re_gen_passthrough", {})
    if re_gen_passthrough:
        # Get the passed through slot data from the real generation
        slot_data: dict[str, Any] = re_gen_passthrough[world.game]
        slot_options: dict[str, Any] = slot_data.get("options", {})
        # Set all your options here instead of getting them from the yaml
        for key, value in slot_options.items():
            opt: Optional[Option] = getattr(world.options, key, None)
            if opt is not None:
                setattr(world.options, key, opt.from_any(value))
