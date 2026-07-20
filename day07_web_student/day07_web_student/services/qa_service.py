from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")

    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户", "多少名"]):
        return f"数据集中共有 {int(metrics['用户数']):,} 名用户。"

    # TOD 4-1：补充“流失率”“偏好品类”“生命周期风险”和“订单”四类问答。
    # 每个回答都必须引用 data 目录中已经计算的指标，不得编造数值。

    # 流失率
    if "流失率" in normalized or "流失" in normalized:
        return (
            f"总体流失率为 {metrics['流失率']:.1%}，"
            f"对应流失人数为 {int(metrics['流失人数']):,} 人"
            f"（总用户 {int(metrics['用户数']):,} 人）。"
        )

    # 偏好品类
    if "品类" in normalized or "类别" in normalized or "category" in normalized:
        top_users = category_df.loc[category_df["用户数"].idxmax()]
        top_churn = category_df.loc[category_df["流失率"].idxmax()]
        return (
            f"用户数最多的偏好品类是「{top_users['PreferedOrderCat']}」，共 {int(top_users['用户数']):,} 人；"
            f"流失率最高的品类是「{top_churn['PreferedOrderCat']}」，达到 {top_churn['流失率']:.1%}。"
        )

    # 生命周期风险
    if "生命周期" in normalized or "阶段" in normalized or "风险" in normalized or "tenure" in normalized:
        risk_row = segment_df.loc[segment_df["流失率"].idxmax()]
        return (
            f"生命周期风险最高的阶段是「{risk_row['TenureGroup']}」，"
            f"流失率 {risk_row['流失率']:.1%}，"
            f"共 {int(risk_row['用户数']):,} 名用户。"
        )

    # 订单
    if "订单" in normalized or "下单" in normalized or "order" in normalized:
        return (
            f"用户平均订单数为 {metrics['平均订单数']:.2f} 单/人，"
            f"订单数中位数为 {int(metrics['订单数中位数'])} 单。"
        )

    return (
        "基础问答尚未完成。目前只能回答总用户数；请继续完成TOO 4-1。"
        "请换一种更具体的问法。"
    )
