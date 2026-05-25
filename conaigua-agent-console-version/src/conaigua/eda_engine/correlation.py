import pandas as pd
from scipy import stats

def compute_correlations(df, var1: str, var2: str) -> dict:
    data = df[[var1, var2]].dropna()
    s1 = data[var1]
    s2 = data[var2]

    pearson_r, pearson_p = stats.pearsonr(s1, s2)
    spearman_r, spearman_p = stats.spearmanr(s1, s2)

    return {
        "var1": var1,
        "var2": var2,
        "n_obs": len(data),
        "pearson": {
            "r": round(float(pearson_r), 4),
            "p_value": round(float(pearson_p), 4),
            "significativo": bool(pearson_p < 0.05)
        },
        "spearman": {
            "r": round(float(spearman_r), 4),
            "p_value": round(float(spearman_p), 4),
            "significativo": bool(spearman_p < 0.05)
        }
    }