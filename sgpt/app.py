import os

from sgpt.codex_auth import (
    DEFAULT_CLIENT_ID,
    DEFAULT_ISSUER,
    DEFAULT_PORT,
    ensure_env_api_key,
    perform_login,
)

_disable_codex_fallback = os.getenv("SGPT_DISABLE_CODEX_FALLBACK", "").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

if not _disable_codex_fallback and "OPENAI_API_KEY" not in os.environ:
    try:  # pragma: no cover - environment and filesystem errors are non-deterministic
        ensure_env_api_key()
    except Exception:
        pass

# To allow users to use arrow keys in the REPL.
import readline  # noqa: F401
import sys
from typing import Optional

import typer
from click import BadArgumentUsage
from click.types import Choice
from prompt_toolkit import PromptSession

from sgpt.config import cfg
from sgpt.function import get_openai_schemas
from sgpt.handlers.chat_handler import ChatHandler
from sgpt.handlers.default_handler import DefaultHandler
from sgpt.handlers.repl_handler import ReplHandler
from sgpt.llm_functions.init_functions import install_functions as inst_funcs
from sgpt.role import DefaultRoles, SystemRole
from sgpt.utils import (
    get_edited_prompt,
    get_sgpt_version,
    install_shell_integration,
    run_command,
)


cli = typer.Typer(add_completion=False)


def _exit_with_error(message: str) -> None:
    typer.echo(f"Error: {message}")
    raise typer.Exit(code=2)


def main(
    prompt: str = typer.Argument(
        "",
        show_default=False,
        help="The prompt to generate completions for.",
    ),
    model: str = typer.Option(
        cfg.get("DEFAULT_MODEL"),
        help="Large language model to use.",
    ),
    temperature: float = typer.Option(
        0.0,
        min=0.0,
        max=2.0,
        help="Randomness of generated output.",
    ),
    top_p: float = typer.Option(
        1.0,
        min=0.0,
        max=1.0,
        help="Limits highest probable tokens (words).",
    ),
    md: bool = typer.Option(
        cfg.get("PRETTIFY_MARKDOWN") == "true",
        help="Prettify markdown output.",
    ),
    shell: bool = typer.Option(
        False,
        "--shell",
        "-s",
        help="Generate and execute shell commands.",
        rich_help_panel="Assistance Options",
    ),
    interaction: bool = typer.Option(
        cfg.get("SHELL_INTERACTION") == "true",
        help="Interactive mode for --shell option.",
        rich_help_panel="Assistance Options",
    ),
    describe_shell: bool = typer.Option(
        False,
        "--describe-shell",
        "-d",
        help="Describe a shell command.",
        rich_help_panel="Assistance Options",
    ),
    code: bool = typer.Option(
        False,
        "--code",
        "-c",
        help="Generate only code.",
        rich_help_panel="Assistance Options",
    ),
    functions: bool = typer.Option(
        cfg.get("OPENAI_USE_FUNCTIONS") == "true",
        help="Allow function calls.",
        rich_help_panel="Assistance Options",
    ),
    editor: bool = typer.Option(
        False,
        help="Open $EDITOR to provide a prompt.",
    ),
    cache: bool = typer.Option(
        True,
        help="Cache completion results.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        help="Show version.",
        callback=get_sgpt_version,
    ),
    chat: Optional[str] = typer.Option(
        None,
        help="Follow conversation with id, use \"temp\" for quick session.",
        rich_help_panel="Chat Options",
    ),
    repl: Optional[str] = typer.Option(
        None,
        help="Start a REPL (Read–eval–print loop) session.",
        rich_help_panel="Chat Options",
    ),
    show_chat: Optional[str] = typer.Option(
        None,
        help="Show all messages from provided chat id.",
        rich_help_panel="Chat Options",
    ),
    list_chats: bool = typer.Option(
        False,
        "--list-chats",
        "-lc",
        help="List all existing chat ids.",
        callback=ChatHandler.list_ids,
        rich_help_panel="Chat Options",
    ),
    role: Optional[str] = typer.Option(
        None,
        help="System role for GPT model.",
        rich_help_panel="Role Options",
    ),
    create_role: Optional[str] = typer.Option(
        None,
        help="Create role.",
        callback=SystemRole.create,
        rich_help_panel="Role Options",
    ),
    show_role: Optional[str] = typer.Option(
        None,
        help="Show role.",
        callback=SystemRole.show,
        rich_help_panel="Role Options",
    ),
    list_roles: bool = typer.Option(
        False,
        "--list-roles",
        "-lr",
        help="List roles.",
        callback=SystemRole.list,
        rich_help_panel="Role Options",
    ),
    install_integration: bool = typer.Option(
        False,
        help="Install shell integration (ZSH and Bash only)",
        callback=install_shell_integration,
        hidden=True,
    ),
    install_functions: bool = typer.Option(
        False,
        help="Install default functions.",
        callback=inst_funcs,
        hidden=True,
    ),
) -> None:
    stdin_passed = not sys.stdin.isatty()

    if stdin_passed:
        stdin = ""
        try:
            for line in sys.stdin:
                if "__sgpt__eof__" in line:
                    break
                stdin += line
        except EOFError:
            pass
        if not stdin:
            stdin_passed = False
        else:
            prompt = f"{stdin}\n\n{prompt}" if prompt else stdin
            try:
                if os.name == "posix":
                    sys.stdin = open("/dev/tty", "r")
                elif os.name == "nt":
                    sys.stdin = open("CON", "r")
            except OSError:
                pass

    if show_chat:
        ChatHandler.show_messages(show_chat, md)

    if sum((shell, describe_shell, code)) > 1:
        _exit_with_error(
            "Only one of --shell, --describe-shell, and --code options can be used at a time."
        )

    if chat and repl:
        _exit_with_error("--chat and --repl options cannot be used together.")

    if editor and stdin_passed:
        _exit_with_error("--editor option cannot be used with stdin input.")

    if editor:
        prompt = get_edited_prompt()

    role_class = (
        DefaultRoles.check_get(shell, describe_shell, code)
        if not role
        else SystemRole.get(role)
    )

    function_schemas = (get_openai_schemas() or None) if functions else None

    if repl:
        try:
            ReplHandler(repl, role_class, md).handle(
                init_prompt=prompt,
                model=model,
                temperature=temperature,
                top_p=top_p,
                caching=cache,
                functions=function_schemas,
            )
        except BadArgumentUsage as exc:
            _exit_with_error(str(exc))

    if chat:
        try:
            full_completion = ChatHandler(chat, role_class, md).handle(
                prompt=prompt,
                model=model,
                temperature=temperature,
                top_p=top_p,
                caching=cache,
                functions=function_schemas,
            )
        except BadArgumentUsage as exc:
            _exit_with_error(str(exc))
    else:
        full_completion = DefaultHandler(role_class, md).handle(
            prompt=prompt,
            model=model,
            temperature=temperature,
            top_p=top_p,
            caching=cache,
            functions=function_schemas,
        )

    session: PromptSession[str] = PromptSession()

    while shell and interaction:
        default_option = "e" if cfg.get("DEFAULT_EXECUTE_SHELL_CMD") == "true" else "a"
        try:
            option = typer.prompt(
                text="[E]xecute, [M]odify, [D]escribe, [A]bort",
                type=Choice(("e", "m", "d", "a", "y"), case_sensitive=False),
                default=default_option,
                show_choices=False,
                show_default=False,
            )
        except typer.Abort:
            option = default_option
        if option in ("e", "y"):
            run_command(full_completion)
        elif option == "m":
            full_completion = session.prompt("", default=full_completion)
            continue
        elif option == "d":
            DefaultHandler(DefaultRoles.DESCRIBE_SHELL.get_role(), md).handle(
                full_completion,
                model=model,
                temperature=temperature,
                top_p=top_p,
                caching=cache,
                functions=function_schemas,
            )
            continue
        break


@cli.command()
def login(
    open_browser: bool = typer.Option(
        True,
        "--browser/--no-browser",
        help="Open the authorization URL in your default browser.",
    ),
    port: Optional[int] = typer.Option(
        None,
        "--port",
        help="Preferred localhost port for the callback server.",
    ),
    issuer: str = typer.Option(
        DEFAULT_ISSUER,
        "--issuer",
        help="OAuth issuer.",
        hidden=True,
    ),
    client_id: str = typer.Option(
        DEFAULT_CLIENT_ID,
        "--client-id",
        help="OAuth client identifier.",
        hidden=True,
    ),
) -> None:
    desired_port = port if port is not None else DEFAULT_PORT
    success = perform_login(
        open_browser=open_browser,
        port=desired_port,
        issuer=issuer,
        client_id=client_id,
        echo=typer.echo,
    )
    if not success:
        raise typer.Exit(code=1)


def entry_point() -> None:
    args = sys.argv[1:]
    if args and args[0] == "login":
        cli()
    else:
        typer.run(main)


if __name__ == "__main__":
    entry_point()
