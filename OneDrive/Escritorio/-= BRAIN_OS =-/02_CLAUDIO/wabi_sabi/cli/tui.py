# wabi_sabi/cli/tui.py
"""
TUI Split-Screen Layout for Wabi-Sabi CLI
Layout "Cerebro": 3-pane split
- Left (70%): Chat history (scrollable, anchored input at bottom)
- Right Top: Sticky Plan Panel (context, plan, progress) - always visible
- Right Bottom: Live thinking/tool execution log
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
import threading
import time

@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: float = field(default_factory=time.time)

@dataclass
class PlanStep:
    description: str
    completed: bool = False
    in_progress: bool = False

class WabiTUI:
    def __init__(self, console=None):
        self.console = console or Console()
        self.layout = self._create_layout()
        self.chat_messages = []
        self.plan_steps = []
        self.current_model = "nvidia/llama-3.3-nemotron-super-49b-v1"
        self.current_provider = "nvidia"
        self.tokens_used = 0
        self.thinking_status = "idle"
        self.tool_log = []
        self.context_summary = ""
        self.session_refs = []
        self._live = None
        self._running = False
        self._input_thread = None
        self.prompt_session = PromptSession(history=InMemoryHistory())
        self.slash_commands = [
            "/model", "/use", "/continue", "/plans", "/status",
            "/providers", "/help", "/exit", "/new", "/init", "/brief",
            "/why", "/compact", "/think", "/run", "/plan"
        ]

    def _create_layout(self):
        layout = Layout(name="root")
        layout.split_row(
            Layout(name="chat", ratio=7, minimum_size=60),
            Layout(name="right", ratio=3, minimum_size=30)
        )
        layout["right"].split_column(
            Layout(name="plan", ratio=2, minimum_size=15),
            Layout(name="tools", ratio=1, minimum_size=8)
        )
        return layout

    def _render_chat(self):
        lines = []
        for msg in self.chat_messages[-50:]:
            if msg.role == "user":
                prefix = "[bold cyan]Luis>[/bold cyan] "
            elif msg.role == "assistant":
                prefix = "[bold green]Wabi>[/bold green] "
            elif msg.role == "tool":
                prefix = "[bold yellow]Tool>[/bold yellow] "
            else:
                prefix = f"[dim]{msg.role}>[/dim] "
            lines.append(Text.from_markup(prefix + msg.content))

        chat_text = Text()
        for line in lines:
            chat_text.append(line)
            chat_text.append("\n")

        return Panel(
            chat_text,
            title="[bold]CHAT[/bold]",
            subtitle=f"[dim]{len(self.chat_messages)} msgs[/dim]",
            border_style="blue"
        )

    def _render_plan(self):
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style="bold", width=3)
        table.add_column()

        if self.plan_steps:
            table.add_row("[bold]PLAN ACTIVO[/bold]", "")
            for i, step in enumerate(self.plan_steps, 1):
                if step.completed:
                    icon = "[green]✓[/green]"
                elif step.in_progress:
                    icon = "[yellow]⟳[/yellow]"
                else:
                    icon = "[dim]○[/dim]"
                table.add_row(f"{icon} {i}.", step.description)
        else:
            table.add_row("[dim]Sin plan activo[/dim]", "")

        table.add_row("", "")

        table.add_row("[bold]MODELO[/bold]", "")
        table.add_row("  Proveedor", f"{self.current_provider}")
        table.add_row("  Modelo", f"{self.current_model}")
        table.add_row("  Tokens", f"{self.tokens_used}")

        table.add_row("", "")

        table.add_row("[bold]ULTIMA ACCION[/bold]", "")
        if self.tool_log:
            for log in self.tool_log[-3:]:
                table.add_row("  ", f"[dim]{log}[/dim]")
        else:
            table.add_row("  ", "[dim]—[/dim]")

        table.add_row("", "")

        table.add_row("[bold]CONTEXTO[/bold]", "")
        if self.session_refs:
            for ref in self.session_refs[-3:]:
                table.add_row("  ", f"[dim]{ref}[/dim]")
        else:
            table.add_row("  ", "[dim]—[/dim]")

        return Panel(
            table,
            title="[bold]PLAN Y ESTADO[/bold]",
            border_style="green"
        )

    def _render_tools(self):
        lines = []

        if self.thinking_status != "idle":
            spinner_frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
            frame = int(time.time() * 10) % len(spinner_frames)
            spinner = spinner_frames[frame]
            lines.append(f"[bold yellow]{spinner} {self.thinking_status}[/bold yellow]")
            lines.append("")

        if self.tool_log:
            lines.append("[bold]HERRAMIENTAS[/bold]")
            for log in self.tool_log[-5:]:
                lines.append(f"  [dim]{log}[/dim]")

        tools_text = Text.from_markup("\n".join(lines)) if lines else Text("[dim]Esperando...[/dim]")

        return Panel(
            tools_text,
            title="[bold]PENSANDO / HERRAMIENTAS[/bold]",
            border_style="yellow"
        )

    def update_layout(self):
        self.layout["chat"].update(self._render_chat())
        self.layout["plan"].update(self._render_plan())
        self.layout["tools"].update(self._render_tools())

    def add_message(self, role: str, content: str):
        self.chat_messages.append(ChatMessage(role=role, content=content))
        self.update_layout()

    def set_plan(self, steps: List[str]):
        self.plan_steps = [PlanStep(desc) for desc in steps]
        self.update_layout()

    def update_plan_step(self, index: int, completed: bool = False, in_progress: bool = False):
        if 0 <= index < len(self.plan_steps):
            self.plan_steps[index].completed = completed
            self.plan_steps[index].in_progress = in_progress
            self.update_layout()

    def set_thinking(self, status: str):
        self.thinking_status = status
        self.update_layout()

    def clear_thinking(self):
        self.thinking_status = "idle"
        self.update_layout()

    def add_tool_log(self, log: str):
        self.tool_log.append(log)
        if len(self.tool_log) > 20:
            self.tool_log = self.tool_log[-20:]
        self.update_layout()

    def set_model(self, provider: str, model: str):
        self.current_provider = provider
        self.current_model = model
        self.update_layout()

    def add_session_ref(self, ref: str):
        self.session_refs.append(ref)
        self.update_layout()

    def set_context_summary(self, summary: str):
        self.context_summary = summary
        self.update_layout()

    def get_user_input(self) -> str:
        completer = WordCompleter(self.slash_commands, ignore_case=True)
        return self.prompt_session.prompt(
            "wabi> ",
            completer=completer,
            auto_suggest=AutoSuggestFromHistory()
        )

    def start(self):
        self._running = True
        self.update_layout()
        self._live = Live(self.layout, console=self.console, refresh_per_second=10, screen=True)
        self._live.start()

    def stop(self):
        self._running = False
        if self._live:
            self._live.stop()
            self._live = None

    def run_input_loop(self, handler):
        def input_loop():
            while self._running:
                try:
                    user_input = self.get_user_input()
                    if not user_input:
                        continue
                    if user_input in {"/exit", "exit", "salir"}:
                        self._running = False
                        break
                    handler(user_input)
                except (EOFError, KeyboardInterrupt):
                    self._running = False
                    break
                except Exception as e:
                    self.add_message("system", f"[red]Error: {e}[/red]")

        self._input_thread = threading.Thread(target=input_loop, daemon=True)
        self._input_thread.start()
        return self._input_thread

def demo_tui():
    tui = WabiTUI()
    tui.start()

    tui.add_message("user", "Hola Wabi, continua donde se quedó Opus")
    tui.set_plan([
        "Leer AGENTS.md",
        "Analizar HANDOFF",
        "Reportar pendientes"
    ])
    tui.add_session_ref("Opus: ultima sesion hace 3h")
    tui.add_session_ref("Sonet: handoff en 05_HANDOFF_legacy/")

    tui.set_thinking("INDEXANDO workspace...")
    time.sleep(1)
    tui.add_tool_log("read_file(AGENTS.md) OK 2.1KB")
    tui.update_plan_step(0, completed=True)
    tui.set_thinking("LEYENDO NEXT_SESSION_BRIEF.md...")
    time.sleep(1)
    tui.add_tool_log("read_file(NEXT_SESSION_BRIEF.md) OK 890B")
    tui.update_plan_step(1, completed=True)
    tui.set_thinking("PLANIFICANDO...")
    time.sleep(1)
    tui.add_message("assistant", "Encontre 3 pendientes de la sesion anterior con Opus:\n1. MOPN v14 - validar I1/T6g\n2. ositcore tests - suite 7 failing\n3. CLAUDIO - ws22 smoke test creado")
    tui.update_plan_step(2, completed=True)
    tui.clear_thinking()

    def handle_input(cmd):
        tui.add_message("user", cmd)
        if cmd.startswith("/model "):
            parts = cmd.split()
            if len(parts) > 1:
                tui.set_model("nvidia", parts[1])
                tui.add_message("system", f"Modelo cambiado a {parts[1]}")
        elif cmd == "/continue":
            tui.add_message("system", "Reconstruyendo contexto desde handoff...")
        elif cmd == "/status":
            tui.add_message("system", f"Provider: {tui.current_provider} | Modelo: {tui.current_model} | Tokens: {tui.tokens_used}")

    tui.run_input_loop(handle_input)
    tui._input_thread.join()
    tui.stop()

if __name__ == "__main__":
    demo_tui()