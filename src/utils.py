from collections import defaultdict
from typing import List
from models.data import ContextResidency

def visualize_context_timelines(residency_list: List[ContextResidency]):
    """
    ASCII art by Codex - quick visualization of context timelines
    """
    contexts = defaultdict(list)
    for item in residency_list:
        contexts[item.context_name].append(item)

    for name in contexts:
        contexts[name].sort(key=lambda x: x.timestamp)

    all_timestamps = [item.timestamp for item in residency_list]
    if not all_timestamps:
        print("No data to visualize.")
        return

    global_min = min(all_timestamps)
    global_max = max(all_timestamps)
    total_duration = (global_max - global_min).total_seconds()

    timeline_width = 100

    print(f"\nTimeline Overview ({global_min.strftime('%b %d')} - {global_max.strftime('%b %d')})\n" + "=" * 100)

    for context_name, items in contexts.items():
        line = ['-'] * (timeline_width + 1)
        labels = []

        for item in items:
            if total_duration > 0:
                pos = int(((item.timestamp - global_min).total_seconds() / total_duration) * timeline_width)
            else:
                pos = 0

            day_str = item.timestamp.strftime('%a')
            time_str = item.timestamp.strftime('%H:%M:%S')
            short_ts = f"{day_str} {time_str}"

            label_text = f"[{item.event} @ {short_ts}]"

            line[pos] = 'o' if item.event == 'RESIDENT' else 'x'
            labels.append((pos, label_text))

        print(f"{context_name:<25} |{''.join(line)}|")
        print(f"{'':<25}  Events:")
        for pos, label in labels:
            print(f"{'':<27}  - Pos {pos:2d}: {label}")
        print("-" * 80)