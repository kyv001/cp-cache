# cp-cache

一个用于复制 SPlayer 缓存文件并合并音频轨道的 CLI 工具。

## 功能

- 从 SPlayer 缓存目录复制音频文件
- 自动匹配曲目 ID 与缓存文件
- 支持批量重命名和添加序号前缀
- 使用 ffmpeg 合并多个音频文件为一个专辑文件
- 支持 mp3、wav、flac 等常见音频格式

## 安装

### 环境要求

- Python 3.13+
- ffmpeg（系统需已安装）
- uv（Python 包管理器）

### 安装步骤

```bash
# 克隆仓库
git clone <repository-url>
cd cp-cache

# 安装依赖
uv sync

# 安装为可编辑模式（可选）
uv pip install -e .
```

## 使用方法

### 直接运行

```bash
# 使用 uv 运行
uv run cp-cache

# 或激活虚拟环境后运行
source .venv/bin/activate
cp-cache
```

### 使用流程示例

```bash
$ uv run cp-cache
CP Cache CLI
Default cache path: /home/user/.config/SPlayer/DataCache/music
Confirm? (Y/enter path): y
Using cache path: /home/user/.config/SPlayer/DataCache/music
Enter target path: ~/Music/MyAlbum
Using target path: /home/user/Music/MyAlbum

# 输入曲目 ID（在 SPlayer 中查看）
Enter track ID (^C or ^D to exit): 123456
Using file: 123456_abc123def456.mp3
Enter target file name (without extension):  song1
123456_abc123def456.mp3 -> song1.mp3

Enter track ID (^C or ^D to exit): 123457
Using file: 123457_xyz789uvw012.mp3
Enter target file name (without extension):  song2
123457_xyz789uvw012.mp3 -> song2.mp3

Enter track ID (^C or ^D to exit): 123458
Multiple files found for track ID 123458: ['123458_high.mp3', '123458_low.mp3']
Enter file index (0-1): 0
Using file: 123458_high.mp3
Enter target file name (without extension):  song3
123458_high.mp3 -> song3.mp3

# 按 Ctrl+C 或 Ctrl+D 结束输入
Enter track ID (^C or ^D to exit): ^C

# 添加序号前缀
Would you like to add track id prefix? (Y/n): y
/home/user/.config/SPlayer/DataCache/music/123456_abc123def456.mp3 -> /home/user/Music/MyAlbum/01 - song1.mp3
/home/user/.config/SPlayer/DataCache/music/123457_xyz789uvw012.mp3 -> /home/user/Music/MyAlbum/02 - song2.mp3
/home/user/.config/SPlayer/DataCache/music/123458_high.mp3 -> /home/user/Music/MyAlbum/03 - song3.mp3

# 合并专辑（可选）
Enter album name (leave blank to skip): My Album
```

### 快捷键

- `Ctrl+C` 或 `Ctrl+D`：退出当前输入，进入下一步

## 项目结构

```
cp-cache/
├── src/
│   └── cp_cache/
│       └── __init__.py    # 主模块和 CLI 入口
├── pyproject.toml         # 项目配置和依赖
├── uv.lock               # uv 锁定文件
├── README.md             # 本文件
└── LICENSE               # 许可证
```

## 开发

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行单个测试文件
uv run pytest tests/test_specific.py

# 运行单个测试函数
uv run pytest tests/test_specific.py::test_function_name

# 生成覆盖率报告
uv run pytest --cov=cp_cache --cov-report=term-missing
```

### 代码检查

```bash
# 格式化代码
uv run ruff format .

# 检查代码
uv run ruff check .

# 自动修复问题
uv run ruff check . --fix

# 类型检查
uv run mypy src/cp_cache
```

### 构建

```bash
# 构建 wheel 包
uv build
```

## 依赖

- **ffmpeg-python**: ffmpeg Python 绑定
- **future**: Python 2/3 兼容库（ffmpeg-python 的依赖）

## 注意事项

- 确保系统已安装 ffmpeg
- 默认缓存路径为 `~/.config/SPlayer/DataCache/music`
- 输出格式为 mp3，即使原始文件是其他格式
- **缓存文件格式**：`{trackid}_{quality}.sc`
  - `trackid`：曲目 ID，一个大整数（约 8-10 位）
  - `quality`：音质，`standard`（标准音质）或 `HQ`（高品质）
  - `.sc`：文件后缀名无实际意义，覆盖了原始后缀名
  - 实际音频格式：mp3、flac 或其他音频格式

## 许可证

[LICENSE](LICENSE)

## 免责声明

> ⚠️ **重要提示**

1. **与 SPlayer 的关系**：本软件与 [SPlayer](https://github.com/imsyy/SPlayer) 及其开发团队没有任何关联，SPlayer 是其各自所有者的商标。

2. **版权风险**：本工具仅从本地缓存目录读取已存在的文件，该功能可能存在潜在的版权风险。使用本工具处理任何受版权保护的内容可能违反相关法律法规。

3. **合法使用**：**请勿将本软件用于任何非法目的**，包括但不限于未经授权复制、分发受版权保护的内容。用户应自行承担使用本软件的所有法律责任。

4. **使用限制**：本软件仅供学习和研究目的使用。在使用前，请确保您拥有处理相关内容的合法权利。

## 致谢

- 感谢 [SPlayer](https://github.com/imsyy/SPlayer) 提供的优秀音乐播放器
