#     Copyright (C) 2023  Coretex LLC

#     This file is part of Coretex.ai

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Any, List, Optional, Union

from tabulate import tabulate

import click
import inquirer

from ...node import NodeMode
from ...configuration import NodeConfiguration


def clickPrompt(
    text: str,
    default: Any = None,
    type: Optional[Union[type, click.ParamType]] = None,
    **kwargs: Any
) -> Any:

    return click.prompt(click.style(f"\n\U00002754 {text}", fg = "cyan"), default = default, type = type, **kwargs)


def arrowPrompt(choices: List[Any], message: str) -> Any:
    click.echo("\n")
    answers = inquirer.prompt([
        inquirer.List(
            "option",
            message = message,
            choices = choices,
        )
    ])

    return answers["option"]


def previewNodeConfig(nodeConfig: NodeConfiguration) -> None:
    allowDocker = "Yes" if nodeConfig.allowDocker else "No"

    if nodeConfig.secret is None or nodeConfig.secret == "":
        nodeSecret = ""
    else:
        nodeSecret = "********"

    table = [
        ["Node name",               nodeConfig.name],
        ["Node image",              nodeConfig.image],
        ["Storage path",            nodeConfig.storagePath],
        ["RAM",                     f"{nodeConfig.ram}GB"],
        ["SWAP memory",             f"{nodeConfig.swap}GB"],
        ["POSIX shared memory",     f"{nodeConfig.sharedMemory}GB"],
        ["CPU cores allocated",     f"{nodeConfig.cpuCount}"],
        ["Node mode",               f"{NodeMode(nodeConfig.mode).name}"],
        ["Docker access",           allowDocker],
        ["Node secret",             nodeSecret],
        ["Node init script",        nodeConfig.initScript if nodeConfig.initScript is not None else ""],
        ["Node heartbeat interval", f"{nodeConfig.heartbeatInterval // 1000}s"]
    ]
    if nodeConfig.modelId is not None:
        table.append(["Coretex Model ID", f"{nodeConfig.modelId}"])

    if nodeConfig.nearWalletId is not None:
        table.append(["NEAR wallet id", nodeConfig.nearWalletId])

    if nodeConfig.endpointInvocationPrice is not None:
        table.append(["Endpoint invocation price", f"{nodeConfig.endpointInvocationPrice}"])

    stdEcho(tabulate(table))


def outputUrl(baseUrl: str, entityUrl: str) -> str:
    return ("\033[4m" + f"{baseUrl}/{entityUrl}" + "\033[0m")


def stdEcho(text: str) -> None:
    click.echo(click.style(f"\n{text}", fg = "cyan"))


def warningEcho(text: str) -> None:
    click.echo(click.style(f"\nWARNING: {text}", fg = "yellow"))


def successEcho(text: str) -> None:
    click.echo(click.style(f"\n\U0001F680 {text} \U0001F680", fg = "green"))


def progressEcho(text: str) -> None:
    click.echo(click.style(f"\n\U00002699 {text} \U00002699", fg = "yellow"))


def errorEcho(text: str) -> None:
    click.echo(click.style(f"\n\U0000274C {text} \U0000274C", fg = "red"))


def highlightEcho(text: str) -> None:
    click.echo(click.style(f"\n\U00002755 {text} \U00002755"))
