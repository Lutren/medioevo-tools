# MEDIOEVO: Una teoría de información digital para sistemas agentes

Estado: `BORRADOR_PUBLICO_SEGURO_v0_1`

Este es un borrador breve y público-seguro. No incluye manuscritos privados,
datasets privados, secretos, prompts internos, material protegido de runtime ni
canon no publicado.

## 1. Prefacio

La teoría de la información dio a la computación una gramática durable: fuente,
mensaje, canal, receptor, ruido, redundancia, compresión y capacidad. Esa
gramática sigue siendo necesaria. Explica por qué una señal se degrada, por qué
la codificación importa, por qué la redundancia puede ayudar y por qué todo
canal tiene límites.

Los sistemas agentes agregan un problema práctico. El receptor ya no es solo
un receptor. Es un operador con memoria, herramientas, permisos, objetivos,
incertidumbre y capacidad de actuar. Un agente de software puede leer un
mensaje, clasificarlo, buscar evidencia, escribir un archivo, llamar una
herramienta, delegar trabajo, publicar contenido o detenerse porque la acción
es insegura. En ese entorno, la información no queda completa cuando llega.
Se vuelve operacional cuando el sistema sabe qué es el mensaje, qué evidencia
lo sostiene, qué acciones están permitidas, qué riesgos quedan y qué estado
debe transferirse al siguiente agente o sesión.

MEDIOEVO se propone aquí como una extensión de teoría de información digital
para sistemas agentes. No reemplaza la teoría clásica de la información.
Extiende la capa operacional que la rodea.

La idea central es simple:

```txt
Información para agentes = mensaje + estado del observador + evidencia +
                           permiso + reversibilidad + residuo + handoff.
```

Este libro es breve por diseño. Define los conceptos, ofrece fórmulas, conecta
la teoría con un runtime mínimo y deja fuera los claims fuertes que no
pertenecen a esta obra.

## This Is Not Theoretical Physics

Este libro no afirma actualizar la mecánica cuántica, la relatividad, la
termodinámica, la física del espacio-tiempo ni la ontología física.

Actualiza teoría de información digital en la capa operacional de agentes,
software, lenguaje, coordinación, memoria, evidencia y acción.

Cualquier analogía física es una metáfora salvo que se formalice y se pruebe
por separado en un trabajo específico de física. Si una obra futura usa
términos de física, debe definir otro alcance, otra evidencia y otros
criterios de falsación. Esa obra no es este libro.

## 2. De Shannon a la información agente

El modelo clásico describe comunicación como movimiento de un mensaje desde
una fuente hasta un destino a través de un canal. El ruido puede corromper el
mensaje. La codificación, la redundancia y la compresión pueden mejorar la
entrega. La capacidad limita cuánto puede transmitirse.

Ese modelo sigue siendo esencial. Un prompt, un archivo, un log, una
instrucción de usuario, una fila de base de datos y el resultado de una
herramienta son mensajes que se mueven por canales. Pueden comprimirse,
corromperse, truncarse, duplicarse, malinterpretarse o retrasarse.

Pero los sistemas agentes cambian el destino. El destino no es solo un lugar
donde cae el mensaje. Es un observador activo. Trae estado de trabajos
anteriores. Tiene herramientas. Puede modificar el entorno. Puede aumentar o
reducir riesgo.

En un modelo de receptor pasivo, la pregunta principal es: ¿llegó el mensaje?

En un modelo de receptor agente, la pregunta cambia:

```txt
¿Puede este observador usar esta información correctamente, con seguridad y
con continuidad?
```

Esa pregunta requiere más campos que el modelo clásico:

- estado del observador;
- clasificación de afirmaciones;
- estado de evidencia;
- permiso de acción;
- reversibilidad;
- ruido residual R;
- eficiencia efectiva Phi_eff;
- GhostGate antes de actuar;
- ActionGate antes de ejecutar;
- WitnessLog para verificabilidad externa;
- Source Cards para anclar evidencia;
- Handoff para continuidad;
- TaskContract para episodios de trabajo.

El canal extendido es:

```txt
fuente -> mensaje -> canal -> estado del observador -> clasificación
       -> estado de evidencia -> Source Card -> GhostGate -> ActionGate
       -> acción o pausa -> WitnessLog -> Handoff -> siguiente observador/sesión
```

## 3. El observador como filtro operacional

Un agente nunca observa desde cero. Observa desde un estado.

El mismo mensaje puede producir resultados distintos según lo que el observador
ya sabe, qué herramientas puede usar, qué permisos tiene, qué archivos están
en alcance, qué tarea está activa y qué riesgos están bloqueados. No es una
afirmación mística. Es un hecho operacional.

El estado de un observador incluye:

- memoria disponible;
- contrato de tarea actual;
- herramientas disponibles;
- herramientas bloqueadas;
- alcance local de archivos;
- evidencia previa;
- incógnitas no resueltas;
- formato de salida esperado;
- obligaciones de handoff.

Si el estado del observador es confuso, el sistema puede actuar sobre supuestos
obsoletos. Si el alcance de herramientas es confuso, puede hacer una escritura
insegura. Si la evidencia es confusa, puede promover inferencia como certeza.

MEDIOEVO trata al observador como filtro entre mensaje y acción. El filtro no
solo decodifica. Clasifica y aplica gates.

## Definiciones formales

**Átomo de información**: la unidad operacional mínima que puede clasificarse,
vincularse a evidencia, usarse para actuar o transferirse por handoff. Puede
ser una afirmación, tarea, restricción, observación, decisión o resultado.

**Observador**: un agente o sesión humano-agente que recibe información desde
un estado específico: memoria, contexto de tarea, permisos, herramientas,
evidencia previa e incertidumbre actual.

**Canal**: el medio y protocolo por el cual un átomo de información se mueve
entre fuente, observador, herramienta, agente, usuario, memoria o handoff.

**Ruido**: cualquier factor que reduce la interpretación correcta o la acción
segura: incertidumbre, ambigüedad, contradicción, evidencia faltante, estado
obsoleto, exceso de contexto, confusión de permisos o costo de coordinación.

**Residuo R**: ruido operacional acumulado que queda después de observar,
clasificar, coordinar e intentar cerrar una tarea.

**Phi_eff**: eficiencia informacional efectiva; relación entre salida útil
verificada y costo total de coordinación.

**Afirmación**: enunciado que puede ser verdadero, falso, parcial, incierto,
obsoleto o fuera de alcance, y por eso debe clasificarse antes de usarse.

**Source Card**: ancla compacta de evidencia que describe de dónde viene una
afirmación, qué tipo de fuente es, cuándo se capturó, su confianza y los
límites de uso.

**WitnessLog**: registro append-only de observaciones, decisiones, acciones,
resultados, gates y resúmenes de evidencia que hace verificable el trabajo de
agentes sin exponer material privado.

**GhostGate**: compuerta de planificación previa a la acción. Permite leer,
listar, buscar, inspeccionar y proponer, pero bloquea ejecución, escrituras,
publicación, red y operaciones destructivas.

**ActionGate**: compuerta de ejecución que decide `APPROVE`, `REVIEW` o
`BLOCK` según evidencia, reversibilidad, riesgo, privacidad y alcance.

**Handoff**: estado mínimo suficiente para que otro agente o sesión continúe
sin releer todo.

**TaskContract**: frontera explícita de un episodio de trabajo: objetivo,
acciones permitidas, acciones bloqueadas, evidencia requerida, salida esperada
y criterios de cierre.

**Protocolo de agente**: reglas repetibles para que agentes reciban tareas,
clasifiquen afirmaciones, usen herramientas, coordinen, registren evidencia y
cierren trabajo.

**Protocolo institucional**: patrón de gobernanza humana adaptado a agentes,
como TPS, mantenedores de Linux, Wikipedia, tribunal, gremio, laboratorio o
commenda.

## 4. R: residuo informacional

Residuo es lo que queda cuando la información no se ha resuelto por completo
en estado verificado, acción segura o cierre útil.

Residuo no es solo error. Incluye incertidumbre, contradicción, evidencia
faltante, ambigüedad, estado obsoleto, riesgo irreversible y costo de
coordinación. Una respuesta puede sonar fluida y aun así producir residuo alto
si no puede verificarse, si ignora una frontera de permisos o si deja al
siguiente agente sin poder continuar.

MEDIOEVO usa R como señal operacional. R alto significa: deja de abrir nuevas
features y cierra el ciclo. Verifica, documenta, reduce alcance, produce
handoff o pide revisión.

La fórmula básica es:

```txt
R_total =
  w_u * uncertainty
+ w_c * contradiction
+ w_m * missing_evidence
+ w_a * ambiguity
+ w_s * stale_state
+ w_i * irreversible_risk
+ w_o * coordination_overhead
```

Cada término se normaliza a `[0, 1]`. Los pesos dependen de la tarea. Un
análisis local de solo lectura puede tolerar más incertidumbre que una
publicación externa, acción de pago, cambio de credenciales o limpieza
destructiva.

R sirve porque convierte una incomodidad vaga en una señal operativa medible.

## 5. Phi_eff: eficiencia informacional efectiva

La eficiencia clásica suele medir compresión, rendimiento o costo. La
eficiencia agente debe medir utilidad verificada en relación con costo de
coordinación.

```txt
Phi_eff = verified_useful_output / total_coordination_cost
```

Salida útil verificada incluye:

- archivos creados o actualizados con evidencia;
- pruebas que pasan;
- decisiones registradas con razones;
- afirmaciones enlazadas a Source Cards;
- tareas cerradas con criterios de aceptación;
- handoff que permite continuar a otra sesión.

El costo de coordinación incluye:

- tokens;
- tiempo;
- llamadas de herramientas;
- reintentos;
- bucles de aclaración;
- eventos de revisión;
- comandos fallidos;
- costo de rollback;
- conflicto entre agentes.

Phi_eff no es una puntuación universal. Es una señal de runtime. Si baja, el
sistema debe dejar de producir volumen y volver al cierre verificable.

## 6. Afirmaciones, evidencia y Source Cards

Los sistemas agentes producen afirmaciones. Resumen, infieren, planean,
clasifican y recomiendan. Sin una capa de afirmaciones, mezclan hechos
verificados, conjeturas, memoria obsoleta y enunciados sin soporte.

MEDIOEVO usa cuatro categorías operacionales:

- `CERTEZA`: verificada directamente con evidencia;
- `INFERENCIA`: conclusión razonable desde evidencia, marcada como tal;
- `INCOGNITA`: estado desconocido o no verificado;
- `BLOQUEO`: inseguro, privado, destructivo, externo o fuera de alcance.

Una Source Card ancla una afirmación sin copiar la fuente completa. Puede
contener:

```txt
source_id
source_type
location
captured_at
claim_supported
confidence
boundary
hash_or_excerpt
```

La Source Card es pequeña, pero cambia el comportamiento del sistema. Obliga al
agente a distinguir qué sabe de dónde lo sabe.

## 7. GhostGate y ActionGate

GhostGate es la compuerta previa a la acción. Puede planear. No puede ejecutar.
Puede leer, listar, buscar, inspeccionar, comparar y proponer. No puede
escribir, publicar, ejecutar shell, hacer push, usar credenciales ni disparar
efectos externos.

ActionGate es la compuerta de ejecución. Decide si una acción concreta puede
proceder.

```txt
APPROVE si:
  R <= threshold
  y la evidencia es suficiente
  y la reversibilidad es suficiente
  y no se toca una frontera bloqueada

REVIEW si:
  la evidencia es parcial
  o la reversibilidad es parcial
  o el alcance es externo/legal/publicación/pagos/proveedor/canal

BLOCK si:
  existe riesgo técnico concreto
  o se detecta exposición de secretos/datos privados
  o se pide acción destructiva sin gate
  o se detecta publicación sin revisión
```

En `claudio-agent-runtime`, esto aparece como:

- `ghostgate tools`;
- `ghostgate check`;
- `permissions check`;
- `execute write`;
- `rollback restore`.

La implementación actual está limitada intencionalmente: escrituras locales
reversibles. Shell, git write, red, publicación, scheduler, daemon y canales
externos quedan fuera hasta tener gates separados.

## 8. WitnessLog y estado verificable

El trabajo de agentes debe poder observarse sin exponer material privado.
WitnessLog es el registro append-only para ese propósito.

Registra:

- comando;
- event id;
- timestamp;
- decisión de ActionGate;
- estado;
- resumen redactado del resultado;
- digest del output cuando es útil.

WitnessLog no necesita guardar contenido privado completo. De hecho, no debe.
Debe guardar lo suficiente para verificar que la acción ocurrió, qué gate se
aplicó y cómo otro operador puede auditar el camino.

Así el trabajo agente se vuelve inspeccionable sin convertirse en fuga.

## 9. Handoff como codec de continuidad

Handoff es compresión para continuidad operacional.

```txt
Handoff = estado mínimo suficiente para que otro agente/sesión
          continúe sin releer todo
```

El objetivo no es conservar cada token. El objetivo es conservar el estado
necesario para continuar con seguridad:

- estado actual;
- hechos verificados;
- inferencias;
- incógnitas;
- archivos tocados;
- pruebas corridas;
- gates aplicados;
- siguiente acción.

Handoff previene pérdida de operador. Los datos persisten. El operador no.

## 10. Instituciones humanas como protocolos de agentes

Las instituciones humanas son tecnologías de coordinación. MEDIOEVO las usa
como biblioteca de protocolos para agentes.

TPS aporta trabajo estándar, problemas visibles y ciclos de mejora. Los
mantenedores de Linux aportan ownership de parches, revisión, disciplina de
release y confianza acumulada. Wikipedia aporta normas de citación, tono
neutral, historial de revisión y manejo de disputas. La lógica de tribunal
aporta afirmaciones, evidencia, carga de prueba y revisión adversarial. Los
gremios aportan transmisión de habilidad y estándares de oficio. El laboratorio
aporta hipótesis, experimento, registro y replicación. La commenda aporta
delegación acotada de riesgo, capital y agencia.

La idea práctica es directa: los agentes necesitan instituciones, no solo
prompts.

## 11. DUAT Operator Shell

DUAT Operator Shell es la capa humana/producto para operar agentes. El kernel
técnico es `claudio-agent-runtime`.

El shell debe exponer:

- reporte `doctor/status`;
- estado de permisos;
- estado de GhostGate plan;
- estado de ActionGate execute;
- estado de WitnessLog;
- estado de memoria;
- task board;
- registro de skills;
- estado de rollback;
- presupuesto futuro R/Phi.

El shell no es una interfaz mística. Es una consola operacional para
información agente.

## 12. Ruta mínima de implementación

La ruta mínima es:

1. crear una raíz local de runtime;
2. implementar checks de permisos;
3. implementar GhostGate plan;
4. implementar ActionGate execute para escrituras locales reversibles;
5. implementar rollback;
6. implementar WitnessLog JSONL;
7. implementar resúmenes de memoria;
8. implementar task board;
9. implementar carga de metadata de skills;
10. implementar handoff;
11. implementar presupuesto R/Phi desde evidencia de runtime.

El kernel actual ya cubre la primera capa práctica. El siguiente paso es
calcular R/Phi desde task board, memoria, witness log, resultados de comandos,
uso de rollback, evidencia faltante y eventos REVIEW/BLOCK.

## 13. Falsabilidad y benchmarks

Esta teoría debe probarse operacionalmente.

Benchmarks posibles:

- ¿R baja después de agregar Source Cards?
- ¿Phi_eff sube cuando mejora el handoff?
- ¿Los agentes hacen menos escrituras inseguras con GhostGate?
- ¿Las decisiones REVIEW/BLOCK son consistentes entre tareas similares?
- ¿Una segunda sesión puede continuar más rápido desde handoff que desde logs
  crudos?
- ¿WitnessLog permite auditar sin exponer contenido privado?
- ¿Rollback reduce riesgo irreversible?

Si estas pruebas fallan, el sistema debe revisarse. Una teoría útil de
información agente debe mejorar el trabajo, no solo describirlo.

## 14. Conclusión

MEDIOEVO extiende la teoría de información digital para agentes al agregar la
capa operacional faltante: estado del observador, clasificación de
afirmaciones, anclaje de evidencia, permiso, reversibilidad, residuo,
eficiencia, testigo y handoff.

El resultado no es física teórica. Es una teoría práctica para agentes de
software que leen, deciden, coordinan y actúan.

El principio central es:

```txt
No maximizar salida. Maximizar cierre verificable.
```

En sistemas agentes, la información no queda completa cuando se transmite.
Queda completa cuando puede verificarse, usarse con seguridad, registrarse y
transferirse.

