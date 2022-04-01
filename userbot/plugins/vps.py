import asyncio
import glob
import os

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _catutils

plugin_category = "tools"


# ============================@ Constants @===============================
config = "./config.py"
BADCAT = Config.BADCAT
var_checker = [
    "APP_ID",
    "PM_LOGGER_GROUP_ID",
    "PRIVATE_CHANNEL_BOT_API_ID",
    "PRIVATE_GROUP_BOT_API_ID",
]
exts = ["jpg", "png", "webp", "webm", "m4a", "mp4", "mp3", "tgs"]

cmds = [
    "rm -rf downloads",
    "mkdir downloads",
]
# ========================================================================


@catub.cat_cmd(
    pattern="(set|get|del) var ([\s\S]*)",
    command=("var", plugin_category),
    info={
        "header": "To manage config vars.",
        "flags": {
            "set": "To set new var in vps or modify the old var",
            "get": "To show the already existing var value.",
            "del": "To delete the existing value",
        },
        "usage": [
            "{tr}set var <var name> <var value>",
            "{tr}get var <var name>",
            "{tr}del var <var name>",
        ],
        "examples": [
            "{tr}get var ALIVE_NAME",
        ],
    },
)
async def variable(event):  # sourcery no-metrics
    """
    Manage most of ConfigVars setting, set new var, get current var, or delete var...
    """
    if not os.path.exists(config):
        return await edit_delete(
            event, "`There no Config file , You can't use this plugin.`"
        )
    cmd = event.pattern_match.group(1)
    string = ""
    match = None
    with open(config, "r") as f:
        configs = f.readlines()
    if cmd == "get":
        cat = await edit_or_reply(event, "`Getting information...`")
        await asyncio.sleep(1)
        variable = event.pattern_match.group(2).split()[0]
        for i in configs:
            if variable in i:
                return await cat.edit("**ConfigVars**:" f"\n\n`{i}`")
        await cat.edit(
            "**ConfigVars**:" f"\n\n__Error:\n-> __`{variable}`__ doesn't exists__"
        )
    elif cmd == "set":
        variable = "".join(event.text.split(maxsplit=2)[2:])
        cat = await edit_or_reply(event, "`Setting information...`")
        if not variable:
            return await cat.edit("`.set var <ConfigVars-name> <value>`")
        value = "".join(variable.split(maxsplit=1)[1:])
        variable = "".join(variable.split(maxsplit=1)[0])
        if variable not in var_checker:
            value = f'"{value}"'
        if not value:
            return await cat.edit("`.set var <ConfigVars-name> <value>`")
        await asyncio.sleep(1)
        for i in configs:
            if variable in i:
                string += f"    {variable} = {value}\n"
                match = True
            else:
                string += f"{i}"
        if match:
            await cat.edit(f"`{variable}` **successfully changed to  ->  **`{value}`")
        else:
            string += f"    {variable} = {value}\n"
            await cat.edit(
                f"`{variable}`**  successfully added with value`  ->  **{value}`"
            )
        with open(config, "w") as f1:
            f1.write(string)
            f1.close()
        await event.client.reload(cat)
    if cmd == "del":
        cat = await edit_or_reply(event, "`Deleting information...`")
        await asyncio.sleep(1)
        variable = event.pattern_match.group(2).split()[0]
        for i in configs:
            if variable in i:
                match = True
            else:
                string += f"{i}"
        with open(config, "w") as f1:
            f1.write(string)
            f1.close()
        if match:
            await cat.edit(f"`{variable}` **successfully deleted.**")
        else:
            await cat.edit(
                "**ConfigVars**:" f"\n\n__Error:\n-> __`{variable}`__ doesn't exists__"
            )
        await event.client.reload(cat)


@catub.cat_cmd(
    pattern="(re|clean)load$",
    command=("reload", plugin_category),
    info={
        "header": "To reload your bot in vps/ similar to restart",
        "flags": {
            "re": "To set new var in vps or modify the old var",
            "clean": "To show the already existing var value.",
        },
        "usage": [
            "{tr}reload",
            "{tr}cleanload",
        ],
    },
)
async def _(event):
    "To reload Your bot"
    cmd = event.pattern_match.group(1)
    cat = await edit_or_reply(event, "`Wait 2-3 min, reloading...`")
    if cmd == "clean":
        for file in exts:
            removing = glob.glob(f"./*.{file}")
            for i in removing:
                os.remove(i)
        for i in cmds:
            await _catutils.runcmd(i)
    await event.client.reload(cat)


@catub.cat_cmd(
    pattern="(good|bad)cat$",
    command=("switch", plugin_category),
    info={
        "header": "To switch between goodcat & badcat(For extra nsfw and gali).",
        "usage": [
            "{tr}goodcat",
            "{tr}badcat",
        ],
    },
)
async def variable(event):
    "To switch between good & bad cat"
    if not os.path.exists(config):
        return await edit_delete(
            event, "`There no Config file , You can't use this plugin.`"
        )
    string = ""
    match = None
    switch = "BADCAT"
    cmd = event.pattern_match.group(1).lower()
    with open(config, "r") as f:
        configs = f.readlines()
    for i in configs:
        if switch in i:
            match = True
        else:
            string += f"{i}"
    if cmd == "good":
        if match and not BADCAT:
            cat = await edit_or_reply(
                event, f"`Changing badcat to goodcat wait for 2-3 minutes.`"
            )
            with open(config, "w") as f1:
                f1.write(string)
                f1.close()
            await _catutils.runcmd("rm -rf badcatext")
            return await event.client.reload(cat)
        await edit_delete(event, "`You already using GoodCat`")
    elif cmd == "bad":
        if match and BADCAT:
            return await edit_or_reply(event, "`You already using BadCat`")
        string += f'    {switch} = "True"\n'
        cat = await edit_or_reply(
            event, "`Changing goodcat to badcat wait for 2-3 minutes.`"
        )
        with open(config, "w") as f1:
            f1.write(string)
            f1.close()
        await event.client.reload(cat)
