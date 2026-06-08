import re
def find_best_matches(text: str, dictionary: list):
    lookup = {d["match"]: d["canonical"] for d in dictionary}

    results = []

    for line in text.split("\n"):
        words = re.findall(r"\w+", line.lower())

        best_match = None
        best_span = None
        best_len = 0

        n = len(words)

        for i in range(n):
            for j in range(i + 1, min(n + 6, n + 1)):
                phrase = " ".join(words[i:j])

                if phrase in lookup:
                    span_len = j - i
                    if span_len > best_len:
                        best_match = lookup[phrase]
                        best_span = [i, j]
                        best_len = span_len

        results.append({
            "line": line,
            "match": best_match,
            "span": best_span
        })

    return results