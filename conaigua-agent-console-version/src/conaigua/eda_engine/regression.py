import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

def _diagnostico(r2: float, p_value: float = None) -> str:
    if r2 >= 0.8:
        calidad = "ajuste excelente"
    elif r2 >= 0.5:
        calidad = "ajuste moderado"
    else:
        calidad = "ajuste débil"
    if p_value is not None:
        sig = "estadísticamente significativo" if p_value < 0.05 else "no significativo"
        return f"{calidad}, modelo {sig} (p={round(p_value, 4)})"
    return calidad

def linear_regression(df, x_col: str, y_col: str) -> dict:
    data = df[[x_col, y_col]].dropna()
    x = data[x_col].values
    y = data[y_col].values
    n = len(y)

    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)
    y_pred = model.predict(x.reshape(-1, 1))

    residuals = y - y_pred
    se = np.sqrt(np.sum(residuals**2) / (n - 2))
    x_mean = x.mean()
    se_coef = se / np.sqrt(np.sum((x - x_mean)**2))
    t_critical = stats.t.ppf(0.975, df=n - 2)
    margin = t_critical * se_coef
    t_stat = float(model.coef_[0]) / se_coef
    p_value = float(2 * stats.t.sf(np.abs(t_stat), df=n - 2))

    return {
        "tipo": "lineal_simple",
        "variable_x": x_col,
        "variable_y": y_col,
        "n_obs": n,
        "intercepto": round(float(model.intercept_), 4),
        "pendiente": round(float(model.coef_[0]), 4),
        "intervalo_confianza_95": {
            "inferior": round(float(model.coef_[0]) - margin, 4),
            "superior": round(float(model.coef_[0]) + margin, 4)
        },
        "r2": round(float(r2_score(y, y_pred)), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(y, y_pred))), 4),
        "p_value": round(p_value, 4),
        "significativo": bool(p_value < 0.05),
        "diagnostico": _diagnostico(float(r2_score(y, y_pred)), p_value)
    }

def multiple_regression(df, x_cols: list, y_col: str) -> dict:
    data = df[x_cols + [y_col]].dropna()
    x = data[x_cols].values
    y = data[y_col].values
    n = len(y)
    p = len(x_cols)

    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)

    coeficientes = {
        col: round(float(coef), 4)
        for col, coef in zip(x_cols, model.coef_)
    }

    return {
        "tipo": "lineal_multiple",
        "variables_x": x_cols,
        "variable_y": y_col,
        "n_obs": n,
        "intercepto": round(float(model.intercept_), 4),
        "coeficientes": coeficientes,
        "r2": round(float(r2_score(y, y_pred)), 4),
        "r2_ajustado": round(
            float(1 - (1 - r2_score(y, y_pred)) * (n - 1) / (n - p - 1)), 4
        ),
        "rmse": round(float(np.sqrt(mean_squared_error(y, y_pred))), 4),
        "diagnostico": _diagnostico(float(r2_score(y, y_pred)))
    }