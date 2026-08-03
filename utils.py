import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

def save_results(res, folder, file_name: str = "test_metrics.json"):
    output_path = Path(folder) / file_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics = {}
    if res:
        metrics = {name: float(value) for name, value in res[0].items()}
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    return output_path

class TaskMgr:
    FINISHED_FILE: str = "finished.json"

    def __init__(self, work_dir: Optional[str | Path] = None):
        """
        If work_dir is None, use the current working directory.

        With Hydra:
            hydra.job.chdir=true

        Path.cwd() should be the current Hydra job directory.
        """
        self.work_dir = Path(work_dir) if work_dir is not None else Path("")
        self.finished_path = Path(os.path.join(self.work_dir, self.FINISHED_FILE))

    def finished(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Mark this task as finished.

        Only call this after the experiment successfully completes.
        """
        self.work_dir.mkdir(parents=True, exist_ok=True)

        payload = {
            "finished": True,
            "finished_at": datetime.now().isoformat(timespec="seconds"),
        }

        if metadata is not None:
            payload["metadata"] = metadata

        with open(self.finished_path, mode="w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def check_finished(self) -> bool:
        """
        Return True if this task has already finished.
        """
        if not self.finished_path.exists():
            return False

        try:
            with open(self.finished_path, mode="r", encoding="utf-8") as f:
                payload = json.load(f)

            return bool(payload.get("finished", False))

        except Exception:
            print(f"The task has been finished at {self.finished_path}.")
            # If the finished file is corrupted, do not skip the task.
            return False

    def remove_finished(self) -> None:
        """
        Remove the finished marker, useful if you want to rerun a task.
        """
        if self.finished_path.exists():
            self.finished_path.unlink()