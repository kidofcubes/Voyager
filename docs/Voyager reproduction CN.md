

# Voyager
## 安装

先要安装 [uv](https://docs.astral.sh/uv/) 和 [npm](https://nodejs.org) (测试的时候用的 npm 版本是 v24.4.1)

Linux 安装: (在windows上应该差的不多)
```bash
git clone https://github.com/kidofcubes/Voyager.git
uv venv --python 3.13.5
source .venv/bin/activate #用上uv的venv
uv pip install -e .
cd voyager/env/mineflayer
npm install
cd mineflayer-collectblock
npx tsc
cd ..
npm install
```


注意: 主Voyager class被改过从原版来让改LLM的配置更容易


## 快速开始

### jupyter lab (推荐)

`$ jupyter lab --port 9998 --ip=0.0.0.0`
点击或复制终端中生成的链接，粘贴到浏览器中，然后打开 training.ipynb

### 直接使用 Python 脚本
默认情况下，training.py 脚本已配置为通过 25565 端口连接 Minecraft，使用 OpenRouter 上的 meta-llama/llama-3.1-405b-instruct:free 作为其 AI 模型，并使用 Qwen/Qwen3-Embedding-8B 作为其嵌入模型。

对于首次测试运行，你可以通过设置环境变量来完成配置：将 `HUGGINGFACEHUB_API_TOKEN` 设置为你的 Hugging Face 令牌，并将 `OPENAI_API_KEY` 设置为你的 https://openrouter.ai 令牌，如下所示：

`HUGGINGFACEHUB_API_TOKEN=hf_token_here OPENAI_API_KEY=openrouter_token_here python train.py`

（请注意：你需要确保本地的 3000 端口空闲以供 MineFlayer 使用，同时确保有一个 Minecraft 服务器/实例正在 25565 端口上运行。）

（新账户在 Hugging Face 和 OpenRouter 上获得的免费额度足以测试程序是否正常工作，但远远不足以支持一次完整的训练过程。）

# 我的世界 (仅限Java版)

以下是您提供内容的中文翻译，适用于 GitHub 项目的 README 文档，语言清晰、专业，符合技术文档风格：

---

## 客户端托管 / 单人游戏托管（使用“开放至局域网”功能）

从技术上讲，使用 Minecraft 并不需要 Microsoft 账号，但您需要使用像 [Prism Launcher](https://prismlauncher.org/) 这样的第三方启动器以**离线模式**启动游戏。

要在没有账户的情况下，在 Prism Launcher 中添加仅限离线的账号，请在你的 Prism Launcher 文件夹中创建一个名为 `accounts.json` 的文件。  
在 Linux 系统中，该文件的路径通常为：`/home/用户名/.local/share/PrismLauncher/accounts.json`

`accounts.json` 
```json
{"accounts": [{"entitlement": {"canPlayMinecraft": true,"ownsMinecraft": true},"type": "MSA"}],"formatVersion": 3}
```

1. 安装一个 Minecraft 启动器，并安装 **1.19.4 版本的 Fabric**。  
   （推荐使用 Prism Launcher，它能更方便地管理模组和配置，但大多数启动器均可使用。）

2. 安装以下模组及其依赖项（所有模组均可在 [Modrinth](https://modrinth.com/) 上找到）：
   - `Multiplayer Server Pause`
   - `Better Respawn`
   - `Mod Menu`

   **使用的具体版本：**
   - Minecraft: 1.19.4
   - Fabric Loader: 0.17.2
   - Fabric API: 0.87.2+1.19.4
   - Mod Menu: 1.0.3
   - Multiplayer Server Pause: 1.3.1
   - iChunUtil: 1.0.3
   - Better Respawn: 1.19.4-2.0.2

   （安装方式：将 `.jar` 文件放入 `minecraft_folder/mods` 文件夹中。）

3. 配置 `Better Respawn` 的设置：  
   编辑位于 `minecraft_folder/config/better_respawn/better_respawn.properties` 的配置文件，内容如下：

   ```ini
   # 玩家重生时距离死亡位置的最大距离
   max_respawn_distance=32
   # 玩家重生时距离死亡位置的最小距离
   min_respawn_distance=0
   # 若床或重生锚在此范围内，玩家将在此重生
   respawn_block_range=32
   ```

4. 启动游戏，进入“单人游戏”并创建一个新世界。  
   将游戏模式设为“创造模式”（Creative），难度设为“和平”（Peaceful）。

5. 世界创建完成后，按下 `Esc` 键，选择“开放至局域网”（Open to LAN）。  
   勾选“允许作弊：开启”，然后点击“开始局域网世界”。

6. 聊天栏中会显示一个端口号，该端口即为你的 `mc-port`。

---

## 专用服务器托管（需要安装 Java 17）

从 [Fabric 官网](https://fabricmc.net/use/server/) 下载对应版本的服务器安装程序，或在新建文件夹中运行以下命令：

```bash
curl -OJ https://meta.fabricmc.net/v2/versions/loader/1.19.4/0.17.2/1.1.0/server/jar
java -Xmx2G -jar fabric-server-mc.1.19.4-loader.0.17.2-launcher.1.1.0.jar nogui
```

服务器首次运行后会生成 `server.properties` 文件，请修改以下配置项：

```ini
difficulty=peaceful
gamemode=survival
online-mode=false
enable-rcon=true  # 仅在需要使用 RCON 功能时启用
rcon.password=hunter2
rcon.port=25575
spawn-protection=0  # 此项非常重要，否则机器人无法在出生点附近执行操作
```

接着，将上述客户端托管部分中列出的模组安装到服务器的 `mods` 文件夹中（服务器首次运行后会自动生成该文件夹）。

以相同方式配置 `better_respawn`，然后重新启动服务器。

---

### [Azure](https://github.com/MineDojo/Voyager/blob/main/installation/minecraft_instance_install.md#option-1-microsoft-azure-login-recommended)（未测试）

这是原始 Voyager 项目的推荐方法，但我尚未有机会亲自测试。

项目说明中提到：
> 使用此方法可让 Voyager 在请求超时时自动恢复。

但截至目前，我在本地托管时并未遇到此类问题。

---

# AI 集成

## 本地部署（Self-Hosting）

初步测试在配备 12GB 显存的 RTX 3060 上进行。使用 `Qwen3-14B-Q4_K_M` GGUF 模型是能流畅运行的最大模型（在 `llama.cpp` 下约每秒生成 26 个 token）。


### [vLLM](https://docs.vllm.ai/en/v0.10.1/getting_started/quickstart.html)

- 需在独立的虚拟环境中安装。
- 仅支持 Linux 系统，Windows 用户需使用 WSL。
- 支持同时托管嵌入模型（embeddings）和大语言模型（LLMs）。

### [llama.cpp](https://github.com/ggml-org/llama.cpp)（仅支持 GGUF 格式）

- 可在 Windows 和 Linux 上通过二进制文件轻松安装。
- 适用于模型过大、无法完全加载到 GPU 显存的情况。
- 支持同时托管嵌入模型和大语言模型。

### [text-embeddings-inference](https://github.com/huggingface/text-embeddings-inference)

- 推荐通过 Docker 安装，也可本地编译后直接运行。
- 支持 GPU 和 CPU 运行。
- 仅支持嵌入模型（embeddings only）。

在 CPU 上运行 Qwen 嵌入模型时曾遇到一个 bug，使用以下命令可解决：

```bash
docker run -p 8080:80 -v hf_cache:/data --pull always ghcr.io/huggingface/text-embeddings-inference:cpu-ipex-latest --model-id Qwen/Qwen3-Embedding-0.6B --dtype float16
```

---

## 在线托管方法

大多数在线大模型服务均支持 OpenAI API 接口规范，因此可轻松与 Voyager 集成。

### [OpenRouter](https://openrouter.ai)

- 免费注册每日可获得 50 次免费模型调用。
- 一次性支付约 77 元人民币可升级至每日 1000 次免费调用。
- （1000 次免费调用约可支持 1.5 次完整训练流程。）