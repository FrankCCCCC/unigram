class Recorder:
    def __init__(self):
        self.history_dict = {}

    def add(self, name: str, step: int, val):
        if isinstance(val, torch.Tensor):
            val = float(val.detach().cpu())
        else:
            val = float(val)
        self.history_dict.setdefault(name, []).append((int(step), val))

    def get_items(self, name: str):
        return self.history_dict.get(name, [])

    def get_series(self, name: str):
        items = self.get_items(name)
        if not items:
            return [], []
        steps, values = zip(*items)
        return list(steps), list(values)

    def last_step(self, name: str):
        items = self.get_items(name)
        if not items:
            return 0
        return int(items[-1][0])

    def get_keys(self):
        return self.history_dict.keys()

    def to_dict(self):
        return {
            name: [
                {"step": int(step), "value": float(value)}
                for step, value in items
            ]
            for name, items in self.history_dict.items()
        }

    def save(self, file):
        file = Path(file)
        file.parent.mkdir(parents=True, exist_ok=True)
        with file.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
        return file

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