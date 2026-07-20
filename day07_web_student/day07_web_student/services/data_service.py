from pathlib import Path

import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def load_dashboard_data(base_dir: Path, selected_category: str = "全部") -> dict:
    data_dir = base_dir / "data"
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    category_df = _read_csv(data_dir / "category_analysis.csv")
    segment_df = _read_csv(data_dir / "segment_analysis.csv")

    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))

    # TOD 2-1：在已有两张指标卡基础上，增加“总体流失率”和“平均订单数”。
    metrics = [
        {"label": "总用户数", "value": f"{int(metric_map['用户数']):,}", "note": "人"},
        {"label": "流失用户", "value": f"{int(metric_map['流失人数']):,}", "note": "人"},
        {"label": "总体流失率", "value": f"{metric_map['流失率']:.1%}", "note": "占比"},
        {"label": "平均订单数", "value": f"{metric_map['平均订单数']:.2f}", "note": "单/人"},
    ]

    categories = ["全部", *category_df["PreferedOrderCat"].tolist()]
    table_df = category_df.copy()
    # TOD 3-1：选择具体品类后筛选table_df。
    # 教师参考项目中使用布尔条件筛选。
    if selected_category != "全部":
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

    # TOD 2-2：找出流失率最高的生命周期阶段，并生成一句数据观察。
    risk_row = segment_df.loc[segment_df["流失率"].idxmax()]
    insight = (
        f"生命周期风险最高的阶段是「{risk_row['TenureGroup']}」，"
        f"流失率高达 {risk_row['流失率']:.1%}，"
        f"远高于总体流失率 {metric_map['流失率']:.1%}，"
        f"说明新用户留存是当前最需关注的环节。"
    )

    return {
        "metrics": metrics,
        "categories": categories,
        "category_rows": table_df.to_dict("records"),
        "insight": insight,
    }


def filter_category_export(base_dir: Path, selected_category: str = "全部") -> pd.DataFrame:
    """拓展 A：导出与当前筛选一致的品类数据，复用已有的筛选逻辑。"""
    data_dir = base_dir / "data"
    category_df = _read_csv(data_dir / "category_analysis.csv")
    if selected_category != "全部":
        category_df = category_df[category_df["PreferedOrderCat"] == selected_category]
    return category_df
