import sys
import sacrebleu

def sentence_chrf(reference, hypothesis):
    """Compute chrF++ score for a single sentence pair."""
    return sacrebleu.sentence_chrf(hypothesis, [reference])

def explain(chrf_score):
    """Explain chrF++ score based on updated interpretation table."""
    if chrf_score >= 95:
        return "Perfect / near-perfect"
    elif chrf_score >= 80:
        return "Very high similarity"
    elif chrf_score >= 60:
        return "High similarity"
    elif chrf_score >= 40:
        return "Moderate"
    elif chrf_score >= 20:
        return "Low"
    else:
        return "Very low"


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 compare.py input1 input2 output")
        sys.exit(1)

    ref_path = sys.argv[1]
    hyp_path = sys.argv[2]
    out_path = sys.argv[3]

    with open(ref_path, 'r', encoding='utf-8') as f:
        references = [line.strip() for line in f if line.strip()]
        print(references)

    with open(hyp_path, 'r', encoding='utf-8') as f:
        hypotheses = [line.strip() for line in f if line.strip()]

    if len(references) != len(hypotheses):
        print("Error: Number of lines in input1 and input2 must be the same.")
        sys.exit(1)

    # Compute overall chrF++
    total_chrf = sacrebleu.corpus_chrf(hypotheses, [references])

    # Write results
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(f"Overall chrF++ score: {total_chrf.score:.2f}\n")
        out.write("="*50 + "\n")

        for i, (ref, hyp) in enumerate(zip(references, hypotheses), 1):
            chrf = sentence_chrf(ref, hyp)
            explanation = explain(chrf.score)
            out.write(f"Sentence {i}:\n")
            out.write(f"Reference  : {ref}\n")
            out.write(f"Hypothesis : {hyp}\n")
            out.write(f"chrF++ Score : {chrf.score:.2f}\n")
            out.write(f"Explanation : {explanation}\n")
            out.write("-" * 50 + "\n")

    print(f"Detailed chrF++ results written to {out_path}")

if __name__ == "__main__":
    main()
