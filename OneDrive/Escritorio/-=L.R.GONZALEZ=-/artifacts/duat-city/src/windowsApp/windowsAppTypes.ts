export type WindowsAppWrapperKind =
  | "electron"
  | "tauri"
  | "native_dotnet_edge_app_mode";

export interface WindowsAppFeatureMatrix {
  iso3dRenderer: boolean;
  canvasFallback: boolean;
  pixelLightEngine: boolean;
  audioGameFeelManualEnable: boolean;
  agentLifePanel: boolean;
  brainRuntime: boolean;
  rpgExport: boolean;
  ositObservacionismo: boolean;
  vermeerLightProfile: boolean;
  qOverlay: boolean;
}

export interface WindowsAppProfile {
  schema: "duat/windows-app-profile/v1.4";
  fingerprint: "DUAT-v1.4-WINAPP-CONVERSION";
  preferredWrappers: WindowsAppWrapperKind[];
  implementedWrapper: WindowsAppWrapperKind;
  dependencyGate: "APPROVE_LOCAL_NO_NEW_DEPS" | "REVIEW_NEW_DEPENDENCY_REQUIRED";
  publicationAllowed: false;
  cloudUsed: false;
  wabiExecutionAllowed: false;
  unknownZipCodeExecuted: false;
  assetsCopiedWithoutProvenance: false;
  runtimeUrlPath: "/duat-city/";
  features: WindowsAppFeatureMatrix;
  notes: string[];
}
