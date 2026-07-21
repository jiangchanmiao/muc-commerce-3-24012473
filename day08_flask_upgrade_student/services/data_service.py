from pathlib import Path

import numpy as np
import pandas as pd


def _to_serializable(obj):
    """递归把 numpy/pandas 类型转成普通 Python 值，保证 jsonify 能序列化。"""
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_serializable(v) for v in obj]
    return obj


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def load_dashboard_data(base_dir: Path, selected_category: str = "全部") -> dict:
    data_dir = base_dir / "data"
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    category_df = _read_csv(data_dir / "category_analysis.csv")
    segment_df = _read_csv(data_dir / "segment_analysis.csv")

    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    metrics = [
        {"label": "总用户数", "value": f"{int(metric_map['用户数']):,}", "note": "人"},
        {"label": "流失用户", "value": f"{int(metric_map['流失人数']):,}", "note": "人"},
        {"label": "总体流失率", "value": f"{metric_map['流失率']:.1%}", "note": "用户占比"},
        {"label": "平均订单数", "value": f"{metric_map['平均订单数']:.2f}", "note": "单/人"},
    ]

    categories = ["全部", *category_df["PreferedOrderCat"].tolist()]
    table_df = category_df.copy()
    if selected_category != "全部" and selected_category in categories:
        table_df = table_df[table_df["PreferedOrderCat"] == selected_category]

    table_df = table_df.rename(
        columns={
            "PreferedOrderCat": "偏好品类",
            "用户数": "用户数",
            "流失率": "流失率",
            "平均订单数": "平均订单数",
        }
    )[["偏好品类", "用户数", "流失率", "平均订单数"]]
    table_df["流失率"] = table_df["流失率"].map(lambda value: f"{value:.1%}")
    table_df["平均订单数"] = table_df["平均订单数"].map(lambda value: f"{value:.2f}")

    highest_risk = segment_df.loc[segment_df["流失率"].idxmax()]
    insight = (
        f"{highest_risk['TenureGroup']}的流失率最高，为{highest_risk['流失率']:.1%}。"
        "这是一项描述性观察，不能直接解释流失原因。"
    )

    return {
        "metrics": metrics,
        "categories": categories,
        "category_rows": table_df.to_dict("records"),
        "insight": insight,
    }


def load_metric_api_data(base_dir: Path) -> list[dict]:
    """返回给JSON接口使用的指标卡数据。"""
    data = load_dashboard_data(base_dir)
   # TOD 8-4：确保接口返回可被jsonify序列化的普通Python值。
    data["metrics"] = _to_serializable(data["metrics"])
    return data["metrics"]


def load_category_api_data(base_dir: Path, selected_category: str = "全部") -> list[dict]:
    """返回给JSON接口使用的筛选表格数据。"""
    data = load_dashboard_data(base_dir, selected_category)
    data["category_rows"] = _to_serializable(data["category_rows"])
    return data["category_rows"]
