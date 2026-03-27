import re
from io import StringIO
import matplotlib.pyplot as plt


RAW_TEXT_1 = """
test all algorithms
algorithm: BFS
tiles path: [1, 6, 3, 5, 4, 0, 1, 6, 4, 2, 7, 0, 1, 6, 4, 5, 3, 6, 1]
length: 19
expanded: 24826
algorithm: manhattan
tiles path: [1, 6, 3, 5, 4, 0, 1, 6, 4, 2, 7, 0, 1, 6, 4, 5, 3, 6, 1]
length: 19
expanded: 334
algorithm: misplaced
tiles path: [1, 6, 3, 5, 4, 0, 1, 6, 4, 2, 7, 0, 1, 6, 4, 5, 3, 6, 1]
length: 19
expanded: 2334
algorithm: rowcol
tiles path: [1, 6, 3, 5, 4, 0, 1, 6, 4, 2, 7, 0, 1, 6, 4, 5, 3, 6, 1]
length: 19
expanded: 649
algorithm: wrongneighbors
tiles path: [1, 6, 3, 5, 4, 0, 1, 6, 4, 2, 7, 0, 1, 6, 4, 5, 3, 6, 1]
length: 19
expanded: 761
algorithm: max_rowcol_wneighbors
tiles path: [1, 6, 3, 5, 4, 0, 1, 6, 4, 2, 7, 0, 1, 6, 4, 5, 3, 6, 1]
length: 19
expanded: 761
algorithm: max_man_wneighbors
tiles path: [1, 6, 3, 5, 4, 0, 1, 6, 4, 2, 7, 0, 1, 6, 4, 5, 3, 6, 1]
length: 19
expanded: 761
algorithm: max_misp_wneighbors
tiles path: [1, 6, 3, 5, 4, 0, 1, 6, 4, 2, 7, 0, 1, 6, 4, 5, 3, 6, 1]
length: 19
expanded: 761
algorithm: max_misp_man
tiles path: [1, 6, 3, 5, 4, 0, 1, 6, 4, 2, 7, 0, 1, 6, 4, 5, 3, 6, 1]
length: 19
expanded: 334
algorithm: max_rowcol_man
tiles path: [1, 6, 3, 5, 4, 0, 1, 6, 4, 2, 7, 0, 1, 6, 4, 5, 3, 6, 1]
length: 19
expanded: 334
"""

RAW_TEXT_2 = """
test all algorithms
algorithm: BFS
tiles path: [3, 2, 7, 5, 1, 8, 4, 5, 3, 0, 1, 5, 7, 6, 4, 8, 1, 5, 3, 2, 7, 5, 4, 6]
length: 24
expanded: 96572
algorithm: manhattan
tiles path: [3, 2, 7, 5, 1, 8, 4, 5, 3, 0, 1, 5, 7, 6, 4, 8, 1, 5, 3, 2, 7, 5, 4, 6]
length: 24
expanded: 1173
algorithm: misplaced
tiles path: [3, 2, 7, 5, 1, 8, 4, 5, 3, 0, 1, 5, 7, 6, 4, 8, 1, 5, 3, 2, 7, 5, 4, 6]
length: 24
expanded: 17252
algorithm: rowcol
tiles path: [3, 2, 7, 5, 1, 8, 4, 5, 3, 0, 1, 5, 7, 6, 4, 8, 1, 5, 3, 2, 7, 5, 4, 6]
length: 24
expanded: 4062
algorithm: wrongneighbors
tiles path: [1, 8, 4, 5, 3, 2, 7, 5, 3, 0, 1, 5, 4, 8, 1, 5, 7, 6, 4, 5, 3, 2, 7, 6, 4, 5, 7, 6]
length: 28
expanded: 7187
algorithm: max_rowcol_wneighbors
tiles path: [1, 8, 4, 5, 3, 2, 7, 5, 3, 0, 1, 5, 4, 8, 1, 5, 7, 6, 4, 5, 3, 2, 7, 6, 4, 5, 7, 6]
length: 28
expanded: 7187
algorithm: max_man_wneighbors
tiles path: [1, 8, 4, 5, 3, 2, 7, 5, 3, 0, 1, 5, 4, 8, 1, 5, 7, 6, 4, 5, 3, 2, 7, 6, 4, 5, 7, 6]
length: 28
expanded: 7187
algorithm: max_misp_wneighbors
tiles path: [1, 8, 4, 5, 3, 2, 7, 5, 3, 0, 1, 5, 4, 8, 1, 5, 7, 6, 4, 5, 3, 2, 7, 6, 4, 5, 7, 6]
length: 28
expanded: 7187
algorithm: max_misp_man
tiles path: [3, 2, 7, 5, 1, 8, 4, 5, 3, 0, 1, 5, 7, 6, 4, 8, 1, 5, 3, 2, 7, 5, 4, 6]
length: 24
expanded: 1173
algorithm: max_rowcol_man
tiles path: [3, 2, 7, 5, 1, 8, 4, 5, 3, 0, 1, 5, 7, 6, 4, 8, 1, 5, 3, 2, 7, 5, 4, 6]
length: 24
expanded: 1173
"""

def parse_results(text: str):
    """
    Parse algorithm results from the raw text.
    Ignores 'tiles path' lines.
    Returns a list of dicts with keys: algorithm, length, expanded.
    """
    pattern = re.compile(
        r"algorithm:\s*(?P<algorithm>[^\n]+)\s+"
        r"(?:tiles path:\s*\[[^\]]*\]\s+)?"
        r"length:\s*(?P<length>\d+)\s+"
        r"expanded:\s*(?P<expanded>\d+)",
        re.MULTILINE,
    )

    results = []
    for match in pattern.finditer(text):
        results.append(
            {
                "algorithm": match.group("algorithm").strip(),
                "length": int(match.group("length")),
                "expanded": int(match.group("expanded")),
            }
        )

    return results


def plot_results(results):
    """
    Plot two sorted bar charts:
    1. solution length (ascending)
    2. expanded nodes (ascending)
    """

    # -------- Sort by length --------
    sorted_by_length = sorted(results, key=lambda r: r["length"])
    alg_len = [r["algorithm"] for r in sorted_by_length]
    lengths = [r["length"] for r in sorted_by_length]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(alg_len, lengths)
    plt.title("Solution Length by Algorithm (sorted)")
    plt.xlabel("Algorithm")
    plt.ylabel("Length")
    plt.xticks(rotation=30, ha="right")


    for bar, value in zip(bars, lengths):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.show()

    # -------- Sort by expanded nodes --------
    sorted_by_expanded = sorted(results, key=lambda r: r["expanded"])
    alg_exp = [r["algorithm"] for r in sorted_by_expanded]
    expanded = [r["expanded"] for r in sorted_by_expanded]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(alg_exp, expanded)
    plt.title("Expanded Nodes by Algorithm (sorted)")
    plt.xlabel("Algorithm")
    plt.ylabel("Expanded Nodes")
    plt.xticks(rotation=30, ha="right")
    plt.yscale("log")

    for bar, value in zip(bars, expanded):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.show()


def main():
    for text in [RAW_TEXT_1, RAW_TEXT_2]:
        results = parse_results(text)
        plot_results(results)


if __name__ == "__main__":
    main()