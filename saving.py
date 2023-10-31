import json
import threading
from typing import Callable, Concatenate, ParamSpec, TypeVar, Union

from config import new_location, watching_location
from episode import episode_order

ProcessingType = dict[str, dict[str, bool]]
LockType = Union[threading.RLock, threading.RLock]

T = TypeVar("T")
P = ParamSpec("P")


class Processing(ProcessingType):
    def __init__(self) -> None:
        self._lock = threading.RLock()

    def __str__(self) -> str:
        with self._lock:
            return json.dumps(self)

    def start(self, anime: str, ep: str):
        with self._lock:
            tmp = self.get(anime, {})
            tmp[ep] = True
            self[anime] = tmp

    def finish(self, anime: str, ep: str, success: bool):
        with self._lock:
            if not anime in self or ep not in self[anime]:
                return
            tmp = {k: v for k, v in self[anime].items()}
            if success:
                tmp[ep] = False
            else:
                del tmp[ep]
            self[anime] = tmp

    def update_processed(self, anime: str) -> list[str]:
        processed_eps = []
        with self._lock:
            ids_to_delete: list[str] = []
            if anime in self:
                if len(self[anime]) > 0:
                    processed_eps = [k for k, v in self[anime].items() if not v]
                self[anime] = {k: v for k, v in self[anime].items() if v}
                if len(self[anime]) == 0:
                    ids_to_delete.append(anime)

            for anime in ids_to_delete:
                del self[anime]
        return processed_eps

    def get_eps(self, anime: str) -> list[str]:
        return list(self.get(anime, {}))

    def with_lock(
        self, func: Callable[Concatenate["Processing", P], T]
    ) -> Callable[P, T]:
        def f(*args: P.args, **kwargs: P.kwargs) -> T:
            with self._lock:
                return func(self, *args, **kwargs)

        return f

    def __repr__(self) -> str:
        return str(self)


def parse_watching() -> tuple[dict[str, list[str]], dict[str, str]]:
    watching: dict[str, list[str]] = {}
    names: dict[str, str] = {}
    with open(watching_location, "r") as f:
        s = f.read()
        for line in s.split("\n"):
            watch, *name = line.split("|")
            anime = watch.strip()
            if anime == "":
                continue
            id_, *epleft = anime.split(" ")
            if len(name) > 0:
                names[id_] = name[0].strip()

            ep = (" ".join(epleft)).split(",")
            if ep == [""]:
                ep = []
            watching[id_] = ep
    return watching, names


def parse_new(watching: dict[str, list[str]], names: dict[str, str]) -> bool:
    changed = False
    with open(new_location, "r") as f:
        s = f.read()
        for line in s.split("\n"):
            id_, *name = line.split("|")
            if len(name) > 0:
                name = name[0].strip()
            else:
                continue
            id_ = id_.strip()
            if id_ == "":
                continue
            if id_ in watching and names.get(id_, "") == name:
                continue
            changed = True
            watching[id_] = watching.get(id_, [])
            if len(name) > 0:
                names[id_] = name
    return changed


def save_watching(watching: dict[str, list[str]], names: dict[str, str]):
    with open(watching_location, "w") as f:
        for anime in watching:
            f.write(anime + " " + ",".join(sorted(watching[anime], key=episode_order)))
            if anime in names:
                f.write(" | " + names[anime])
            f.write("\n")


def get_watching(names: dict[str, str], processing: Processing) -> dict[str, list[str]]:
    watching, new_names = parse_watching()
    names.update(new_names)

    changed = False
    for anime_id in watching:
        processed_eps = processing.update_processed(anime_id)
        if len(processed_eps) > 0:
            changed = True
        watching[anime_id].extend(processed_eps)

    changed = parse_new(watching, names) or changed

    if changed:
        save_watching(watching, names)
    return watching
