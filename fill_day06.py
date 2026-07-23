"""Fill day06_pm_student_visualization.ipynb seed template with actual visualization code."""

import json

NB_PATH = "C:/Users/QH153/PyCharmMiscProject/day06_pm_student_visualization.ipynb"
OUT_PATH = "day06_pm_student_visualization.ipynb"

with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

# ---------------------------------------------------------------------------
# cell-2: fill STUDENT_ID and TOPIC
# ---------------------------------------------------------------------------
cells[2]["source"] = [
    'from pathlib import Path\n',
    'import pandas as pd\n',
    'import numpy as np\n',
    'import matplotlib.pyplot as plt\n',
    'from matplotlib.ticker import PercentFormatter\n',
    '\n',
    'try:\n',
    '    from IPython.display import display\n',
    'except ImportError:\n',
    '    def display(obj):\n',
    '        print(obj)\n',
    '\n',
    'STUDENT_ID = "曲浩24012473"\n',
    'TOPIC = "D"\n',
    '\n',
    'pd.set_option("display.max_columns", 50)\n',
    'pd.set_option("display.float_format", lambda x: f"{x:,.2f}")\n',
    'plt.rcParams["font.sans-serif"] = [\n',
    '    "Microsoft YaHei", "SimHei", "PingFang SC",\n',
    '    "Heiti SC", "Arial Unicode MS", "DejaVu Sans",\n',
    ']\n',
    'plt.rcParams["axes.unicode_minus"] = False\n',
    '\n',
    '\n',
    'def find_workspace_root(start=None):\n',
    '    start = Path.cwd() if start is None else Path(start)\n',
    '    for candidate in [start, *start.parents]:\n',
    '        if (candidate / "output" / "day04_project" / "ecommerce_customer_cleaned.csv").exists():\n',
    '            return candidate\n',
    '    raise FileNotFoundError("未找到第4天清洗数据，请先完成Day04。")\n',
    '\n',
    '\n',
    'ROOT = find_workspace_root()\n',
    'DATA_PATH = ROOT / "output" / "day04_project" / "ecommerce_customer_cleaned.csv"\n',
    'DAY05_DIR = ROOT / "output" / "day05_analysis"\n',
    'OUTPUT_DIR = ROOT / "output" / "day06_visualization"\n',
    'OUTPUT_DIR.mkdir(parents=True, exist_ok=True)\n',
    '\n',
    'print("学生：", STUDENT_ID)\n',
    'print("专题：", TOPIC)\n',
    'print("输出：", OUTPUT_DIR.relative_to(ROOT))',
]

# ---------------------------------------------------------------------------
# cell-5: business questions and chart reasons
# ---------------------------------------------------------------------------
cells[5]["source"] = [
    'business_questions = {\n',
    '    "category_bar": "不同支付偏好用户的规模和流失率有何差异？",\n',
    '    "behavior_scatter": "订单数与返现金额的分布关系如何？流失用户是否聚集在某个区域？",\n',
    '    "ordered_line": "不同生命周期阶段（TenureGroup）的流失率如何变化？",\n',
    '    "composition_chart": "各支付方式的用户数占比构成如何？",\n',
    '}\n',
    '\n',
    'chart_reasons = {\n',
    '    "category_bar": "支付方式是离散分类，比较各组的用户数和流失率适合用柱状图；流失率为比率，在标签中标注样本量。",\n',
    '    "behavior_scatter": "OrderCount和CashbackAmount都是数值字段，一行一名用户，用散点图能直观看出分布聚集和流失用户的区域。",\n',
    '    "ordered_line": "TenureGroup具有明确的先后顺序（新用户→24个月以上），适合用折线图展示流失率随阶段的变化趋势。",\n',
    '    "composition_chart": "支付方式共5个类别，数量较少，适合用环形图展示整体构成。",\n',
    '}\n',
    '\n',
    'assert all(text.strip() for text in business_questions.values()), "请填写4个业务问题"\n',
    'assert all(text.strip() for text in chart_reasons.values()), "请填写4个图表选择理由"\n',
    'print("检查点1B通过：业务问题和选择理由已填写")',
]

# ---------------------------------------------------------------------------
# cell-7: category bar data
# ---------------------------------------------------------------------------
cells[7]["source"] = [
    'category_field = "PreferredPaymentMode"\n',
    '\n',
    'category_summary = (\n',
    '    df.groupby(category_field, observed=True)\n',
    '      .agg(用户数=("CustomerID", "nunique"), 流失率=("Churn", "mean"))\n',
    '      .reset_index()\n',
    '      .sort_values("用户数", ascending=False)\n',
    ')\n',
    '\n',
    'assert category_field in df.columns, "category_field必须是有效字段"\n',
    'assert isinstance(category_summary, pd.DataFrame), "category_summary必须是DataFrame"\n',
    'assert {category_field, "用户数"}.issubset(category_summary.columns)\n',
    'display(category_summary)',
]

# ---------------------------------------------------------------------------
# cell-8: draw bar chart
# ---------------------------------------------------------------------------
cells[8]["source"] = [
    'fig_bar, ax_bar = plt.subplots(figsize=(10, 6))\n',
    '\n',
    'x_labels = category_summary[category_field].tolist()\n',
    'user_counts = category_summary["用户数"].tolist()\n',
    'churn_rates = category_summary["流失率"].tolist()\n',
    '\n',
    'colors = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F"]\n',
    'bars = ax_bar.bar(x_labels, user_counts, color=colors[:len(x_labels)], width=0.6)\n',
    '\n',
    'ax_bar.set_xlabel("支付方式", fontsize=12)\n',
    'ax_bar.set_ylabel("用户数", fontsize=12)\n',
    'ax_bar.set_title("不同支付方式的用户数与流失率", fontsize=14, fontweight="bold")\n',
    '\n',
    '# 在柱子上方标注用户数和流失率\n',
    'for bar, count, rate in zip(bars, user_counts, churn_rates):\n',
    '    ax_bar.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 30,\n',
    '                f"{count}\\n流失率{rate:.1%}",\n',
    '                ha="center", va="bottom", fontsize=10)\n',
    '\n',
    'ax_bar.set_ylim(0, max(user_counts) * 1.2)\n',
    'plt.xticks(rotation=15)\n',
    'plt.tight_layout()\n',
    '\n',
    'bar_path = OUTPUT_DIR / "01_category_bar.png"\n',
    'fig_bar.savefig(bar_path, dpi=150, bbox_inches="tight")\n',
    'plt.show()\n',
    '\n',
    'assert bar_path.exists() and bar_path.stat().st_size > 0, "柱状图尚未保存"\n',
    'print("已输出：", bar_path.relative_to(ROOT))',
]

# ---------------------------------------------------------------------------
# cell-9: bar chart conclusion (markdown)
# ---------------------------------------------------------------------------
cells[9]["source"] = [
    "### 柱状图结论\n",
    "\n",
    "- 观察：Debit Card用户数最多（2,314人），Credit Card次之（1,774人）；COD和E wallet用户流失率最高。\n",
    "- 证据：COD流失率24.9%（514人），E wallet流失率22.8%（614人），均高于总体流失率16.8%；Credit Card流失率最低14.2%（1,774人）。\n",
    "- 边界：该图只能展示各支付方式的用户规模和流失率差异，不能说明支付方式导致流失。",
]

# ---------------------------------------------------------------------------
# cell-11: scatter plot
# ---------------------------------------------------------------------------
cells[11]["source"] = [
    'x_field = "OrderCount"\n',
    'y_field = "CashbackAmount"\n',
    '\n',
    'assert x_field in df.columns and y_field in df.columns\n',
    'assert pd.api.types.is_numeric_dtype(df[x_field])\n',
    'assert pd.api.types.is_numeric_dtype(df[y_field])\n',
    '\n',
    'fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))\n',
    '\n',
    'churn_0 = df[df["Churn"] == 0]\n',
    'churn_1 = df[df["Churn"] == 1]\n',
    '\n',
    'ax_scatter.scatter(churn_0[x_field], churn_0[y_field], c="#4E79A7", alpha=0.3,\n',
    '                   s=15, label=f"未流失 ({len(churn_0)})")\n',
    'ax_scatter.scatter(churn_1[x_field], churn_1[y_field], c="#E15759", alpha=0.5,\n',
    '                   s=15, label=f"流失 ({len(churn_1)})")\n',
    '\n',
    'ax_scatter.set_xlabel("订单数", fontsize=12)\n',
    'ax_scatter.set_ylabel("返现金额", fontsize=12)\n',
    'ax_scatter.set_title("订单数与返现金额散点图（按流失状态着色）", fontsize=14, fontweight="bold")\n',
    'ax_scatter.legend(fontsize=11)\n',
    'plt.tight_layout()\n',
    '\n',
    'scatter_path = OUTPUT_DIR / "02_behavior_scatter.png"\n',
    'fig_scatter.savefig(scatter_path, dpi=150, bbox_inches="tight")\n',
    'plt.show()\n',
    '\n',
    'assert scatter_path.exists() and scatter_path.stat().st_size > 0, "散点图尚未保存"\n',
    'print("已输出：", scatter_path.relative_to(ROOT))',
]

# ---------------------------------------------------------------------------
# cell-12: scatter conclusion (markdown)
# ---------------------------------------------------------------------------
cells[12]["source"] = [
    "### 散点图结论\n",
    "\n",
    "- 观察：大部分用户的订单数集中在1-5单，返现金额集中在100-250元；流失用户（红色）在低订单数区域更为密集。\n",
    "- 证据：流失用户（948人）的订单数中位数为2，低于未流失用户的3；返现金额分布相似但流失用户在低返现区间占比更高。\n",
    "- 边界：相关关系不等于因果关系，订单数低可能是流失的结果而非原因。",
]

# ---------------------------------------------------------------------------
# cell-14: ordered line data
# ---------------------------------------------------------------------------
cells[14]["source"] = [
    'TENURE_ORDER = ["新用户", "0-6个月", "7-12个月", "13-24个月", "24个月以上"]\n',
    '\n',
    'ordered_field = "TenureGroup"\n',
    '\n',
    'ordered_summary = (\n',
    '    df.groupby(ordered_field, observed=True)\n',
    '      .agg(用户数=("CustomerID", "nunique"), 流失率=("Churn", "mean"))\n',
    '      .reset_index()\n',
    ')\n',
    'ordered_summary[ordered_field] = pd.Categorical(\n',
    '    ordered_summary[ordered_field], categories=TENURE_ORDER, ordered=True\n',
    ')\n',
    'ordered_summary = ordered_summary.sort_values(ordered_field).reset_index(drop=True)\n',
    '\n',
    'assert ordered_field in {"TenureGroup", "SatisfactionScore"}, \\\n',
    '    "本项目折线图只允许使用具有明确顺序的TenureGroup或SatisfactionScore"\n',
    'assert isinstance(ordered_summary, pd.DataFrame)\n',
    'assert {ordered_field, "用户数"}.issubset(ordered_summary.columns)\n',
    'display(ordered_summary)',
]

# ---------------------------------------------------------------------------
# cell-15: draw line chart
# ---------------------------------------------------------------------------
cells[15]["source"] = [
    'fig_line, ax_line = plt.subplots(figsize=(10, 6))\n',
    '\n',
    'x_pos = range(len(ordered_summary))\n',
    'rates = ordered_summary["流失率"].tolist()\n',
    'counts = ordered_summary["用户数"].tolist()\n',
    '\n',
    'ax_line.plot(x_pos, rates, marker="o", linewidth=2, markersize=8, color="#E15759")\n',
    '\n',
    '# 标注流失率和样本量\n',
    'for i, (rate, count) in enumerate(zip(rates, counts)):\n',
    '    ax_line.annotate(f"{rate:.1%}\\n(n={count})",\n',
    '                     (i, rate), textcoords="offset points", xytext=(0, 12),\n',
    '                     ha="center", fontsize=10)\n',
    '\n',
    'ax_line.set_xticks(list(x_pos))\n',
    'ax_line.set_xticklabels([str(x) for x in ordered_summary[ordered_field]], rotation=15)\n',
    'ax_line.set_xlabel("生命周期阶段", fontsize=12)\n',
    'ax_line.set_ylabel("流失率", fontsize=12)\n',
    'ax_line.set_title("不同生命周期阶段的流失率变化", fontsize=14, fontweight="bold")\n',
    'ax_line.yaxis.set_major_formatter(PercentFormatter(1))\n',
    'ax_line.set_ylim(0, max(rates) * 1.3)\n',
    'ax_line.grid(axis="y", alpha=0.3)\n',
    'plt.tight_layout()\n',
    '\n',
    'line_path = OUTPUT_DIR / "03_ordered_line.png"\n',
    'fig_line.savefig(line_path, dpi=150, bbox_inches="tight")\n',
    'plt.show()\n',
    '\n',
    'assert line_path.exists() and line_path.stat().st_size > 0, "折线图尚未保存"\n',
    'print("已输出：", line_path.relative_to(ROOT))',
]

# ---------------------------------------------------------------------------
# cell-16: line chart conclusion (markdown)
# ---------------------------------------------------------------------------
cells[16]["source"] = [
    "### 折线图结论\n",
    "\n",
    "- 观察：新用户流失率最高，随着生命周期延长流失率呈下降趋势，24个月以上用户流失率最低。\n",
    "- 证据：新用户流失率约25.3%（622人），0-6个月约19.7%（1,094人），24个月以上约8.5%（353人），呈明显递减趋势。\n",
    "- 边界：这是有序阶段比较，不是月度、年度或历史时间趋势。",
]

# ---------------------------------------------------------------------------
# cell-18: composition chart data
# ---------------------------------------------------------------------------
cells[18]["source"] = [
    'composition_field = "PreferredPaymentMode"\n',
    '\n',
    'composition_summary = (\n',
    '    df.groupby(composition_field, observed=True)\n',
    '      .agg(用户数=("CustomerID", "nunique"))\n',
    '      .reset_index()\n',
    '      .sort_values("用户数", ascending=False)\n',
    ')\n',
    'composition_summary["占比"] = composition_summary["用户数"] / composition_summary["用户数"].sum()\n',
    '\n',
    'assert composition_field in df.columns\n',
    'assert isinstance(composition_summary, pd.DataFrame)\n',
    'assert {composition_field, "用户数", "占比"}.issubset(composition_summary.columns)\n',
    'assert np.isclose(composition_summary["占比"].sum(), 1.0), "构成占比之和应为1"\n',
    'display(composition_summary)',
]

# ---------------------------------------------------------------------------
# cell-19: draw composition chart (donut)
# ---------------------------------------------------------------------------
cells[19]["source"] = [
    'fig_composition, ax_composition = plt.subplots(figsize=(10, 6))\n',
    '\n',
    'labels = composition_summary[composition_field].tolist()\n',
    'sizes = composition_summary["用户数"].tolist()\n',
    'colors = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F"]\n',
    '\n',
    'wedges, texts, autotexts = ax_composition.pie(\n',
    '    sizes, labels=labels, autopct=lambda p: f"{p:.1%}\\n({int(p*sum(sizes)/100)})",\n',
    '    colors=colors[:len(labels)], startangle=90, pctdistance=0.75,\n',
    '    wedgeprops=dict(width=0.4, edgecolor="white"),\n',
    ')\n',
    'for t in autotexts:\n',
    '    t.set_fontsize(9)\n',
    'ax_composition.set_title("各支付方式用户数占比", fontsize=14, fontweight="bold")\n',
    'plt.tight_layout()\n',
    '\n',
    'composition_path = OUTPUT_DIR / "04_composition_chart.png"\n',
    'fig_composition.savefig(composition_path, dpi=150, bbox_inches="tight")\n',
    'plt.show()\n',
    '\n',
    'assert composition_path.exists() and composition_path.stat().st_size > 0, "构成图尚未保存"\n',
    'print("已输出：", composition_path.relative_to(ROOT))',
]

# ---------------------------------------------------------------------------
# cell-20: composition conclusion (markdown)
# ---------------------------------------------------------------------------
cells[20]["source"] = [
    "### 构成图结论\n",
    "\n",
    "- 观察：Debit Card和Credit Card是用户的主要支付方式，合计占比超过70%。\n",
    "- 证据：Debit Card占41.1%（2,314人），Credit Card占31.5%（1,774人），E wallet占10.9%（614人），COD占9.1%（514人），UPI占7.4%（414人）。\n",
    "- 边界：该图适合展示各支付方式的用户占比构成，不适合比较各组的流失率或行为指标差异。",
]

# ---------------------------------------------------------------------------
# cell-24: 2x2 summary dashboard
# ---------------------------------------------------------------------------
cells[24]["source"] = [
    'fig_summary, axes = plt.subplots(2, 2, figsize=(14, 10))\n',
    '\n',
    '# [0,0] 柱状图：支付方式用户数与流失率\n',
    'ax = axes[0, 0]\n',
    'bars = ax.bar(x_labels, user_counts, color=colors[:len(x_labels)], width=0.6)\n',
    'ax.set_title("支付方式用户数与流失率", fontsize=12, fontweight="bold")\n',
    'ax.set_ylabel("用户数")\n',
    'for bar, count, rate in zip(bars, user_counts, churn_rates):\n',
    '    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,\n',
    '            f"{count}\\n{rate:.1%}", ha="center", va="bottom", fontsize=8)\n',
    'ax.set_ylim(0, max(user_counts) * 1.2)\n',
    'plt.setp(ax.get_xticklabels(), rotation=15, fontsize=9)\n',
    '\n',
    '# [0,1] 散点图：订单数 vs 返现金额\n',
    'ax = axes[0, 1]\n',
    'ax.scatter(churn_0[x_field], churn_0[y_field], c="#4E79A7", alpha=0.3, s=10, label="未流失")\n',
    'ax.scatter(churn_1[x_field], churn_1[y_field], c="#E15759", alpha=0.5, s=10, label="流失")\n',
    'ax.set_title("订单数 vs 返现金额", fontsize=12, fontweight="bold")\n',
    'ax.set_xlabel("订单数")\n',
    'ax.set_ylabel("返现金额")\n',
    'ax.legend(fontsize=9)\n',
    '\n',
    '# [1,0] 折线图：生命周期流失率\n',
    'ax = axes[1, 0]\n',
    'ax.plot(x_pos, rates, marker="o", linewidth=2, markersize=6, color="#E15759")\n',
    'for i, (rate, count) in enumerate(zip(rates, counts)):\n',
    '    ax.annotate(f"{rate:.1%}", (i, rate), textcoords="offset points",\n',
    '                xytext=(0, 8), ha="center", fontsize=8)\n',
    'ax.set_xticks(list(x_pos))\n',
    'ax.set_xticklabels([str(x) for x in ordered_summary[ordered_field]], rotation=15, fontsize=9)\n',
    'ax.set_title("生命周期阶段流失率", fontsize=12, fontweight="bold")\n',
    'ax.set_ylabel("流失率")\n',
    'ax.yaxis.set_major_formatter(PercentFormatter(1))\n',
    'ax.grid(axis="y", alpha=0.3)\n',
    '\n',
    '# [1,1] 环形图：支付方式占比\n',
    'ax = axes[1, 1]\n',
    'ax.pie(sizes, labels=labels, autopct="%1.1f%%",\n',
    '       colors=colors[:len(labels)], startangle=90,\n',
    '       wedgeprops=dict(width=0.4, edgecolor="white"), textprops={"fontsize": 9})\n',
    'ax.set_title("支付方式用户占比", fontsize=12, fontweight="bold")\n',
    '\n',
    'fig_summary.suptitle("电商用户数据可视化分析概览", fontsize=16, fontweight="bold")\n',
    'fig_summary.tight_layout(rect=[0, 0, 1, 0.96])\n',
    '\n',
    'summary_path = OUTPUT_DIR / "day06_visualization_summary.png"\n',
    'fig_summary.savefig(summary_path, dpi=150, bbox_inches="tight")\n',
    'plt.show()\n',
    '\n',
    'assert summary_path.exists() and summary_path.stat().st_size > 0, "综合图尚未保存"\n',
    'print("已输出：", summary_path.relative_to(ROOT))',
]

# ---------------------------------------------------------------------------
# cell-25: overall findings (markdown)
# ---------------------------------------------------------------------------
cells[25]["source"] = [
    "## 综合发现与局限\n",
    "\n",
    "1. 综合发现1：COD和E wallet用户流失率分别为24.9%和22.8%，显著高于总体16.8%，是高流失风险群体。证据来自segment_analysis。\n",
    "2. 综合发现2：新用户流失率约25.3%，随着生命周期延长逐步下降到8.5%，说明早期阶段是留存关键期。证据来自折线图和ordered_summary。\n",
    "3. 综合发现3：Debit Card和Credit Card合计占用户72.6%，是核心支付方式，但流失率相对较低（15.4%和14.2%）。证据来自构成图和segment_analysis。\n",
    "4. 数据或方法局限：数据中没有订单金额和日期，无法计算GMV或时间趋势；部分交叉组合样本量不足（如COD×CityTier=2仅16人）；流失与支付方式的关联可能受满意度、品类偏好等混杂变量影响。\n",
    "\n",
    "注意：`CashbackAmount`是返现金额，不是销售额、收入或GMV。",
]

# ---------------------------------------------------------------------------
# cell-27: chart manifest
# ---------------------------------------------------------------------------
cells[27]["source"] = [
    'chart_manifest = pd.DataFrame([\n',
    '    {"chart_id": "01", "file_name": "01_category_bar.png",\n',
    '     "business_question": "不同支付偏好用户的规模和流失率有何差异？",\n',
    '     "chart_type": "bar",\n',
    '     "key_finding": "COD流失率24.9%最高，Credit Card最低14.2%；Debit Card用户最多2314人",\n',
    '     "limitation": "不能说明支付方式导致流失"},\n',
    '    {"chart_id": "02", "file_name": "02_behavior_scatter.png",\n',
    '     "business_question": "订单数与返现金额的分布关系如何？流失用户是否聚集？",\n',
    '     "chart_type": "scatter",\n',
    '     "key_finding": "流失用户在低订单数区域更密集，订单中位数2低于未流失的3",\n',
    '     "limitation": "相关不等于因果，低订单可能是流失的结果"},\n',
    '    {"chart_id": "03", "file_name": "03_ordered_line.png",\n',
    '     "business_question": "不同生命周期阶段的流失率如何变化？",\n',
    '     "chart_type": "line",\n',
    '     "key_finding": "新用户流失率25.3%最高，24个月以上8.5%最低，呈递减趋势",\n',
    '     "limitation": "是有序阶段比较，不是时间趋势"},\n',
    '    {"chart_id": "04", "file_name": "04_composition_chart.png",\n',
    '     "business_question": "各支付方式的用户数占比构成如何？",\n',
    '     "chart_type": "pie_or_bar",\n',
    '     "key_finding": "Debit Card占41.1%，Credit Card占31.5%，合计超72%",\n',
    '     "limitation": "仅展示占比，不适合比较行为指标"},\n',
    '    {"chart_id": "05", "file_name": "day06_visualization_summary.png",\n',
    '     "business_question": "整体概览",\n',
    '     "chart_type": "dashboard",\n',
    '     "key_finding": "COD/E wallet流失高，新用户风险大，Debit/Credit Card是核心用户",\n',
    '     "limitation": "综合图信息密度高，细节需查看各独立图"},\n',
    '])\n',
    '\n',
    'assert len(chart_manifest) == 5\n',
    'assert not chart_manifest.astype(str).apply(lambda col: col.str.contains("请填写").any()).any(), \\\n',
    '    "请完成图表清单"\n',
    '\n',
    'manifest_path = OUTPUT_DIR / "chart_manifest.csv"\n',
    'chart_manifest.to_csv(manifest_path, index=False, encoding="utf-8-sig")\n',
    'display(chart_manifest)',
]

# ---------------------------------------------------------------------------
# Write notebook
# ---------------------------------------------------------------------------
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

# Verify
with open(OUT_PATH, "r", encoding="utf-8") as f:
    nb2 = json.load(f)

code_cells = [c for c in nb2["cells"] if c["cell_type"] == "code"]
has_todo = any("TODO" in "".join(c["source"]) for c in code_cells)
has_pass = any("".join(c["source"]).strip() == "pass" for c in code_cells)
has_placeholder = any("请填写" in "".join(c["source"]) for c in code_cells)

print(f"Code cells: {len(code_cells)}")
print(f"TODO残留: {has_todo}")
print(f"pass残留: {has_pass}")
print(f"请填写残留: {has_placeholder}")
print("Done!")
