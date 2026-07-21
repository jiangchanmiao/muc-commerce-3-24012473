"""Day8 Flask 数据看板强化 — 接口测试

运行方式（在项目目录 day08_flask_upgrade_student 下执行）：
    python -m pytest test_day08_api.py -v

前提：已安装 pytest，且项目 data/ 目录下有 CSV 数据文件。
"""

import json
import sys
from pathlib import Path

# 把项目根目录加入 sys.path，确保能导入 app 和 services
# 测试文件放在桌面时，需要指向 PyCharmMiscProject 下的项目目录
BASE_DIR = Path(r"C:\Users\QH153\PyCharmMiscProject\ecommerce-user-analysis-seed\day08_flask_upgrade_student")
sys.path.insert(0, str(BASE_DIR))

from app import app


# ------------------------------------------------------------------
# 测试辅助：创建一个已登录的测试客户端
# ------------------------------------------------------------------

def _logged_in_client():
    """返回一个模拟登录后的 Flask test_client。"""
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["username"] = "student"
    return client


# ------------------------------------------------------------------
# 测试 1：/health 不需要登录，返回 JSON
# ------------------------------------------------------------------

def test_health_no_login_required():
    """访问 /health 应返回 ok=True，不需要登录。"""
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["ok"] is True
    assert "service" in data


# ------------------------------------------------------------------
# 测试 2：/api/metrics 需要登录，返回包含 label/value/note 的指标列表
# ------------------------------------------------------------------

def test_metrics_api_logged_in():
    """登录后访问 /api/metrics 应返回指标列表，每项含 label/value/note。"""
    client = _logged_in_client()
    resp = client.get("/api/metrics")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["ok"] is True
    assert "metrics" in data
    metrics = data["metrics"]
    assert isinstance(metrics, list)
    assert len(metrics) > 0
    # 每条指标必须包含 label、value、note 三个字段
    for item in metrics:
        assert "label" in item
        assert "value" in item
        assert "note" in item


# ------------------------------------------------------------------
# 测试 3：/api/categories 按品类筛选，返回对应行
# ------------------------------------------------------------------

def test_categories_api_with_filter():
    """登录后带 category 参数访问 /api/categories 应返回筛选后的行。"""
    client = _logged_in_client()
    resp = client.get("/api/categories?category=Fashion")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["ok"] is True
    assert data["category"] == "Fashion"
    rows = data["rows"]
    assert isinstance(rows, list)
    # 篮选后每行的偏好品类应为 Fashion
    for row in rows:
        assert row.get("偏好品类") == "Fashion"


# ------------------------------------------------------------------
# 测试 4：未登录访问 /api/metrics 应被拒绝
# ------------------------------------------------------------------

def test_metrics_api_require_login():
    """未登录访问 /api/metrics 应被重定向到登录页。"""
    client = app.test_client()
    resp = client.get("/api/metrics")
    # login_required 会 redirect 到 /login，状态码 302
    assert resp.status_code == 302
    assert "/login" in resp.headers.get("Location", "")


# ------------------------------------------------------------------
# 测试 5：/api/ask 空问题返回 400 JSON 错误
# ------------------------------------------------------------------

def test_ask_empty_question_returns_400():
    """POST /api/ask 传空问题应返回 400 和 JSON 错误结构。"""
    client = _logged_in_client()
    resp = client.post("/api/ask", json={"question": ""})
    assert resp.status_code == 400
    data = json.loads(resp.data)
    assert data["ok"] is False
    # 400 错误应包含 error 或 answer 字段
    assert "answer" in data or "error" in data
