from __future__ import annotations

from textwrap import dedent

from wabi_sabi.agents.base_agent import AgentInput, AgentResult, BaseAgent
from wabi_sabi.core.programming import apply_python_patch
from wabi_sabi.core.tools import write_artifact


class ProgrammerAgent(BaseAgent):
    def run(self, agent_input: AgentInput) -> AgentResult:
        prompt = agent_input.prompt
        lowered = prompt.lower()
        if "archivo" in lowered and ("linea" in lowered or "lineas" in lowered or "línea" in lowered):
            code = self._file_summary_function()
            output = "Genere una funcion Python local para leer un archivo y resumir sus lineas."
            inference = ["El usuario probablemente queria un helper reutilizable para archivos de texto."]
        else:
            code = self._generic_module_template(agent_input.prompt)
            output = "Genere un borrador de codigo local."
            inference = ["El pedido necesita revision humana o integracion dirigida para tocar codigo existente."]

        if agent_input.options.get("apply"):
            target = agent_input.options.get("target")
            if not target:
                return AgentResult(
                    agent_name=self.name,
                    ok=False,
                    action="scoped_code_patch_missing_target",
                    output="Para programar sobre el arbol real se requiere --target con una ruta Python dentro del workspace.",
                    evidence=["apply_requested_without_target"],
                    certainty=["Wabi Sabi no aplico cambios al codigo fuente."],
                    inference=["El modo apply necesita alcance explicito para preservar el gate."],
                    unknown=["Ruta destino no indicada."],
                    error="missing_target",
                )
            try:
                patch = apply_python_patch(
                    workspace=self.config.workspace,
                    runtime_root=self.config.runtime_root,
                    target=target,
                    code=code,
                )
            except Exception as exc:
                return AgentResult(
                    agent_name=self.name,
                    ok=False,
                    action="scoped_code_patch_rejected",
                    output="ActionGate local rechazo o no pudo aplicar el parche acotado.",
                    evidence=[f"error={exc}"],
                    certainty=["No se aplico ningun cambio confirmado al destino solicitado."],
                    inference=["La ruta, extension o contenido no paso las restricciones locales."],
                    unknown=["Reintentar solo con una ruta .py dentro del workspace."],
                    error=str(exc),
                )
            artifacts = [str(patch.diff)]
            if patch.backup:
                artifacts.append(str(patch.backup))
            return AgentResult(
                agent_name=self.name,
                ok=True,
                action="scoped_code_patch_applied" if patch.changed else "scoped_code_patch_noop",
                output=f"{output} El cambio quedo aplicado de forma acotada en {patch.target}.",
                artifacts=artifacts,
                evidence=[
                    f"target={patch.target}",
                    f"before_sha256={patch.before_hash}",
                    f"after_sha256={patch.after_hash}",
                    f"diff_written={patch.diff}",
                    f"changed={patch.changed}",
                    patch.verification,
                ],
                certainty=[
                    "La escritura quedo limitada al target indicado.",
                    "Se genero diff y verificacion py_compile.",
                ],
                inference=inference,
                unknown=["No se ejecuto suite de pruebas completa; solo verificacion focal de sintaxis Python."],
            )

        if "archivo" in lowered and ("linea" in lowered or "lineas" in lowered or "línea" in lowered):
            artifact = write_artifact(self.config.output_dir, "programmer_file_summary", ".py", code)
            return AgentResult(
                agent_name=self.name,
                ok=True,
                action="safe_code_artifact_generated",
                output=output + " El codigo quedo como artefacto seguro, no se modifico codigo fuente del proyecto.",
                artifacts=[str(artifact)],
                evidence=[f"artifact_written={artifact}", "source_tree_not_modified_by_agent"],
                certainty=[
                    "La solicitud fue interpretada como generacion de codigo.",
                    "La escritura se limito a runtime/outputs.",
                ],
                inference=inference,
                unknown=["No se indico una ruta concreta para integrar el codigo en un modulo existente."],
            )
        artifact = write_artifact(self.config.output_dir, "programmer_draft", ".py", code)
        return AgentResult(
            agent_name=self.name,
            ok=True,
            action="safe_code_draft_generated",
            output="Genere un borrador de codigo local en runtime/outputs.",
            artifacts=[str(artifact)],
            evidence=[f"artifact_written={artifact}"],
            certainty=["La tarea fue enrutada al agente programador."],
            inference=inference,
            unknown=["No se detecto archivo destino especifico."],
        )

    def _file_summary_function(self) -> str:
        return dedent(
            '''
            from __future__ import annotations

            from pathlib import Path


            def summarize_file_lines(path: str | Path, preview_lines: int = 5) -> dict:
                """Read a text file and return a compact line summary."""
                file_path = Path(path)
                text = file_path.read_text(encoding="utf-8", errors="replace")
                lines = text.splitlines()
                return {
                    "path": str(file_path),
                    "line_count": len(lines),
                    "empty_lines": sum(1 for line in lines if not line.strip()),
                    "first_lines": lines[:preview_lines],
                    "last_lines": lines[-preview_lines:] if preview_lines else [],
                }
            '''
        ).lstrip()

    def _generic_module_template(self, prompt: str) -> str:
        escaped = prompt.replace('"""', '\\"\\"\\"')
        return dedent(
            f'''
            """Generated Wabi Sabi code draft.

            Original request:
            {escaped}
            """


            def run() -> str:
                return "TODO: complete this local implementation after selecting a target file."


            if __name__ == "__main__":
                print(run())
            '''
        ).lstrip()
