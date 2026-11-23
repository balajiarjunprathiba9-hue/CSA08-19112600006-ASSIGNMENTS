
import re

# Define titles to remove from contact names
TITLES = {"dr", "mr", "mrs", "ms", "miss", "prof"}


# Normalize phone numbers
def normalize_phone(raw):
    digits = re.sub(r"\D", "", raw or "")

    if len(digits) < 10:
        return None

    return digits[-10:]


# Normalize names
def normalize_name(raw):
    words = re.findall(r"[a-z0-9]+", (raw or "").lower())

    return " ".join(
        word for word in words if word not in TITLES
    )


# Normalize email addresses
def normalize_email(raw):
    return (raw or "").strip().lower()


# Merge duplicate contacts
def merge_contacts(contacts):

    n = len(contacts)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]

        return x

    def union(a, b):
        ra, rb = find(a), find(b)

        if ra != rb:
            parent[rb] = ra

    # Normalize all contacts
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

        root = find(i)

        g = groups.setdefault(
            root,
            {
                "names": set(),
                "phones": set(),
                "emails": set(),
                "sources": 0
            }
        )

        if name:
            g["names"].add(name)

        g["phones"].update(phones)
        g["emails"].update(emails)
        g["sources"] += 1

    return list(groups.values())


# ==========================================
# SAMPLE INPUT
# ==========================================

contacts = [
    {
        "name": "Dr. Ravi Kumar",
        "phones": ["+91 98765-43210"],
        "emails": ["RAVI@gmail.com"]
    },
    {
        "name": "Ravi Kumar",
        "phones": ["9876543210"],
        "emails": ["ravi@gmail.com"]
    },
    {
        "name": "Mr. Arun",
        "phones": ["9876543211"],
        "emails": ["arun@gmail.com"]
    },
    {
        "name": "Arun",
        "phones": [],
        "emails": ["arun@gmail.com"]
    }
]


# ==========================================
# DISPLAY FINAL RESULT
# ==========================================

result = merge_contacts(contacts)

print("========== MERGED CONTACTS ==========")

for i, contact in enumerate(result, start=1):

    print("\nContact", i)
    print("Names:", sorted(contact["names"]))
    print("Phones:", sorted(contact["phones"]))
    print("Emails:", sorted(contact["emails"]))
    print("Sources:", contact["sources"])

print("\nContact merging completed successfully!")
