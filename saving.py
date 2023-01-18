import json
import threading
from typing import Callable, ParamSpec, TypeVar, Union

from config import new_location, watching_location

ProcessingType = dict[str, dict[str, bool]]
LockType = Union[threading.RLock, threading.RLock]


class Processing(ProcessingType):
    def __init__(self) -> None:
        self.lock = threading.RLock()

    def __str__(self) -> str:
        with self.lock:
            return json.dumps(self)

    def __repr__(self) -> str:
        return str(self)


T = TypeVar('T')
P = ParamSpec('P')


def with_processing(processing: Processing):
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        def f(*args: P.args, **kwargs: P.kwargs):
            with processing.lock:
                return func(*args, **kwargs)
        return f
    return decorator


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
            if id_ in watching and names[id_] == name:
                continue
            changed = True
            watching[id_] = watching.get(id_, [])
            if len(name) > 0:
                names[id_] = name
    return changed


def save_watching(watching: dict[str, list[str]], names: dict[str, str]):
    with open(watching_location, "w") as f:
        for anime in watching:
            f.write(anime + " " + ",".join(watching[anime]))
            if (anime in names):
                f.write(" | " + names[anime])
            f.write("\n")


def update_processing(processing: Processing, watching: dict[str, list[str]]) -> bool:
    changed = False
    with processing.lock:
        idsToDelete: list[str] = []
        for id_ in watching:
            if id_ in processing:
                if len(processing[id_]) > 0:
                    watching[id_] = watching[id_] + \
                        [k for k, v in processing[id_].items() if v]
                processing[id_] = {k: v for k,
                                   v in processing[id_].items() if not v}
                if len(processing[id_]) == 0:
                    idsToDelete.append(id_)
                changed = True

        for id_ in idsToDelete:
            del processing[id_]
    return changed


def get_watching(names: dict[str, str], processing: Processing) -> dict[str, list[str]]:
    watching, new_names = parse_watching()
    names.update(new_names)

    changed = update_processing(processing, watching)

    changed = parse_new(watching, names) or changed

    if changed:
        save_watching(watching, names)
    return watching
