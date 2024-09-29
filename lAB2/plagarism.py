import heapq

def levenshtein_distance(str1, str2):
    if len(str1) < len(str2):
        return levenshtein_distance(str2, str1)
    if len(str2) == 0:
        return len(str1)

    prev_row = list(range(len(str2) + 1))

    for i, c1 in enumerate(str1):
        curr_row = [i + 1]
        for j, c2 in enumerate(str2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row

    return prev_row[-1]

def a_star_search(doc1_sentences, doc2_sentences):
    total_cost = 0
    max_length = max(len(doc1_sentences), len(doc2_sentences))

    for i in range(max_length):
        str1 = doc1_sentences[i].strip() if i < len(doc1_sentences) else ""
        str2 = doc2_sentences[i].strip() if i < len(doc2_sentences) else ""
        total_cost += levenshtein_distance(str1, str2)

    return total_cost

def plagiarism(doc1, doc2):
    doc1_sentences = [sentence.strip() for sentence in doc1.split('.') if sentence.strip()]
    doc2_sentences = [sentence.strip() for sentence in doc2.split('.') if sentence.strip()]
    total_cost = a_star_search(doc1_sentences, doc2_sentences)
    return total_cost

def main(file_pairs):
    for file1, file2 in file_pairs:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            doc1 = f1.read()
            doc2 = f2.read()
        total_cost = plagiarism(doc1, doc2)
        print(f"Total cost for {file1} and {file2}: {total_cost}")

if __name__ == "__main__":
    file_pairs = [
        ('doc1_identical.txt', 'doc2_identical.txt'),
        ('doc1_modified.txt', 'doc2_modified.txt'),
        ('doc1_diff.txt', 'doc2_diff.txt'),
        ('doc1_partialoverlap.txt', 'doc2_partialoverlap.txt'),
    ]
    main(file_pairs)
