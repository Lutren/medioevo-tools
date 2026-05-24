import { useState, useMemo, useRef, useEffect, useCallback } from "react";
import type { Mode, TileType, CityState } from "./core/types";
import type { ViewMode } from "./graphics/types";
import type { ReviewedAssetsManifest } from "./graphics/assetManifestLoader";
import { createCity, placeTile, eraseTile } from "./sim/city";
import { tickEngine } from "./sim/engine";
import { defaultCamera } from "./render/camera";
import { useCameraController } from "./render/useCameraController";
import { applyCameraPreset, centerOnSelectedAgent, mostCriticalAgent } from "./render/cameraPresets";
import { computeLOD } from "./render/lod-controller";
import { Topbar } from "./components/Topbar";
import { Toolbar } from "./components/Toolbar";
import { MainCanvas } from "./components/MainCanvas";
import { CityPanel } from "./components/CityPanel";
import { AgentInspector } from "./components/AgentInspector";
import { BuildingInspector } from "./components/BuildingInspector";
import { RPGBuilderPanel } from "./components/RPGBuilderPanel";
import { OSITPanel } from "./components/OSITPanel";
import { HandoffPanel } from "./components/HandoffPanel";
import { EventLogPanel } from "./components/EventLogPanel";
import {
  loadPrefs,
  savePrefs,
  downloadJson,
  saveCityToJson,
  loadCityFromJson,
} from "./core/persistence";
import { computeGraphicsBudget, estimateGraphicsMetrics } from "./graphics/graphicsMetrics";
import { loadReviewedAssetsManifest } from "./graphics/assetManifestLoader";
import { createSpriteResolver } from "./graphics/spriteResolver";
import { useFpsSampler } from "./performance/useFpsSampler";
import { createPerformanceBenchmarkOutput } from "./performance/performanceOverlay";
import { defaultRenderCounters, type FpsSnapshot } from "./performance/performanceTypes";
import {
  pixelResolutionForQuality,
  V11_BENCHMARK_SCENARIOS,
  type PerformanceBenchmarkV11Document,
  type PerformanceBenchmarkV11Result,
} from "./performance/benchmarkV11";
import {
  pixelResolutionForQualityV111,
  V111_BENCHMARK_SCENARIOS,
  type BenchmarkBrowserMode,
  type BenchmarkFocusStatus,
  type PerformanceBenchmarkV111Document,
  type PerformanceBenchmarkV111Result,
  type PerformanceBenchmarkV111Scenario,
} from "./performance/benchmarkV111";
import type { PixelRealismConfig } from "./pixelRealism/renderPasses";
import { defaultPixelRealismConfig, normalizeQualityForView } from "./pixelRealism/renderPasses";
import { createPixelRealismRuntime } from "./pixelRealism/pixelRealismMetrics";
import type { VibeSceneConfig } from "./vibecoding/vibeTypes";
import { compileVibeScene, vibeToPixelRealismConfig } from "./vibecoding/vibeSceneCompiler";
import { createVibeUndoSnapshot, restoreVibeUndoSnapshot, type VibeUndoSnapshot } from "./vibecoding/vibeHistory";
import { exportRPGWorld } from "./rpg/worldExport";
import type { PlayableLightKind, PlayableMaterial, PlayableSceneState, SceneInteractionTool } from "./scene/sceneTypes";
import {
  applyVibeSceneToPlayableScene,
  createDefaultPlayableSceneState,
  deserializePlayableScene,
  eraseSceneAt,
  makeAgentLoadState,
  placeSceneLight,
  placeSceneMaterial,
  selectSceneAt,
  serializePlayableScene,
  setSceneTime,
  setSceneWeather,
  stepPlayableScene,
} from "./scene/sceneState";
import { runPlayableInteractionQaSequence, type PlayableInteractionQaResult } from "./scene/playableInteractionQa";
import { parseVibeCommand } from "./vibecoding/vibeCommandParser";
import { applyVibeGamePatch } from "./vibecoding/vibeGameActions";
import "./styles.css";

const INIT_STATE = createCity();
const INIT_CAMERA = defaultCamera(INIT_STATE.width, INIT_STATE.height);
const INITIAL_PARAMS = typeof window !== "undefined" ? new URLSearchParams(window.location.search) : new URLSearchParams();
const INITIAL_VIBE_ID = INITIAL_PARAMS.get("vibe") ?? "sunny_castle_lake";
const INITIAL_VIBE = compileVibeScene(INITIAL_VIBE_ID, "preset").config;
const INITIAL_SCENE_DEMO = INITIAL_PARAMS.get("sceneDemo");
const INITIAL_BENCHMARK_STATIC = INITIAL_PARAMS.get("benchmarkStatic") === "1" || INITIAL_PARAMS.get("perfStatic") === "1";

export default function App() {
  const [state, setState] = useState<CityState>(() => {
    const tick = Number(INITIAL_PARAMS.get("tick") ?? 0);
    return Number.isFinite(tick) && tick > 0 ? { ...INIT_STATE, tick } : INIT_STATE;
  });
  const { camera, setCamera, viewport, updateViewport } = useCameraController(INIT_CAMERA);
  const [mode, setMode] = useState<Mode>(() => parseMode(INITIAL_PARAMS.get("mode")));
  const [viewMode, setViewMode] = useState<ViewMode>(() => parseViewMode(INITIAL_PARAMS.get("view")));
  const [visualConfig, setVisualConfig] = useState<PixelRealismConfig>(() => {
    const base = defaultPixelRealismConfig(parseViewMode(INITIAL_PARAMS.get("view")));
    return INITIAL_PARAMS.has("vibe") ? vibeToPixelRealismConfig(compileVibeScene(INITIAL_VIBE_ID, "preset").config, base) : base;
  });
  const [activeVibeScene, setActiveVibeScene] = useState<VibeSceneConfig | undefined>(() => INITIAL_VIBE);
  const [playableScene, setPlayableScene] = useState<PlayableSceneState>(() => createInitialPlayableScene(INITIAL_VIBE, INITIAL_SCENE_DEMO));
  const [sceneTool, setSceneTool] = useState<SceneInteractionTool>("city");
  const [sceneMaterial, setSceneMaterial] = useState<PlayableMaterial>("water");
  const [sceneLightKind, setSceneLightKind] = useState<PlayableLightKind>("neon");
  const [vibeUndo, setVibeUndo] = useState<VibeUndoSnapshot | null>(null);
  const [cinematic, setCinematic] = useState(INITIAL_PARAMS.get("cinematic") === "1");
  const [tool, setTool] = useState<TileType | "select" | "erase">("select");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [animate, setAnimate] = useState(!INITIAL_BENCHMARK_STATIC);
  const [speed, setSpeed] = useState(1);
  const [showHeatmap, setShowHeatmap] = useState(INITIAL_PARAMS.get("heatmap") === "1");
  const [showFibmob, setShowFibmob] = useState(INITIAL_PARAMS.get("fibmob") === "1");
  const [showAgentLabels, setShowAgentLabels] = useState(INITIAL_PARAMS.get("labels") !== "0");
  const [physicsEnabled, setPhysicsEnabled] = useState(true);
  const [showPhysicsDebug, setShowPhysicsDebug] = useState(false);
  const [showChunkDebug, setShowChunkDebug] = useState(false);
  const [reviewedAssets, setReviewedAssets] = useState<ReviewedAssetsManifest | null>(null);
  const fpsSampler = useFpsSampler(true);
  const {
    beginFrame: fpsBeginFrame,
    endFrame: fpsEndFrame,
    reset: resetFpsSampler,
    snapshot: fpsSnapshot,
    getSnapshot: getFpsSnapshot,
  } = fpsSampler;
  const renderCountersRef = useRef(defaultRenderCounters(viewMode, INIT_CAMERA.zoom));
  const benchmarkRef = useRef<{ startedAt: number; durationMs: number; samples: FpsSnapshot[] } | null>(null);
  const [benchmarkRunning, setBenchmarkRunning] = useState(false);
  const [benchmarkProgress, setBenchmarkProgress] = useState(0);
  const [focusedBenchmarkRunning, setFocusedBenchmarkRunning] = useState(false);
  const [focusedBenchmarkProgress, setFocusedBenchmarkProgress] = useState(0);
  const [focusedBenchmarkDuration, setFocusedBenchmarkDuration] = useState(10_000);
  const [playableQaResult, setPlayableQaResult] = useState<PlayableInteractionQaResult | null>(null);
  const focus = INITIAL_PARAMS.get("focus") === "wabi" ? "wabi" as const : undefined;

  const animateRef = useRef(animate);
  animateRef.current = animate;
  const speedRef = useRef(speed);
  speedRef.current = speed;
  const stateRef = useRef(state);
  stateRef.current = state;
  const playableSceneRef = useRef(playableScene);
  playableSceneRef.current = playableScene;
  const cameraRef = useRef(camera);
  cameraRef.current = camera;
  const viewModeRef = useRef(viewMode);
  viewModeRef.current = viewMode;
  const physicsEnabledRef = useRef(physicsEnabled);
  physicsEnabledRef.current = physicsEnabled;
  const fileInputRef = useRef<HTMLInputElement>(null);
  const autoBenchmarkStartedRef = useRef(false);
  const pixelRuntimeRef = useRef<ReturnType<typeof createPixelRealismRuntime> | null>(null);

  // Main simulation RAF loop
  useEffect(() => {
    let lastTick = performance.now();
    let frameId: number;
    const BASE_INTERVAL_MS = 200;

    const loop = (now: number) => {
      fpsBeginFrame(now);
      if (animateRef.current) {
        const interval = BASE_INTERVAL_MS / speedRef.current;
        if (now - lastTick >= interval) {
          setState(prev => tickEngine(prev, {
            enableAgentPhysics: physicsEnabledRef.current,
            enablePhysicsCollisions: true,
            physicsDt: 0.05,
          }));
          setPlayableScene(prev => prev.paused ? prev : stepPlayableScene(prev, stateRef.current.width, stateRef.current.height));
          lastTick = now;
        }
      }
      fpsEndFrame(performance.now(), {
        ...renderCountersRef.current,
        activePixelCells: stateRef.current.fieldMetrics?.activeCells ?? renderCountersRef.current.activePixelCells,
        viewMode: viewModeRef.current,
        cameraZoom: cameraRef.current.zoom,
      });
      frameId = requestAnimationFrame(loop);
    };

    frameId = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(frameId);
  }, [fpsBeginFrame, fpsEndFrame]);

  // Load non-critical UI prefs on mount. City state is explicit JSON only.
  useEffect(() => {
    const prefs = loadPrefs();
    if (!INITIAL_PARAMS.has("heatmap")) setShowHeatmap(prefs.showHeatmap);
    if (!INITIAL_PARAMS.has("fibmob")) setShowFibmob(prefs.showFibmob);
    if (!INITIAL_PARAMS.has("labels")) setShowAgentLabels(prefs.showAgentLabels);
    setSpeed(INITIAL_BENCHMARK_STATIC ? 0.5 : prefs.speed);
  }, []);

  useEffect(() => {
    let cancelled = false;
    loadReviewedAssetsManifest().then(manifest => {
      if (!cancelled) setReviewedAssets(manifest);
    });
    return () => { cancelled = true; };
  }, []);

  const handleTileClick = useCallback((x: number, y: number) => {
    if (sceneTool === "material") {
      setPlayableScene(prev => placeSceneMaterial(prev, x, y, sceneMaterial));
      return;
    }
    if (sceneTool === "light") {
      setPlayableScene(prev => placeSceneLight(prev, x, y, sceneLightKind));
      return;
    }
    if (sceneTool === "erase") {
      setPlayableScene(prev => eraseSceneAt(prev, x, y));
      return;
    }
    if (sceneTool === "select") {
      setPlayableScene(prev => selectSceneAt(prev, x, y));
      return;
    }
    setState(prev => {
      if (tool === "erase") return eraseTile(prev, x, y);
      if (tool !== "select") return placeTile(prev, x, y, tool as TileType);
      return prev;
    });
  }, [sceneLightKind, sceneMaterial, sceneTool, tool]);

  const handleRenderCounters = useCallback((counters: ReturnType<typeof defaultRenderCounters>) => {
    renderCountersRef.current = counters;
  }, []);

  const handleReset = useCallback(() => {
    const fresh = createCity();
    setState(fresh);
    setPlayableScene(applyVibeSceneToPlayableScene(createDefaultPlayableSceneState(), activeVibeScene ?? INITIAL_VIBE, fresh.width, fresh.height));
    const preset = applyCameraPreset(mode, viewMode, fresh, viewport, null);
    setCamera(preset.camera);
    setSelectedId(null);
  }, [activeVibeScene, mode, setCamera, viewMode, viewport]);

  const handleSave = useCallback(() => {
    downloadJson(`duat-city-save-tick${stateRef.current.tick}.json`, saveCityToJson(stateRef.current));
    savePrefs({ showHeatmap, showFibmob, showAgentLabels, speed });
  }, [showHeatmap, showFibmob, showAgentLabels, speed]);

  const handleLoad = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const handleImportFile = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const loaded = loadCityFromJson(String(reader.result ?? ""));
      if (loaded) setState(loaded);
      event.target.value = "";
    };
    reader.readAsText(file);
  }, []);

  const handleResetCamera = useCallback(() => {
    const preset = applyCameraPreset(mode, viewMode, stateRef.current, viewport, selectedId);
    setCamera(preset.camera);
    setShowHeatmap(preset.showHeatmap);
    setShowFibmob(preset.showFibmob);
    setShowPhysicsDebug(preset.showPhysicsDebug);
    setShowChunkDebug(preset.showChunkDebug);
    setShowAgentLabels(preset.showAgentLabels);
  }, [mode, selectedId, setCamera, viewMode, viewport]);

  const handleFollowCriticalAgent = useCallback(() => {
    const agent = mostCriticalAgent(stateRef.current);
    if (!agent) return;
    setSelectedId(agent.id);
    setCamera(centerOnSelectedAgent(agent, viewport.width, viewport.height, 2.1));
  }, [setCamera, viewport.height, viewport.width]);

  const handleCinematic = useCallback(() => {
    setCinematic(true);
    setViewMode("BEAUTIFUL");
    const preset = applyCameraPreset(mode, "BEAUTIFUL", stateRef.current, viewport, selectedId);
    setCamera(preset.camera);
    setShowHeatmap(false);
    setShowFibmob(false);
    setShowPhysicsDebug(false);
    setShowChunkDebug(false);
    setShowAgentLabels(false);
  }, [mode, selectedId, setCamera, viewport]);

  const exitCinematic = useCallback(() => {
    setCinematic(false);
    setViewMode("OPERATIONAL");
    const preset = applyCameraPreset(mode, "OPERATIONAL", stateRef.current, viewport, selectedId);
    setCamera(preset.camera);
    setShowAgentLabels(true);
  }, [mode, selectedId, setCamera, viewport]);

  useEffect(() => {
    const preset = applyCameraPreset(mode, viewMode, stateRef.current, viewport, selectedId);
    setCamera(preset.camera);
    if (viewMode === "DEBUG" || viewMode === "BEAUTIFUL") {
      setShowHeatmap(preset.showHeatmap);
      setShowFibmob(preset.showFibmob);
      setShowPhysicsDebug(preset.showPhysicsDebug);
      setShowChunkDebug(preset.showChunkDebug);
      setShowAgentLabels(preset.showAgentLabels);
    }
  }, [mode, selectedId, setCamera, viewMode, viewport.height, viewport.width]);

  const lod = useMemo(() => computeLOD(camera, state.R, state.Phi_eff, state.tick, state.physicsMetrics, showPhysicsDebug), [
    camera,
    showPhysicsDebug,
    state.Phi_eff,
    state.R,
    state.physicsMetrics,
    state.tick,
  ]);
  const graphicsBudget = useMemo(() => computeGraphicsBudget(
    state.R,
    state.Phi_eff,
    camera.zoom,
    state.physicsMetrics?.R_physics ?? 0,
    state.tick,
    state.quaternary,
  ), [
    camera.zoom,
    state.Phi_eff,
    state.R,
    state.physicsMetrics?.R_physics,
    state.quaternary,
    state.tick,
  ]);
  const effectiveGraphicsBudget = useMemo(() => viewMode === "BEAUTIFUL"
    ? { ...graphicsBudget, shadowsEnabled: true, heatmapEnabled: false, particlesEnabled: true }
    : viewMode === "DEBUG"
      ? { ...graphicsBudget, heatmapEnabled: true }
      : graphicsBudget, [graphicsBudget, viewMode]);
  const graphicsMetrics = useMemo(() => estimateGraphicsMetrics(
    effectiveGraphicsBudget,
    effectiveGraphicsBudget.chunkMode === "FULL" ? 24 : 8,
    effectiveGraphicsBudget.chunkMode === "FULL" ? 24 : 4,
    effectiveGraphicsBudget.particlesEnabled ? 12 : 0,
    state.quaternary,
  ), [effectiveGraphicsBudget, state.quaternary]);
  const effectivePixelConfig = useMemo(() => normalizeQualityForView({
    ...visualConfig,
    timeOfDay: playableScene.timeOfDay,
    weather: playableScene.weather,
    vibePreset: playableScene.activeVibe?.id ?? visualConfig.vibePreset,
  }, viewMode), [playableScene.activeVibe?.id, playableScene.timeOfDay, playableScene.weather, viewMode, visualConfig]);
  const stateWithPlayableScene: CityState = useMemo(() => ({
    ...state,
    playableScene,
  }), [playableScene, state]);
  const pixelRealismRuntime = useMemo(() => createPixelRealismRuntime(stateWithPlayableScene, effectivePixelConfig), [effectivePixelConfig, stateWithPlayableScene]);
  pixelRuntimeRef.current = pixelRealismRuntime;
  const stateForPanels: CityState = useMemo(() => ({
    ...state,
    graphicsMetrics,
    pixelRealism: pixelRealismRuntime.metrics,
    playableScene,
  }), [graphicsMetrics, pixelRealismRuntime.metrics, playableScene, state]);
  const spriteResolver = useMemo(() => createSpriteResolver(reviewedAssets), [reviewedAssets]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const duatWindow = window as unknown as {
      __DUAT_PERF_SNAPSHOT__?: object;
      __DUAT_RESET_FPS__?: () => void;
    };
    duatWindow.__DUAT_RESET_FPS__ = resetFpsSampler;
    duatWindow.__DUAT_PERF_SNAPSHOT__ = {
      schema: "duat/performance-live-snapshot/v1.4",
      benchmarkStatic: INITIAL_BENCHMARK_STATIC,
      at: new Date().toISOString(),
      snapshot: fpsSnapshot,
      graphicsMetrics,
      pixelRealism: pixelRealismRuntime.metrics,
      renderCounters: renderCountersRef.current,
    };
  }, [fpsSnapshot, graphicsMetrics, pixelRealismRuntime.metrics, resetFpsSampler]);

  const handleApplyVibeScene = useCallback((scene: VibeSceneConfig) => {
    setVibeUndo(createVibeUndoSnapshot(activeVibeScene, visualConfig, playableSceneRef.current));
    setActiveVibeScene(scene);
    setVisualConfig(prev => vibeToPixelRealismConfig(scene, prev));
    setPlayableScene(prev => applyVibeSceneToPlayableScene(prev, scene, stateRef.current.width, stateRef.current.height));
  }, [activeVibeScene, visualConfig]);

  const handleUndoVibeScene = useCallback(() => {
    if (!vibeUndo) return;
    const restored = restoreVibeUndoSnapshot(vibeUndo);
    setVisualConfig(restored.visualConfig);
    setActiveVibeScene(restored.activeVibeScene);
    setPlayableScene(restored.playableScene);
    setVibeUndo(null);
  }, [vibeUndo]);

  const handleToggleScenePause = useCallback(() => {
    setPlayableScene(prev => ({ ...prev, paused: !prev.paused }));
  }, []);

  const handleStepScene = useCallback(() => {
    setPlayableScene(prev => stepPlayableScene(prev, stateRef.current.width, stateRef.current.height));
  }, []);

  const handleSceneTimeOfDay = useCallback((time: PlayableSceneState["timeOfDay"]) => {
    setPlayableScene(prev => setSceneTime(prev, time));
    setVisualConfig(prev => ({ ...prev, timeOfDay: time }));
  }, []);

  const handleSceneWeather = useCallback((weather: PlayableSceneState["weather"]) => {
    setPlayableScene(prev => setSceneWeather(prev, weather));
    setVisualConfig(prev => ({ ...prev, weather }));
  }, []);

  const handleApplySceneVibePreset = useCallback((preset: string) => {
    handleApplyVibeScene(compileVibeScene(preset, "preset").config);
  }, [handleApplyVibeScene]);

  const handleSaveScene = useCallback(() => {
    downloadJson(`duat-playable-scene-v1_1-t${playableSceneRef.current.tick}.json`, serializePlayableScene(playableSceneRef.current));
  }, []);

  const handleLoadScene = useCallback((json: string) => {
    const loaded = deserializePlayableScene(json);
    if (loaded) {
      setPlayableScene(loaded);
      setVisualConfig(prev => ({ ...prev, timeOfDay: loaded.timeOfDay, weather: loaded.weather, vibePreset: loaded.activeVibe?.id ?? prev.vibePreset }));
      setActiveVibeScene(loaded.activeVibe);
    }
  }, []);

  const handleExportRpgScene = useCallback(() => {
    const exportState = { ...stateRef.current, playableScene: playableSceneRef.current, pixelRealism: pixelRealismRuntime.metrics };
    downloadJson(`duat-rpg-scene-v1_1-t${exportState.tick}.json`, JSON.stringify(exportRPGWorld(exportState), null, 2));
  }, [pixelRealismRuntime.metrics]);

  const handleRunPlayableQa = useCallback(() => {
    const result = runPlayableInteractionQaSequence(stateRef.current);
    const loaded = deserializePlayableScene(result.sceneJson);
    if (loaded) {
      setPlayableScene(loaded);
      setVisualConfig(prev => ({
        ...prev,
        qualityPreset: "BEAUTIFUL",
        timeOfDay: loaded.timeOfDay,
        weather: loaded.weather,
        vibePreset: loaded.activeVibe?.id ?? prev.vibePreset,
      }));
      setViewMode("BEAUTIFUL");
      setActiveVibeScene(loaded.activeVibe);
    }
    setPlayableQaResult(result);
    downloadJson(`duat-playable-interaction-qa-v1_1_1-t${stateRef.current.tick}.json`, JSON.stringify(result, null, 2));
  }, []);

  const handleApplyVibeGameCommand = useCallback((command: string) => {
    const compiled = parseVibeCommand(command);
    setPlayableScene(prev => applyVibeGamePatch(prev, compiled.scenePatch).scene);
    setVisualConfig(prev => ({
      ...prev,
      paletteProfile: compiled.scenePatch.styleProfile ?? prev.paletteProfile,
      timeOfDay: compiled.scenePatch.timeOfDay ?? prev.timeOfDay,
      weather: compiled.scenePatch.weather ?? prev.weather,
      vibePreset: compiled.scenePatch.vibePreset ?? prev.vibePreset,
    }));
  }, []);

  const copyPerformanceJson = useCallback(() => {
    const payload = JSON.stringify({
      schema: "duat/performance-snapshot/v0.8",
      timestamp: new Date().toISOString(),
      snapshot: getFpsSnapshot(),
      graphicsMetrics,
    }, null, 2);
    if (navigator.clipboard?.writeText) {
      void navigator.clipboard.writeText(payload).catch(() => {
        downloadJson(`duat-performance-t${stateRef.current.tick}.json`, payload);
      });
    } else {
      downloadJson(`duat-performance-t${stateRef.current.tick}.json`, payload);
    }
  }, [getFpsSnapshot, graphicsMetrics]);

  const startPerformanceBenchmark = useCallback((durationMs = 30_000) => {
    resetFpsSampler();
    benchmarkRef.current = { startedAt: performance.now(), durationMs, samples: [] };
    setBenchmarkProgress(0);
    setBenchmarkRunning(true);
  }, [resetFpsSampler]);

  useEffect(() => {
    if (!benchmarkRunning || !benchmarkRef.current) return;
    const run = benchmarkRef.current;
    run.samples.push(fpsSnapshot);
    const elapsed = performance.now() - run.startedAt;
    setBenchmarkProgress(Math.max(0, Math.min(1, elapsed / run.durationMs)));
    if (elapsed >= run.durationMs) {
      const output = createPerformanceBenchmarkOutput(
        getFpsSnapshot(),
        { ...stateRef.current, graphicsMetrics },
        run.durationMs,
        [`samples=${run.samples.length}`, "in-app requestAnimationFrame sampler"],
      );
      downloadJson(`duat-performance-benchmark-v0_8-t${stateRef.current.tick}.json`, JSON.stringify(output, null, 2));
      benchmarkRef.current = null;
      setBenchmarkRunning(false);
      setBenchmarkProgress(1);
    }
  }, [benchmarkRunning, fpsSnapshot, getFpsSnapshot, graphicsMetrics]);

  const runFocusedBenchmark = useCallback(async (durationMs = focusedBenchmarkDuration, options?: { download?: boolean; publishWindow?: boolean; browserMode?: BenchmarkBrowserMode }): Promise<PerformanceBenchmarkV111Document> => {
    setFocusedBenchmarkRunning(true);
    setFocusedBenchmarkProgress(0);
    const browserMode = options?.browserMode ?? parseBrowserMode(INITIAL_PARAMS.get("browserMode"));
    const results: PerformanceBenchmarkV111Result[] = [];
    const benchWindow = window as typeof window & {
      __DUAT_V111_BENCHMARK_STATUS__?: string;
      __DUAT_BENCHMARK_RESULT__?: PerformanceBenchmarkV111Document;
    };
    if (options?.publishWindow) benchWindow.__DUAT_V111_BENCHMARK_STATUS__ = "running";
    const wasAnimating = animateRef.current;
    setAnimate(false);

    try {
      for (let index = 0; index < V111_BENCHMARK_SCENARIOS.length; index++) {
        const scenario = V111_BENCHMARK_SCENARIOS[index];
        const vibe = scenario.vibePreset ? compileVibeScene(scenario.vibePreset, "preset").config : undefined;
        const scene = { ...createBenchmarkSceneV111(scenario, vibe), paused: true };
        const scenarioState = scenario.agentCount ? makeAgentLoadState(createCity(), scenario.agentCount) : createCity();
        setMode("CITY");
        setCinematic(false);
        setViewMode(scenario.viewMode);
        setVisualConfig(prev => ({
          ...prev,
          qualityPreset: scenario.qualityPreset,
          timeOfDay: scene.timeOfDay,
          weather: scene.weather,
          vibePreset: vibe?.id,
          hideUiForCapture: scenario.viewMode === "BEAUTIFUL",
        }));
        setActiveVibeScene(vibe);
        setPlayableScene(scene);
        setState(scenarioState);
        await nextAnimationFrames(4);
        const measured = await measureFocusedFrames(durationMs);
        const runtime = pixelRuntimeRef.current;
        results.push({
          scenario: scenario.id,
          label: scenario.label,
          avgFps: measured.avgFps,
          minFps: measured.minFps,
          maxFps: measured.maxFps,
          p95FrameMs: measured.p95FrameMs,
          p99FrameMs: measured.p99FrameMs,
          droppedFrames: measured.droppedFrames,
          activeLightCells: runtime?.metrics.activeLightCells ?? 0,
          activeMaterialCells: runtime?.metrics.activeMaterialCells ?? scene.metrics.activeMaterialCells,
          particles: scene.metrics.particles + (renderCountersRef.current.particlesRendered ?? 0),
          agents: scenarioState.agents.length,
          pixelFieldResolution: pixelResolutionForQualityV111(scenario.qualityPreset),
          qualityPreset: scenario.qualityPreset,
          viewMode: scenario.viewMode,
          browserMode,
          focusStatus: measured.focusStatus,
          finite: [
            measured.avgFps,
            measured.minFps,
            measured.maxFps,
            measured.p95FrameMs,
            measured.p99FrameMs,
            runtime?.metrics.activeLightCells ?? 0,
            runtime?.metrics.activeMaterialCells ?? scene.metrics.activeMaterialCells,
          ].every(Number.isFinite),
        });
        setFocusedBenchmarkProgress((index + 1) / V111_BENCHMARK_SCENARIOS.length);
      }
      const focusStatus = summarizeFocus(results.map(result => result.focusStatus));
      const doc: PerformanceBenchmarkV111Document = {
        schema: "duat/performance-benchmark/v1.1.1",
        fingerprint: "DUAT-v1.1.1-FOCUSED-FPS-CLOSURE",
        generatedAt: new Date().toISOString(),
        durationMsPerScenario: durationMs,
        browser: navigator.userAgent,
        browserMode,
        focusStatus,
        focusedBrowserAvailable: focusStatus === "focused",
        scenarios: results,
        notes: [
          "Focused benchmark runner is local-only. Browser focus is verified with document.hasFocus and visibilityState.",
          focusStatus === "focused" ? "Focused browser was observed by the app." : "FOCUSED_BROWSER_NOT_AVAILABLE: focus could not be guaranteed by automation; use the in-app Run Focused FPS Benchmark button for owner-controlled focus.",
          "Light budget and dirty-signature cache are enabled for v1.1.1.",
        ],
      };
      if (options?.publishWindow) {
        benchWindow.__DUAT_BENCHMARK_RESULT__ = doc;
        benchWindow.__DUAT_V111_BENCHMARK_STATUS__ = "done";
      }
      if (options?.download !== false) {
        downloadJson(`duat-performance-benchmark-v1_1_1-${durationMs}ms.json`, JSON.stringify(doc, null, 2));
      }
      return doc;
    } catch (error) {
      if (options?.publishWindow) benchWindow.__DUAT_V111_BENCHMARK_STATUS__ = `failed:${error instanceof Error ? error.message : String(error)}`;
      throw error;
    } finally {
      setAnimate(wasAnimating);
      setFocusedBenchmarkRunning(false);
    }
  }, [focusedBenchmarkDuration]);

  useEffect(() => {
    if (INITIAL_PARAMS.get("benchmark") !== "v1_1_1" || autoBenchmarkStartedRef.current) return;
    autoBenchmarkStartedRef.current = true;
    const durationMs = Math.max(600, Math.min(60_000, Number(INITIAL_PARAMS.get("durationMs") ?? 10_000)));
    const browserMode = parseBrowserMode(INITIAL_PARAMS.get("browserMode"));
    const benchWindow = window as typeof window & {
      __DUAT_V111_BENCHMARK_STATUS__?: string;
    };
    benchWindow.__DUAT_V111_BENCHMARK_STATUS__ = "running";
    void runFocusedBenchmark(durationMs, { download: false, publishWindow: true, browserMode }).catch(error => {
      benchWindow.__DUAT_V111_BENCHMARK_STATUS__ = `failed:${error instanceof Error ? error.message : String(error)}`;
    });
  }, [runFocusedBenchmark]);

  useEffect(() => {
    if (INITIAL_PARAMS.get("benchmark") !== "v1_1" || autoBenchmarkStartedRef.current) return;
    autoBenchmarkStartedRef.current = true;
    let cancelled = false;
    const durationMs = Math.max(600, Math.min(5000, Number(INITIAL_PARAMS.get("durationMs") ?? 1400)));
    const benchWindow = window as typeof window & {
      __DUAT_V11_BENCHMARK_STATUS__?: string;
      __DUAT_BENCHMARK_RESULT__?: PerformanceBenchmarkV11Document;
    };
    benchWindow.__DUAT_V11_BENCHMARK_STATUS__ = "running";

    async function run(): Promise<void> {
      const results: PerformanceBenchmarkV11Result[] = [];
      for (const scenario of V11_BENCHMARK_SCENARIOS) {
        if (cancelled) return;
        const vibe = scenario.vibePreset ? compileVibeScene(scenario.vibePreset, "preset").config : undefined;
        const scene = vibe
          ? applyVibeSceneToPlayableScene(createDefaultPlayableSceneState(), vibe, INIT_STATE.width, INIT_STATE.height)
          : createDefaultPlayableSceneState();
        const scenarioState = scenario.agentCount ? makeAgentLoadState(createCity(), scenario.agentCount) : createCity();
        setMode("CITY");
        setCinematic(false);
        setViewMode(scenario.viewMode);
        setVisualConfig(prev => ({
          ...prev,
          qualityPreset: scenario.qualityPreset,
          timeOfDay: scene.timeOfDay,
          weather: scene.weather,
          vibePreset: vibe?.id,
          hideUiForCapture: scenario.viewMode === "BEAUTIFUL",
        }));
        setActiveVibeScene(vibe);
        setPlayableScene(scene);
        setState(scenarioState);
        await nextAnimationFrames(3);
        const measured = await measureVisibleFrames(durationMs);
        const runtime = pixelRuntimeRef.current;
        results.push({
          scenario: scenario.id,
          label: scenario.label,
          avgFPS: measured.avgFPS,
          p95FrameMs: measured.p95FrameMs,
          minFPS: measured.minFPS,
          maxFPS: measured.maxFPS,
          droppedFrames: measured.droppedFrames,
          activeLightCells: runtime?.metrics.activeLightCells ?? 0,
          activeMaterialCells: runtime?.metrics.activeMaterialCells ?? scene.metrics.activeMaterialCells,
          particles: scene.metrics.particles + (renderCountersRef.current.particlesRendered ?? 0),
          agents: scenarioState.agents.length,
          pixelFieldResolution: pixelResolutionForQuality(scenario.qualityPreset),
          qualityPreset: scenario.qualityPreset,
          visibleBrowser: true,
          finite: [
            measured.avgFPS,
            measured.p95FrameMs,
            measured.minFPS,
            measured.maxFPS,
            runtime?.metrics.activeLightCells ?? 0,
            runtime?.metrics.activeMaterialCells ?? scene.metrics.activeMaterialCells,
          ].every(Number.isFinite),
        });
      }
      const doc: PerformanceBenchmarkV11Document = {
        schema: "duat/performance-benchmark/v1.1",
        fingerprint: "DUAT-v1.1-PLAYABLE-SCENE-QA",
        generatedAt: new Date().toISOString(),
        durationMsPerScenario: durationMs,
        browser: navigator.userAgent,
        visibleBrowser: true,
        scenarios: results,
        notes: [
          "Visible headed browser run via local Edge/CDP, no MCP execution.",
          "requestAnimationFrame frame deltas measured in the app page; timeout fallback resolves if the visible window is focus-throttled.",
        ],
      };
      benchWindow.__DUAT_BENCHMARK_RESULT__ = doc;
      benchWindow.__DUAT_V11_BENCHMARK_STATUS__ = "done";
    }

    void run().catch(error => {
      benchWindow.__DUAT_V11_BENCHMARK_STATUS__ = `failed:${error instanceof Error ? error.message : String(error)}`;
    });
    return () => { cancelled = true; };
  }, []);

  const selectedBuilding = selectedId
    ? state.buildings.find(b => b.id === selectedId)
    : undefined;

  function renderRightPanel() {
    if (selectedBuilding) {
      return (
        <div className="panel-right">
          <BuildingInspector
            state={state}
            buildingId={selectedBuilding.id}
            onClose={() => setSelectedId(null)}
          />
            {mode === "OSIT" && <OSITPanel
              state={stateForPanels}
              viewMode={viewMode}
              focus={focus}
              performanceSnapshot={fpsSnapshot}
              benchmarkRunning={benchmarkRunning}
              benchmarkProgress={benchmarkProgress}
              onResetPerformance={resetFpsSampler}
              onCopyPerformanceJson={copyPerformanceJson}
              onRunPerformanceBenchmark={startPerformanceBenchmark}
              focusedBenchmarkRunning={focusedBenchmarkRunning}
              focusedBenchmarkProgress={focusedBenchmarkProgress}
              focusedBenchmarkDuration={focusedBenchmarkDuration}
              onFocusedBenchmarkDuration={setFocusedBenchmarkDuration}
              onRunFocusedBenchmark={(durationMs) => { void runFocusedBenchmark(durationMs ?? focusedBenchmarkDuration); }}
            />}
        </div>
      );
    }

    switch (mode) {
      case "CITY":
        return (
          <CityPanel
            state={stateForPanels}
            selectedId={selectedId}
            onSelect={setSelectedId}
            showHeatmap={showHeatmap}
            onShowHeatmap={setShowHeatmap}
            showFibmob={showFibmob}
            onShowFibmob={setShowFibmob}
            showAgentLabels={showAgentLabels}
            onShowAgentLabels={setShowAgentLabels}
            onResetCamera={handleResetCamera}
          />
        );
      case "AGENT":
        return (
          <AgentInspector
            state={stateForPanels}
            selectedId={selectedId}
            onSelect={setSelectedId}
          />
        );
      case "RPG":
        return <RPGBuilderPanel state={stateForPanels} />;
      case "OSIT":
        return <OSITPanel
          state={stateForPanels}
          viewMode={viewMode}
          focus={focus}
          performanceSnapshot={fpsSnapshot}
          benchmarkRunning={benchmarkRunning}
          benchmarkProgress={benchmarkProgress}
          onResetPerformance={resetFpsSampler}
          onCopyPerformanceJson={copyPerformanceJson}
          onRunPerformanceBenchmark={startPerformanceBenchmark}
          focusedBenchmarkRunning={focusedBenchmarkRunning}
          focusedBenchmarkProgress={focusedBenchmarkProgress}
          focusedBenchmarkDuration={focusedBenchmarkDuration}
          onFocusedBenchmarkDuration={setFocusedBenchmarkDuration}
          onRunFocusedBenchmark={(durationMs) => { void runFocusedBenchmark(durationMs ?? focusedBenchmarkDuration); }}
        />;
    }
  }
  const showChrome = !cinematic && viewMode !== "BEAUTIFUL";
  const showPanels = showChrome;
  const effectiveHeatmap = viewMode === "DEBUG" ? true : viewMode === "OPERATIONAL" && showHeatmap;
  const effectiveFibmob = viewMode === "DEBUG" ? true : mode === "OSIT" && showFibmob;

  return (
    <div className="duat-root">
      {showChrome && <Topbar state={state} />}
      <div className="duat-body">
        {showChrome && <Toolbar
          mode={mode}
          onMode={m => { setMode(m); setSelectedId(null); }}
          tool={tool}
          onTool={setTool}
          animate={animate}
          onAnimate={setAnimate}
          speed={speed}
          onSpeed={setSpeed}
          onReset={handleReset}
          onSave={handleSave}
          onLoad={handleLoad}
          onResetCamera={handleResetCamera}
          onFollowCriticalAgent={handleFollowCriticalAgent}
          onCinematic={handleCinematic}
          physicsEnabled={physicsEnabled}
          onPhysicsEnabled={setPhysicsEnabled}
          showPhysicsDebug={showPhysicsDebug}
          onShowPhysicsDebug={setShowPhysicsDebug}
          showChunkDebug={showChunkDebug}
          onShowChunkDebug={setShowChunkDebug}
          viewMode={viewMode}
          onViewMode={setViewMode}
          visualConfig={visualConfig}
          onVisualConfig={setVisualConfig}
          activeVibeScene={activeVibeScene}
          onApplyVibeScene={handleApplyVibeScene}
          onUndoVibeScene={handleUndoVibeScene}
          canUndoVibeScene={Boolean(vibeUndo)}
          playableScene={playableScene}
          sceneTool={sceneTool}
          onSceneTool={setSceneTool}
          sceneMaterial={sceneMaterial}
          onSceneMaterial={setSceneMaterial}
          sceneLightKind={sceneLightKind}
          onSceneLightKind={setSceneLightKind}
          onToggleScenePause={handleToggleScenePause}
          onStepScene={handleStepScene}
          onSceneTimeOfDay={handleSceneTimeOfDay}
          onSceneWeather={handleSceneWeather}
          onApplySceneVibePreset={handleApplySceneVibePreset}
          onSaveScene={handleSaveScene}
          onLoadScene={handleLoadScene}
          onExportRpgScene={handleExportRpgScene}
          onRunPlayableQa={handleRunPlayableQa}
          onApplyVibeGameCommand={handleApplyVibeGameCommand}
          playableQaSummary={playableQaResult ? "QA sequence passed locally; JSON exported." : undefined}
          state={stateForPanels}
        />}
        <input ref={fileInputRef} type="file" accept="application/json,.json" onChange={handleImportFile} style={{ display: "none" }} />
        <MainCanvas
          state={stateForPanels}
          camera={camera}
          lod={lod}
          graphicsBudget={effectiveGraphicsBudget}
          physicsMetrics={state.physicsMetrics}
          mode={mode}
          tool={sceneTool === "city" ? tool : "scene"}
          selectedId={selectedId}
          showHeatmap={effectiveHeatmap}
          showFibmob={effectiveFibmob}
          showAgentLabels={showAgentLabels}
          showPhysicsDebug={viewMode === "DEBUG" || showPhysicsDebug}
          showChunkDebug={viewMode === "DEBUG" || showChunkDebug}
          showQuaternaryDebug={viewMode === "DEBUG"}
          viewMode={viewMode}
          spriteResolver={spriteResolver}
          pixelRealismRuntime={pixelRealismRuntime}
          onRenderCounters={handleRenderCounters}
          onViewportChange={updateViewport}
          onCameraChange={setCamera}
          onTileClick={handleTileClick}
          onSelect={setSelectedId}
        />
        {showPanels && renderRightPanel()}
      </div>
      {!showChrome && !effectivePixelConfig.hideUiForCapture && (
        <div className="cinematic-controls">
          <button className="ctrl-btn" onClick={exitCinematic}>Exit View</button>
          <button className="ctrl-btn" onClick={handleResetCamera}>Reset Camera</button>
        </div>
      )}
      {showPanels && mode === "OSIT" ? (
        <div className="bottom-bar" style={{ height: "auto", maxHeight: 200, overflowY: "auto" }}>
          <HandoffPanel state={stateForPanels} />
        </div>
      ) : showPanels ? (
        <EventLogPanel state={state} />
      ) : null}
    </div>
  );
}

function parseMode(input: string | null): Mode {
  const mode = String(input ?? "CITY").toUpperCase();
  if (mode === "AGENT" || mode === "RPG" || mode === "OSIT") return mode;
  return "CITY";
}

function parseViewMode(input: string | null): ViewMode {
  const mode = String(input ?? "OPERATIONAL").toUpperCase();
  if (mode === "BEAUTIFUL" || mode === "DEBUG") return mode;
  return "OPERATIONAL";
}

function parseBrowserMode(input: string | null): BenchmarkBrowserMode {
  const mode = String(input ?? "fallback").toLowerCase();
  if (mode === "headed") return "headed";
  if (mode === "headless") return "headless";
  if (mode === "cdp") return "CDP";
  return "fallback";
}

function summarizeFocus(statuses: BenchmarkFocusStatus[]): BenchmarkFocusStatus {
  if (statuses.some(status => status === "focused")) return "focused";
  if (statuses.some(status => status === "unconfirmed")) return "unconfirmed";
  return "not_available";
}

function createBenchmarkSceneV111(scenario: PerformanceBenchmarkV111Scenario, vibe?: VibeSceneConfig): PlayableSceneState {
  let scene = vibe
    ? applyVibeSceneToPlayableScene(createDefaultPlayableSceneState(), vibe, INIT_STATE.width, INIT_STATE.height)
    : createDefaultPlayableSceneState();
  if (scenario.sceneDemo === "material_placement") {
    const cx = Math.floor(INIT_STATE.width / 2);
    const cy = Math.floor(INIT_STATE.height / 2);
    scene = placeSceneMaterial(scene, cx - 3, cy + 3, "water");
    scene = placeSceneMaterial(scene, cx - 1, cy + 2, "fire");
    scene = placeSceneMaterial(scene, cx - 1, cy + 1, "smoke");
    scene = placeSceneMaterial(scene, cx + 1, cy + 2, "stone");
    scene = placeSceneMaterial(scene, cx + 3, cy + 1, "neon");
    scene = placeSceneLight(scene, cx - 1, cy + 2, "fire");
    scene = placeSceneLight(scene, cx + 3, cy + 1, "neon");
  }
  return scene;
}

function createInitialPlayableScene(vibe: VibeSceneConfig, demo: string | null): PlayableSceneState {
  let scene = applyVibeSceneToPlayableScene(createDefaultPlayableSceneState(), vibe, INIT_STATE.width, INIT_STATE.height);
  const cx = Math.floor(INIT_STATE.width / 2);
  const cy = Math.floor(INIT_STATE.height / 2);
  if (demo === "water_reflection") {
    scene = placeSceneMaterial(scene, cx - 2, cy + 4, "water");
    scene = placeSceneMaterial(scene, cx - 1, cy + 4, "water");
    scene = placeSceneLight(scene, cx - 2, cy + 2, "signal");
  } else if (demo === "fire_smoke") {
    scene = placeSceneMaterial(scene, cx, cy + 1, "fire");
    scene = placeSceneMaterial(scene, cx, cy, "smoke");
    scene = placeSceneLight(scene, cx, cy + 1, "fire");
  } else if (demo === "material_placement") {
    scene = placeSceneMaterial(scene, cx - 3, cy + 2, "water");
    scene = placeSceneMaterial(scene, cx - 2, cy + 2, "stone");
    scene = placeSceneMaterial(scene, cx - 1, cy + 2, "wood");
    scene = placeSceneMaterial(scene, cx, cy + 2, "neon");
    scene = placeSceneLight(scene, cx, cy + 1, "neon");
  }
  return scene;
}

function nextAnimationFrames(count: number): Promise<void> {
  return new Promise(resolve => {
    let remaining = count;
    const fallback = window.setTimeout(resolve, Math.max(120, count * 80));
    const step = () => {
      remaining--;
      if (remaining <= 0) {
        window.clearTimeout(fallback);
        resolve();
      }
      else requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  });
}

function measureVisibleFrames(durationMs: number): Promise<Pick<PerformanceBenchmarkV11Result, "avgFPS" | "p95FrameMs" | "minFPS" | "maxFPS" | "droppedFrames">> {
  return new Promise(resolve => {
    const deltas: number[] = [];
    const start = performance.now();
    let last = 0;
    let resolved = false;
    const finish = () => {
      if (resolved) return;
      resolved = true;
      window.clearTimeout(timeout);
      const sorted = [...deltas].sort((a, b) => a - b);
      const avgFrameMs = deltas.length > 0 ? deltas.reduce((sum, value) => sum + value, 0) / deltas.length : durationMs;
      const p95FrameMs = sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * 0.95))] ?? avgFrameMs;
      const minDelta = sorted[0] ?? avgFrameMs;
      const maxDelta = sorted[sorted.length - 1] ?? avgFrameMs;
      resolve({
        avgFPS: roundBenchmark(1000 / avgFrameMs),
        p95FrameMs: roundBenchmark(p95FrameMs),
        minFPS: roundBenchmark(1000 / maxDelta),
        maxFPS: roundBenchmark(1000 / minDelta),
        droppedFrames: deltas.filter(delta => delta > 33.4).length + (deltas.length === 0 ? 1 : 0),
      });
    };
    const timeout = window.setTimeout(finish, durationMs + 1200);
    const step = (now: number) => {
      if (resolved) return;
      if (last > 0) {
        const delta = Math.max(0.1, now - last);
        deltas.push(delta);
      }
      last = now;
      if (now - start < durationMs) {
        requestAnimationFrame(step);
        return;
      }
      finish();
    };
    requestAnimationFrame(step);
  });
}

function measureFocusedFrames(durationMs: number): Promise<Pick<PerformanceBenchmarkV111Result, "avgFps" | "minFps" | "maxFps" | "p95FrameMs" | "p99FrameMs" | "droppedFrames" | "focusStatus">> {
  return new Promise(resolve => {
    const deltas: number[] = [];
    const start = performance.now();
    let last = 0;
    let resolved = false;
    const initialFocus = readFocusStatus();
    const finish = () => {
      if (resolved) return;
      resolved = true;
      window.clearTimeout(timeout);
      const sorted = [...deltas].sort((a, b) => a - b);
      const avgFrameMs = deltas.length > 0 ? deltas.reduce((sum, value) => sum + value, 0) / deltas.length : durationMs;
      const p95FrameMs = sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * 0.95))] ?? avgFrameMs;
      const p99FrameMs = sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * 0.99))] ?? p95FrameMs;
      const minDelta = sorted[0] ?? avgFrameMs;
      const maxDelta = sorted[sorted.length - 1] ?? avgFrameMs;
      resolve({
        avgFps: roundBenchmark(1000 / avgFrameMs),
        minFps: roundBenchmark(1000 / maxDelta),
        maxFps: roundBenchmark(1000 / minDelta),
        p95FrameMs: roundBenchmark(p95FrameMs),
        p99FrameMs: roundBenchmark(p99FrameMs),
        droppedFrames: deltas.filter(delta => delta > 33.4).length + (deltas.length === 0 ? 1 : 0),
        focusStatus: summarizeFocus([initialFocus, readFocusStatus()]),
      });
    };
    const timeout = window.setTimeout(finish, durationMs + 1500);
    const step = (now: number) => {
      if (resolved) return;
      if (last > 0) {
        const delta = Math.max(0.1, now - last);
        deltas.push(delta);
      }
      last = now;
      if (now - start < durationMs) {
        requestAnimationFrame(step);
        return;
      }
      finish();
    };
    requestAnimationFrame(step);
  });
}

function readFocusStatus(): BenchmarkFocusStatus {
  if (typeof document === "undefined") return "not_available";
  if (document.hasFocus()) return "focused";
  return document.visibilityState === "visible" ? "unconfirmed" : "not_available";
}

function roundBenchmark(value: number): number {
  return Number.isFinite(value) ? Number(value.toFixed(2)) : 0;
}
