import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { getWindowsAppProfile } from "../windowsApp/windowsAppProfile";

describe("DUAT Windows app conversion v1.4", () => {
  it("preserves core runtime features behind a local wrapper", () => {
    const profile = getWindowsAppProfile();
    expect(profile.fingerprint).toBe("DUAT-v1.4-WINAPP-CONVERSION");
    expect(profile.schema).toBe("duat/windows-app-profile/v1.4");
    expect(profile.implementedWrapper).toBe("native_dotnet_edge_app_mode");
    expect(profile.preferredWrappers).toContain("electron");
    expect(profile.preferredWrappers).toContain("tauri");
    expect(profile.dependencyGate).toBe("APPROVE_LOCAL_NO_NEW_DEPS");
    expect(profile.runtimeUrlPath).toBe("/duat-city/");

    for (const enabled of Object.values(profile.features)) {
      expect(enabled).toBe(true);
    }
  });

  it("keeps protected boundaries closed", () => {
    const profile = getWindowsAppProfile();
    expect(profile.publicationAllowed).toBe(false);
    expect(profile.cloudUsed).toBe(false);
    expect(profile.wabiExecutionAllowed).toBe(false);
    expect(profile.unknownZipCodeExecuted).toBe(false);
    expect(profile.assetsCopiedWithoutProvenance).toBe(false);
  });

  it("emits a safe Windows app manifest when packaged", () => {
    const manifestPath = resolve(process.cwd(), "public/asset-manifest/windows_app_manifest_v1_4.json");
    const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
    expect(manifest.schema).toBe("duat/windows-app-manifest/v1.4");
    expect(manifest.fingerprint).toBe("DUAT-v1.4-WINAPP-CONVERSION");
    expect(manifest.wrapper).toBe("native_dotnet_edge_app_mode");
    expect(manifest.executable.sha256).toMatch(/^[A-F0-9]{64}$/);
    expect(manifest.app.file_count).toBeGreaterThan(0);
    expect(manifest.runtime.loopback_only).toBe(true);
    expect(manifest.runtime.canvas_fallback_preserved).toBe(true);
    expect(manifest.runtime.iso3d_toggle_preserved).toBe(true);
    expect(manifest.boundaries.publication_allowed).toBe(false);
    expect(manifest.boundaries.wabi_execution_allowed).toBe(false);
    expect(manifest.boundaries.cloud_used).toBe(false);
    expect(manifest.boundaries.mcp_execution).toBe(false);
    expect(manifest.boundaries.unknown_zip_code_executed).toBe(false);
  });
});
