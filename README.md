# 贪吃蛇游戏 Snake Game

基于 Python 与 Pygame 的贪吃蛇游戏设计与实现

- **小组成员**：何岚、李思齐
- **指导教师**：黄天羽
- **开发语言**：Python 3
- **开发框架**：Pygame 2.x

---

## 一、运行方法

```bash
# 1. 安装依赖
pip install pygame

# 2. 运行游戏
python main.py
```

### 操作方式

| 按键 | 功能 |
|------|------|
| ↑ ↓ ← → | 控制蛇的移动方向 |
| R | Game Over 后重新开始 |
| ESC | 退出游戏 |

---

## 二、程序结构

```
SnakeGame/
│
├── main.py        # 程序入口：初始化 Pygame，创建 Game 并启动
├── game.py        # 主循环、事件处理、状态协调、重新开始
├── snake.py       # 蛇的移动、增长、碰撞检测、绘制
├── food.py        # 食物的随机生成（含去重）与绘制
├── ui.py          # 分数显示、Game Over 界面
│
├── test_game.py   # 自动化测试
└── README.md
```

### 模块职责

| 模块 | 职责 |
|------|------|
| `main.py` | 初始化 Pygame，创建 `Game` 实例并调用 `run()` |
| `game.py` | 游戏主循环、键盘事件、分数、判定吃食物与碰撞、重启 |
| `snake.py` | 维护蛇身坐标列表，处理移动、增长、碰撞判定 |
| `food.py` | 生成不与蛇身重合的随机食物位置 |
| `ui.py` | 绘制实时分数与 Game Over 遮罩界面 |

设计原则：`Game` 只负责**协调**，不直接操作蛇的坐标；
`Snake` / `Food` / `UI` 各自封装数据与绘制，便于单独调试和扩展。

---

## 三、核心技术点

### 1. 防止蛇瞬间反向

不直接修改当前方向，而是先存入 `next_direction`，在 `move()` 时才提交：

```python
if direction == "LEFT" and self.direction != "RIGHT":
    self.next_direction = "LEFT"
```

比较对象是 `self.direction`（上一次 `move()` 已提交的方向），
而不是 `next_direction`。这样即使玩家在同一帧内连按两个方向键
（例如向右移动时快速按 ↑ 再按 ←），反向的那一次也会被拒绝。

### 2. 食物不落在蛇身上（拒绝采样）

```python
def randomize(self, snake_body):
    new_position = self.random_position()
    while new_position in snake_body:
        new_position = self.random_position()
    self.position = new_position
```

### 3. 碰撞检测拆成两个独立判断

```python
if x < 0 or x >= w or y < 0 or y >= h:   # ① 撞墙
    return True
if self.body[0] in self.body[1:]:        # ② 撞自己
    return True
```

### 4. 重新开始 = 重建对象

不逐个字段清零，直接重建 `Snake` 和 `Food`，从根本上杜绝状态残留：

```python
def restart(self):
    self.score = 0
    self.game_over = False
    self.snake = Snake(self.width, self.height)
    self.food = Food(self.width, self.height, self.snake.body)
```

### 5. 速度控制

```python
self.clock.tick(10)   # 10 FPS，每秒移动 10 格
```

用 Pygame 时钟锁帧，把"移动速度"与"刷新率"解耦。

---

## 四、本次修复记录

### 修复：开局第一个食物可能生成在蛇身上

**问题**：`Food.__init__` 直接调用 `random_position()`，没有做去重检查。
`randomize()` 是检查了的，所以只有**开局的第一个食物**有概率被蛇身盖住，
玩家看不见食物。

**修复**：`Food.__init__` 增加可选参数 `snake_body`，构造时即调用
`randomize()` 做去重；`game.py` 在创建和重启时都把蛇身传进去。

```python
# food.py
def __init__(self, width, height, snake_body=None):
    ...
    self.randomize(snake_body)

# game.py
self.food = Food(self.width, self.height, self.snake.body)
```

### 改进：R 键只在 Game Over 后生效

原先游戏进行中按 R 也会重开，容易误触。

```python
if event.key == pygame.K_r and self.game_over:
    self.restart()
```

---

## 五、测试

```bash
python test_game.py
```

包含 6 项检查：

| # | 测试内容 |
|---|----------|
| 1 | 同一帧连按两键不能反向自杀 |
| 2 | 开局食物不落在蛇身上（3000 次随机种子） |
| 3 | 重新开始后分数、长度、状态完全复位 |
| 4 | 碰撞检测（撞墙 / 撞自己 / 正常均正确） |
| 5 | 吃到食物后长度 +1、分数 +10 |
| 6 | 2000 步随机操作压力测试不崩溃 |

当前状态：**6 / 6 全部通过**

---

## 六、后续计划

- [ ] 完善界面：网格线、开始页面、暂停功能
- [ ] 增加最高分记录
- [ ] 增加难度递增（随分数提高速度）
- [ ] 录制演示视频与设计文档
