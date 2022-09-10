def get_command_help(cmd):
    prefix = ""

    if cmd.parent is not None:
        prefix = f"{cmd.parent.name} {cmd.name}"
    else:
        prefix = f"{cmd.name}"
    
    return prefix

def generate_help_pages(bot, cog):
    pages = []
    commands = bot.get_cog(cog).walk_commands()
    commands_formatted = []
    commands_2 = []
    spacing = 0

    for cmd in commands:
        if cmd.name.lower() != cog.lower():
            prefix = get_command_help(cmd)

            if len(prefix) > spacing:
                spacing = len(prefix)

            commands_2.append([prefix, cmd.description])

    for cmd in commands_2:
        commands_formatted.append(f"{cmd[0]}{' ' * (spacing - len(cmd[0]))} :: {cmd[1]}")

    commands_str = ""
    for cmd in commands_formatted:
        if len(commands_str) + len(cmd) > 1000:
            pages.append(commands_str)
            commands_str = ""

        commands_str += f"{cmd}\n"

    if len(commands_str) > 0:
        pages.append(commands_str)

    return pages