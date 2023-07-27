import math
import numpy as np


class RecallAtK:
    def calculate(self, gt, results, k):
        relevant_items = len(gt)
        relevant_found = sum(1 for doc_id in results[:k] if doc_id in gt)
        return relevant_found / relevant_items


class AverageRecall_At_K:
    def __init__(self):
        self.recall_at_k = RecallAtK()

    def calculate(self, ground_truths, search_results, k):
        total_recall_at_k = 0.0

        for gt, results in zip(ground_truths, search_results):
            recall_at_k = self.recall_at_k.calculate(gt, results, k)
            total_recall_at_k += recall_at_k

        return total_recall_at_k / len(ground_truths)


class HitAtK:
    def calculate(self, gt, results, k):
        for doc_id in results[:k]:
            if doc_id in gt:
                return 1
        return 0


class AverageHit_At_K:
    def __init__(self):
        self.hit_at_k = HitAtK()

    def calculate(self, ground_truths, search_results, k):
        total_hit_at_k = 0.0

        for gt, results in zip(ground_truths, search_results):
            hit_at_k = self.hit_at_k.calculate(gt, results, k)
            total_hit_at_k += hit_at_k

        return total_hit_at_k / len(ground_truths)


class PrecisionAtK:
    def calculate(self, gt, results, k):
        relevant_found = sum(1 for doc_id in results[:k] if doc_id in gt)
        return relevant_found / k


class AveragePrecision_At_K:
    def __init__(self):
        self.precision_at_k = PrecisionAtK()

    def calculate(self, ground_truths, search_results, k):
        total_precision_at_k = 0.0

        for gt, results in zip(ground_truths, search_results):
            precision_at_k = self.precision_at_k.calculate(gt, results, k)
            total_precision_at_k += precision_at_k

        return total_precision_at_k / len(ground_truths)



# Example usage
ground_truths = [
    ["doc1", "doc3", "doc5"],
    ["doc4"],
    ["doc2", "doc3", "doc5"],
    ["doc1", "doc4", "doc5"],
    ["doc1", "doc2", "doc3", "doc4", "doc5"],
]

search_results = [
    ["doc2", "doc1", "doc5", "doc3", "doc4"],
    ["doc1", "doc2", "doc3", "doc4", "doc5"],
    ["doc1", "doc3", "doc2", "doc4", "doc5"],
    ["doc2", "doc1", "doc4", "doc5", "doc3"],
    ["doc3", "doc1", "doc2", "doc4", "doc5"],
]

K = 5


recall_at_k = AverageRecall_At_K()
hit_at_k = AverageHit_At_K()
precision_at_k = AveragePrecision_At_K()

recall_score = recall_at_k.calculate(ground_truths, search_results, K)
hit_score = hit_at_k.calculate(ground_truths, search_results, K)
precision_score = precision_at_k.calculate(ground_truths, search_results, K)

print(f"Recall@{K}: {recall_score:.4f}")
print(f"Hit@{K}: {hit_score:.4f}")
print(f"Precision@{K}: {precision_score:.4f}")
# print(f"NDCG@{K}: {np.mean(ndcg_score):.4f}")
