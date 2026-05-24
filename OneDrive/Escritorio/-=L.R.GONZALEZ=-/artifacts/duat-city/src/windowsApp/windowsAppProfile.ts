import type { WindowsAppProfile } from "./windowsAppTypes";

export const DUAT_WINDOWS_APP_PROFILE: WindowsAppProfile = {
  schema: "duat/windows-app-profile/v1.4",
  fingerprint: "DUAT-v1.4-WINAPP-CONVERSION",
  preferredWrappers: ["electron", "tauri", "native_dotnet_edge_app_mode"],
  implementedWrapper: "native_dotnet_edge_app_mode",
  dependencyGate: "APPROVE_LOCAL_NO_NEW_DEPS",
  publicationAllowed: false,
  cloudUsed: false,
  wabiExecutionAllowed: false,
  unknownZipCodeExecuted: false,
  assetsCopiedWithoutProvenance: false,
  runtimeUrlPath: "/duat-city/",
  features: {
    iso3dRenderer: true,
    canvasFallback: true,
    pixelLightEngine: true,
    audioGameFeelManualEnable: true,
    agentLifePanel: true,
    brainRuntime: true,
    rpgExport: true,
    ositObservacionismo: true,
    vermeerLightProfile: true,
    qOverlay: true,
  },
  notes: [
    "Electron/Tauri remain preferred wrappers if reviewed dependencies are later approved.",
    "The v1.4 local build uses a no-new-dependency native .NET Framework launcher plus Edge App Mode.",
    "The launcher serves the existing DUAT web build from loopback and does not execute unknown zip code.",
    "Audio/Game-Feel still requires a local user gesture before preview/playback.",
  ],
};

export function getWindowsAppProfile(): WindowsAppProfile {
  return DUAT_WINDOWS_APP_PROFILE;
}
