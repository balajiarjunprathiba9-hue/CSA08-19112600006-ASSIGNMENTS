
# TASK 6 - COLLEGE FEST REGISTRATION DESK
# Name: ARJUN A B
# Reg No: 1911260006

import tempfile
import shutil
from pathlib import Path
from collections import Counter


# 1. CUSTOM EXCEPTIONS

class RegistrationError(Exception):
    kind = "error"


class DamagedLine(RegistrationError):
    kind = "damaged line"


class InvalidEmail(RegistrationError):
    kind = "invalid e-mail"


class DuplicateRegistration(RegistrationError):
    kind = "duplicate"


# 2. READER MODULE

def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            text = line.strip()
            if text:
                yield line_no, text


# 3. VALIDATOR MODULE

def is_valid_email(email):
    if email == "" or " " in email or email.count("@") != 1:
        return False

    local, domain = email.split("@")

    if local == "" or domain == "":
        return False

    if ("." not in domain or domain.startswith(".")
            or domain.endswith(".") or ".." in domain):
        return False

    return True


def validate_line(text):
    parts = [p.strip() for p in text.split(",")]

    if len(parts) != 5:
        raise DamagedLine(
            f"expected 5 fields, found {len(parts)}"
        )

    reg, name, dept, email, events_text = parts

    if not (reg.isdigit() and len(reg) == 9):
        raise DamagedLine(f"invalid register number '{reg}'")

    if name == "" or dept == "":
        raise DamagedLine("name or department is empty")

    if not is_valid_email(email):
        raise InvalidEmail(f"invalid e-mail '{email}'")

    events = []

    for item in events_text.split(";"):
        item = item.strip().title()

        if item and item not in events:
            events.append(item)

    if not events:
        raise DamagedLine("no events chosen")

    return {
        "reg": reg,
        "name": name.title(),
        "dept": dept.upper(),
        "email": email.lower(),
        "events": events
    }


# 4. PROCESSOR MODULE

def collect(paths):
    master = {}
    seen = set()
    errors = []

    stats = {
        "files_found": 0,
        "files_missing": 0,
        "lines_read": 0
    }

    for path in paths:
        try:
            for line_no, text in read_lines(path):
                stats["lines_read"] += 1

                try:
                    record = validate_line(text)

                    if record["reg"] in seen:
                        raise DuplicateRegistration(
                            f"register number {record['reg']} "
                            "already registered"
                        )

                except RegistrationError as err:
                    errors.append((
                        err.kind, path.name, line_no,
                        str(err), text
                    ))
                    continue

                seen.add(record["reg"])
                master[record["reg"]] = record

            stats["files_found"] += 1

        except FileNotFoundError:
            stats["files_missing"] += 1
            errors.append((
                "missing file", path.name, 0,
                "department file not found", ""
            ))

        except PermissionError:
            errors.append((
                "unreadable file", path.name, 0,
                "permission denied", ""
            ))

        except UnicodeDecodeError:
            errors.append((
                "unreadable file", path.name, 0,
                "file is not valid UTF-8", ""
            ))

    return master, errors, stats


# 5. WRITER MODULE

def write_master(master, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        f.write("reg_no,name,department,email,events\n")

        for r in master.values():
            f.write(
                f"{r['reg']},{r['name']},{r['dept']},"
                f"{r['email']},{';'.join(r['events'])}\n"
            )


def write_event_files(master, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    by_event = {}

    for r in master.values():
        for event in r["events"]:
            by_event.setdefault(event, []).append(r)

    for event, people in by_event.items():
        filename = event.replace(" ", "_") + ".txt"

        with (folder / filename).open("w", encoding="utf-8") as f:
            f.write(
                f"Participants of {event} ({len(people)})\n"
            )

            for r in people:
                f.write(
                    f"{r['reg']} {r['name']} ({r['dept']})\n"
                )


def write_error_log(errors, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        for kind, name, line_no, message, text in errors:
            f.write(
                f"[{kind}] {name}:{line_no} - "
                f"{message} | {text}\n"
            )


def write_summary(master, errors, stats, path):
    by_dept = Counter(
        r["dept"] for r in master.values()
    )

    by_event = Counter(
        e for r in master.values() for e in r["events"]
    )

    by_kind = Counter(e[0] for e in errors)

    with Path(path).open("w", encoding="utf-8") as f:
        f.write("COLLEGE FEST - SUMMARY REPORT\n")

        f.write(
            f"Department files read      : {stats['files_found']}\n"
        )

        f.write(
            f"Department files missing   : {stats['files_missing']}\n"
        )

        f.write(
            f"Lines read                 : {stats['lines_read']}\n"
        )

        f.write(
            f"Valid unique registrations : {len(master)}\n"
        )

        for kind, n in sorted(by_kind.items()):
            f.write(f"Rejected - {kind:<16}: {n}\n")

        f.write(
            "Registrations by department: "
            + ", ".join(
                f"{d}={n}" for d, n in sorted(by_dept.items())
            ) + "\n"
        )

        f.write(
            "Participants by event      : "
            + ", ".join(
                f"{e}={n}" for e, n in sorted(by_event.items())
            ) + "\n"
        )


# 6. MAIN PACKAGE FUNCTION

def run(input_dir, output_dir, department_files):
    paths = [
        Path(input_dir) / name
        for name in department_files
    ]

    master, errors, stats = collect(paths)

    out = Path(output_dir)

    write_master(master, out / "master_list.csv")
    write_event_files(master, out / "events")
    write_error_log(errors, out / "error_log.txt")
    write_summary(master, errors, stats,
                  out / "summary_report.txt")

    return master, errors, stats


# 7. DEMONSTRATION

def main():
    work = Path(tempfile.mkdtemp())

    try:
        inp = work / "input"
        inp.mkdir()

        files = {
            "cse.txt": (
                "192311001,arun kumar,cse,arun@simats.edu,Dance;Singing\n"
                "192311002,bala s,cse,bala@simats.edu,Quiz\n"
                "192311001,Arun Kumar,CSE,arun@simats.edu,Drama\n"
                "192311003,Charan,CSE,charan@@simats.edu,Dance\n"
            ),

            "ece.txt": (
                "192312001,Divya R,ECE,divya@simats.edu,Singing; Drama\n"
                "192312002,Eswar\n"
                "192312003,Farhan,ECE,farhan@simats.edu,Quiz;quiz;Dance\n"
            ),

            "mech.txt": (
                "192313001,Gokul,MECH,gokul@simats.edu,Drama\n"
            ),

            "civil.txt": (
                "192314001,Harini,CIVIL,harini@simats.edu,Singing\n"
            )
        }

        for name, content in files.items():
            (inp / name).write_text(
                content, encoding="utf-8"
            )

        print("COLLEGE FEST REGISTRATION DESK")
        print("--------------------------------")

        print("Input files:", sorted(
            p.name for p in inp.iterdir()
        ))

        print("it.txt is intentionally missing.")

        master, errors, stats = run(
            inp,
            work / "output",
            ["cse.txt", "ece.txt", "mech.txt",
             "civil.txt", "it.txt"]
        )

        out = work / "output"

        print("\nProgram finished normally.\n")

        for name in [
            "master_list.csv",
            "error_log.txt",
            "summary_report.txt"
        ]:
            print(f"--- {name} ---")
            print(
                (out / name).read_text(encoding="utf-8"),
                end=""
            )

        print("\n--- EVENTS FOLDER ---")
        print(sorted(
            p.name for p in (out / "events").iterdir()
        ))

        print("\n--- DANCE PARTICIPANTS ---")
        print(
            (out / "events" / "Dance.txt").read_text(),
            end=""
        )

        print("\n--- SINGING PARTICIPANTS ---")
        print(
            (out / "events" / "Singing.txt").read_text(),
            end=""
        )

    finally:
        shutil.rmtree(work)


if __name__ == "__main__":
    main()
