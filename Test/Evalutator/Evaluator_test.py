from Evaluate.Performance_Evaluator import AverageRecall_At_K, AverageHit_At_K, AveragePrecision_At_K


# receive the list of ground truth and search results
# calculate the average recall@k, average hit@k, average precision@k
# return the average recall@k, average hit@k, average precision@k

K=10
def PerformanceEvaluator(ground_truths, search_results):
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