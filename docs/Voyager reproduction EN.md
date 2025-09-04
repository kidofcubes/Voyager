

# Voyager
## installation

First, install [uv](https://docs.astral.sh/uv/) and [npm](https://nodejs.org) (npm version used during testing was v24.4.1)

installation on Linux (The windows process should be fairly similar):
```bash
git clone https://github.com/kidofcubes/Voyager.git
uv venv --python 3.13.5
source .venv/bin/activate
uv pip install -e .
cd voyager/env/mineflayer
npm install
cd mineflayer-collectblock
npx tsc
cd ..
npm install
```


Note: The main Voyager class has been restructured from the original to make editing the configuration of each LLM and embedding instance easier.

## quickstart

### jupyter lab (recommended)

`$ jupyter lab --port 9998 --ip=0.0.0.0`
click/copy the resulting link from the terminal into your browser, and open up training.ipynb.

### directly use python script
the training.py script has been setup to connect to minecraft on port 25565 by default, along with `meta-llama/llama-3.1-405b-instruct:free` from openrouter for it's AI and `Qwen/Qwen3-Embedding-8B` for its embeddings.

for your first test run, you should be able to get away with setting up the environment variables `HUGGINGFACEHUB_API_TOKEN` to your huggingface token, and setting your `OPENAI_API_KEY` to your https://openrouter.ai token like so:

`HUGGINGFACEHUB_API_TOKEN=hf_token_here OPENAI_API_KEY=sk-or-v1-openrouter_token_here python train.py`
(You will need port 3000 to be free for MineFlayer, and of course, a minecraft server/instance running on port 25565)

(The free credits you get from both on a fresh account should be enough to test if the program is working, but not nearly enough to get you through an entire training session)

# minecraft (Java Edition only)

## client hosting/singleplayer hosting (Open to lan option)
A Microsoft account with minecraft technically isn't required, but you will have to use an alternative launcher like [Prism](https://prismlauncher.org/) to launch Minecraft in offline mode.

To add an offline only account on Prism Launcher without an account, add a file `accounts.json` to your Prism Launcher folder
on linux, the path i got was `/home/usernamehere/.local/share/PrismLauncher/accounts.json`

`account.json`
```json
{"accounts": [{"entitlement": {"canPlayMinecraft": true,"ownsMinecraft": true},"type": "MSA"}],"formatVersion": 3}
```

Install a minecraft launcher, and install 1.19.4 fabric.
(Prism Launcher is recommended to make installation of the mods and configs easier, though most launchers should work)

Install the mods `Multiplayer Server Pause`, `Better Respawn`,  `Mod Menu` and their dependencies (All of them can be found on [modrinth](https://modrinth.com/))
Exact versions used: 
- Minecraft: 1.19.4
- Fabric-Loader: 0.17.2
- Fabric-Api: 0.87.2+1.19.4
- Mod Menu: 1.0.3
- Multiplayer Server Pause: 1.3.1
- iChunUtil: 1.0.3
- Better Respawn: 1.19.4-2.0.2
(Installation is done by placing the jar files into the `minecraft_folder/mods` folder)

Set the better_respawning config (found in `minecraft_folder/config/better_respawn/better_respawn.properties`) to 
```ini
# The maximum distance to spawn the player away from its death location
max_respawn_distance=32
# The minimum distance to spawn the player away from its death location
min_respawn_distance=0
# If the player is in this range of its bed/respawn anchor it will respawn there
respawn_block_range=32
```

Start up the game, select `Singleplayer` and create a new world.
Set Game Mode to `Creative` and Difficulty to `Peaceful`.
After the world is created, press `Esc` and select `Open to LAN`.
Select `Allow cheats: ON` and press `Start LAN World`.
You will see a port number in the chat log, that is your `mc-port`.


## dedicated server hosting (Requires a java 17 installation)
  Download the installer for the correct fabric and minecraft version from [here](https://fabricmc.net/use/server/), or just run the below in a new folder
```bash
curl -OJ https://meta.fabricmc.net/v2/versions/loader/1.19.4/0.17.2/1.1.0/server/jar
java -Xmx2G -jar fabric-server-mc.1.19.4-loader.0.17.2-launcher.1.1.0.jar nogui
```
Edit the `server.properties` file generated after the server's first run, and change these values
```ini
difficulty=peaceful
gamemode=survival
online-mode=false
enable-rcon=true # Only needed if you wish to use RCON features
rcon.password=hunter2
rcon.port=25575
spawn-protection=0 # This is important, otherwise the bot can't do anything near the spawn
```

Then, install the mods listed above in the client hosting section, placing all the jar files inside the `mods` folder generated after the first run of the server
Configure better_respawn in the same way, and then start the server again.

## [azure](https://github.com/MineDojo/Voyager/blob/main/installation/minecraft_instance_install.md#option-1-microsoft-azure-login-recommended) (Untested)
  This is the recommended method by the original Voyager project, though I haven't had the opportunity to test it.

  The readme mentions that:
  > Using this method will allow Voyager to automatically resume when there's a request timeout.

  But I don't think I've run into this issue so far hosting locally.


# AI integration

## self hosting
initial testing was done on a 12gb 3060, Qwen3-14B-Q4_K_M gguf is about the largest that can fit and run at a somewhat reasonable speed (~26 tokens per second on llama.cpp)

### [vllm](https://docs.vllm.ai/en/v0.10.1/getting_started/quickstart.html)
install in its own virtual environment elsewhere (Also linux only, so you'll have to run wsl if you're on windows)
can host both embeddings and llms
  
### [llama.cpp](https://github.com/ggml-org/llama.cpp) (GGUF only)
easily installed as a binary on both windows and linux
suitable for when your model is too large to fit all into gpu memory
can host both embeddings and llms
  
### [text-embeddings-interface](https://github.com/huggingface/text-embeddings-inference)
primarily installed with docker, though it can also be built locally to run directly
runnable both on and off gpu, embeddings only

a bug was experienced when running qwen embeddings on cpu, using this command helped
`docker run -p 8080:80 -v hf_cache:/data --pull always ghcr.io/huggingface/text-embeddings-inference:cpu-ipex-latest --model-id Qwen/Qwen3-Embedding-0.6B --dtype float16`

## online methods
most online llm hosting endpoints support the OpenAI api schema, so most of them are easily usable with Voyager

### [openrouter](https://openrouter.ai)
free signup gets you 50 requests on free models a day, one time payment of ~77rmb ups it to 1k requests on free models a day
(1k free requests can run ~1.5 full training sessions)