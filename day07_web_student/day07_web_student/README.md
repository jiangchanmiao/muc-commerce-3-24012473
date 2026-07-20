# 第7天学生项目：电商用户分析Web系统

## 运行方法

```bash
python -m pip install -r requirements.txt
python app.py
```

浏览器访问 `http://127.0.0.1:5000`。

- 用户名：`student`
- 密码：`day07`

## 上午停止线

上午只完成以下内容：

1. 建立并重命名个人项目；
2. 从VS Code终端启动Flask；
3. 测试正确登录、错误登录、访问拦截和退出；
4. 定位`app.py`、`services`、`templates`、`static`和`data`；
5. 核对已有2张指标卡、1张图和“总用户数”问答；
6. 搜索TODO，但暂不修改`TODO 2-1`至`TODO 4-1`。

## 下午核心任务

1. 检查并解释登录、退出和登录访问控制；
2. 完成4张指标卡和2张真实图表；
3. 完成偏好品类筛选；
4. 完成至少4类离线规则问答；
5. 在`screenshots`目录保存4张核心验收截图；
6. 完成一项必选拓展；
7. 修改本文件，填写个人信息、完成功能、拓展说明和未解决问题。

使用编辑器搜索`TODO`即可找到需要完成的位置。

## 必选拓展

本项目选择 **拓展 A：导出当前筛选结果**。

新增CSV下载功能，导出内容必须与当前`category`筛选一致。

## 下午核心任务完成说明

### 完成的代码点（搜索 TODO 可见）

| 编号 | 文件 | 实现内容 |
|------|------|----------|
| TODO 2-1 | `services/data_service.py` | 指标卡由 2 张增加到 4 张：新增「总体流失率」「平均订单数」 |
| TODO 2-2 | `services/data_service.py` | 用 `segment_df` 计算流失率最高的生命周期阶段，生成一句数据观察 |
| TODO 2-3 | `templates/dashboard.html` | 图表区新增第二张图，展示 `03_ordered_line.png`（各阶段平均订单数趋势） |
| TODO 3-1 | `services/data_service.py` | 按 `selected_category` 布尔筛选 `category_df`，看板表格与下载随之联动 |
| TODO 4-1 | `services/qa_service.py` | 离线规则问答新增「流失率」「偏好品类」「生命周期风险」「订单」四类，全部引用 `data/` 已有指标 |

### 四项离线问答示例

- 总用户数：数据集中共有 5,630 名用户。
- 总体流失率：总体流失率为 16.8%，对应流失人数 948 人。
- 偏好品类：用户数最多的是「Mobile Phone」（2,080 人）；流失率最高的是「Mobile Phone」（27.4%）。
- 生命周期风险：风险最高的是「新用户」阶段，流失率 53.5%。
- 订单：平均订单数 2.96 单/人，中位数 2 单。

## 拓展 A 实现说明（导出当前筛选结果）

- 路由：`/download?category=Fashion`（`category=全部` 时导出全部品类）
- 复用 `filter_category_export()` 的筛选逻辑，不重新定义指标
- 返回 UTF-8（带 BOM）CSV，文件名形如 `category_analysis_Fashion.csv`
- 看板筛选区提供「下载当前筛选CSV」按钮，导出内容与当前品类筛选一致
- 关键实现位置：`app.py` 的 `download()` 路由 + `services/data_service.py` 的 `filter_category_export()`

## 学生信息

- 姓名：曲浩
- 学号：24012473
- 专题方向：电商用户行为分析可视化与 Web 呈现
- 已完成功能：4 张指标卡、2 张真实图表、偏好品类筛选、4 类离线问答、拓展 A（导出筛选 CSV）
- 选择的拓展任务：A. 导出当前筛选结果
- 拓展访问或运行方法：运行 `python app.py` 后访问 `http://127.0.0.1:5000
- 尚未解决的问题：智能问答基于关键词匹配，只能回答预设范围内的问题，遇到不同表述时可能无法正确应答。

## 验收截图说明

`screenshots/` 目录需保存以下图片：

- `01_login.png`、`02_dashboard.png`、`03_interaction.png`、`04_assistant.png`（四项核心验收）
- `05_extension.png`（拓展 A：下载筛选 CSV 的运行证据）

> 