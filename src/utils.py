import pandas as pd
from rouge_score import rouge_scorer

def calculate_rouge(reference, hypothesis):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return {
        "rouge1": scores['rouge1'].fmeasure,
        "rougeL": scores['rougeL'].fmeasure
    }

def load_processed_data():
    train_data = pd.read_csv("data/processed/train_data.csv")
    test_data = pd.read_csv("data/processed/test_data.csv")
    return train_data, test_data

if __name__ == "__main__":
    # Test hàm tính ROUGE
    ref = "Năng lượng mặt trời giúp giảm ô nhiễm và tiết kiệm chi phí."
    hyp = "Năng lượng mặt trời giúp giảm ô nhiễm và tiết kiệm chi phí điện."
    print(calculate_rouge(ref, hyp))