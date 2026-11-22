
import re

# Define titles to remove from contact names
TITLES = {"dr", "mr", "mrs", "ms", "miss", "prof"}

def normalize_phone(raw):
    """
    '+91 98765-43210', '09876543210', '91 9876543210'
    -> '9876543210'.

    Returns None when fewer than 10 digits are present.
    """
    digits = re.sub(r"\D", "", raw or "")

    if len(digits) < 10:
        return None

    return digits[-10:]


def normalize_name(raw):
    """
    'Dr. Ravi' -> 'ravi'
    '  RAVI   Kumar ' -> 'ravi kumar'
    """
    words = re.findall(r"[a-z0-9]+", (raw or "").lower())

    return " ".join(
        word for word in words if word not in TITLES
    )


def merge_contacts(contacts):
    """
    contacts: list of dictionaries {name, phones[], emails[]}

    Returns a list of merged dictionaries:
    {names: set, phones: set, emails: set, sources: int}
    """

    n = len(contacts)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # Path compression
            x = parent[x]

        return x

    def union(a, b):
        ra, rb = find(a), find(b)

        if ra != rb:
            parent[rb] = ra

    # Normalized copy of every contact
    norm = []

    for c in contacts:
        phones = {
            p for p in map(normalize_phone, c.get("phones", [])) if p
        }

        emails = {
            e for e in map(normalize_email, c.get("emails", [])) if e
        }

        norm.append(
            (normalize_name(c.get("name", "")), phones, emails)
        )

    # Track phone and email ownership
    owner = {}
    email_owner = {}

    for i, (name, phones, emails) in enumerate(norm):

        for p in phones:
            if p in owner:
                union(i, owner[p])
            else:
                owner[p] = i

        if phones:
            for e in emails:
                email_owner.setdefault(e, i)

    # Process contacts without phone numbers
    for i, (name, phones, emails) in enumerate(norm):

        if not phones:
            for e in emails:
                if e in email_owner:
                    union(i, email_owner[e])
                else:
                    email_owner[e] = i

    # Merge contacts into groups
    groups = {}

    for i, (name, phones, emails) in enumerate(norm):

        g = groups.setdefault(
            find(i),
            {
                "names": set(),
                "phones": set(),
                "emails": set(),
                "sources": 0
            }
        )

        if name:
            g["names"].add(name)

        g["phones"] |= phones
        g["emails"] |= emails
        g["sources"] += 1

    return list(groups.values())
