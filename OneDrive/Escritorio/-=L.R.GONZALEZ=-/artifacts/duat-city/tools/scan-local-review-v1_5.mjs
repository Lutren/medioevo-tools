import { createHash } from "node:crypto";
import { createReadStream, existsSync } from "node:fs";
import { mkdir, open, opendir, readFile, stat, writeFile } from "node:fs/promises";
import { dirname, extname, relative, resolve, sep } from "node:path";
import { inflateRawSync } from "node:zlib";

const defaultRoots = [
  "C:\\Users\\L-Tyr\\OneDrive\\Escritorio\\-=L.R.GONZALEZ=-",
  "C:\\Users\\L-Tyr\\OneDrive\\Escritorio\\-= BRAIN_OS =-",
];

const outputPath = resolve(process.argv[2] ?? "docs/asset_manifest_v1_5.json");
const roots = process.argv.slice(3).length > 0 ? process.argv.slice(3).map(value => resolve(value)) : defaultRoots;
const keywords = ["duat", "simulacion", "simulacion", "smallvile", "smallville", "rpv", "metroidvania", "isometrico", "isometric", "iso3d", "canvas", "pixel", "light", "audio", "game-feel", "gamefeel", "agent life", "brainruntime", "brain runtime", "rpg"];
const hardDenySegments = new Set([".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "target"]);
const generatedSegments = new Set(["dist", "build", "release"]);
const relevantExtensions = new Set([".ts", ".tsx", ".js", ".jsx", ".mjs", ".json", ".md", ".txt", ".css", ".html", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".wav", ".mp3", ".ogg", ".zip", ".exe"]);
const textExtensions = new Set([".ts", ".tsx", ".js", ".jsx", ".mjs", ".json", ".md", ".txt", ".css", ".html"]);
const hashLargeLimitBytes = 200 * 1024 * 1024;
const zipEntryHashLimitBytes = 8 * 1024 * 1024;

const entries = [];
const zipReports = [];
const skipped = [];
const totals = {
  filesSeen: 0,
  relevantFiles: 0,
  zipFilesSeen: 0,
  zipEntriesSeen: 0,
  zipEntriesIncluded: 0,
  zipEntriesHashed: 0,
  unreadableFiles: 0,
};

const scanTargets = await expandRoots(roots);

for (const target of scanTargets) {
  if (!existsSync(target.path)) {
    skipped.push({ path: target.path, reason: "target_missing" });
    continue;
  }
  const info = await stat(target.path);
  if (info.isDirectory()) {
    await walk(target.root, target.path);
  } else if (info.isFile()) {
    totals.filesSeen += 1;
    await inspectFile(target.root, target.path).catch(error => {
      totals.unreadableFiles += 1;
      skipped.push({ path: target.path, reason: `inspect_failed:${messageOf(error)}` });
    });
  }
}

const classificationCounts = countBy(entries, "classification");
const categoryCounts = countBy(entries, "category");
const recommendationCounts = countBy(entries, "integrationRecommendation");

const manifest = {
  schema: "duat/local-full-review-asset-manifest/v1.5",
  fingerprint: "DUAT-v1.5-FULL-LOCAL-REVIEW",
  generatedAt: new Date().toISOString(),
  roots,
  scanTargets: scanTargets.map(target => target.path),
  keywords,
  boundary: {
    level: "LEVEL_4_LOCAL_ONLY",
    metadataOnlyForUnknownSources: true,
    zipExtractionToDisk: false,
    unknownZipCodeExecuted: false,
    assetsCopiedOutsideAllowlist: false,
    publicationAllowed: false,
    cloudUsed: false,
    mcpExecution: false,
    wabiExecution: false,
    ownerProvidedIpBoundary: "OWNER_PROVIDED / INTERNAL_PROTECTED_IP",
  },
  totals,
  classificationCounts,
  categoryCounts,
  recommendationCounts,
  zipReports,
  skipped,
  entries,
};

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, JSON.stringify(manifest, null, 2), "utf8");
console.log(JSON.stringify({ ok: true, outputPath, totals, classificationCounts }, null, 2));

async function walk(root, dir) {
  let handle;
  try {
    handle = await opendir(dir);
  } catch (error) {
    skipped.push({ path: dir, reason: `opendir_failed:${messageOf(error)}` });
    return;
  }
  for await (const item of handle) {
    const fullPath = resolve(dir, item.name);
    if (item.isDirectory()) {
      if (shouldSkipDir(root, fullPath)) {
        skipped.push({ path: fullPath, reason: "excluded_dir" });
        continue;
      }
      await walk(root, fullPath);
      continue;
    }
    if (!item.isFile()) continue;
    totals.filesSeen += 1;
    await inspectFile(root, fullPath).catch(error => {
      totals.unreadableFiles += 1;
      skipped.push({ path: fullPath, reason: `inspect_failed:${messageOf(error)}` });
    });
  }
}

function shouldSkipDir(root, fullPath) {
  const parts = pathParts(relative(root, fullPath));
  if (parts.some(part => hardDenySegments.has(part.toLowerCase()))) return true;
  if (parts.some(part => generatedSegments.has(part.toLowerCase()))) {
    const normalized = normalizePath(fullPath).toLowerCase();
    return !(normalized.includes("/artifacts/duat-city/dist/winapp") || normalized.includes("/artifacts/duat-city/docs"));
  }
  return false;
}

async function inspectFile(root, fullPath) {
  const info = await stat(fullPath);
  const ext = extname(fullPath).toLowerCase();
  const normalized = normalizePath(fullPath);
  const pathKeywordHits = keywordHits(normalized);
  const isZip = ext === ".zip";
  const relevantByPath = isRelevantPath(normalized, ext, pathKeywordHits);
  const contentHits = relevantByPath || !textExtensions.has(ext) ? [] : await keywordHitsInText(fullPath);
  const hits = [...new Set([...pathKeywordHits, ...contentHits])];
  const includeFile = relevantByPath || hits.length > 0 || isDuatCitySource(normalized);

  if (isZip) {
    totals.zipFilesSeen += 1;
    await inspectZip(root, fullPath, info, includeFile, hits);
  }
  if (!includeFile || !relevantExtensions.has(ext)) return;

  totals.relevantFiles += 1;
  const classification = classifyPath(normalized, ext);
  const category = categorizePath(normalized, ext);
  entries.push({
    id: stableId("file", fullPath),
    sourceKind: "file",
    sourceRoot: root,
    path: fullPath,
    relativePath: relative(root, fullPath),
    filename: fullPath.split(/[\\/]/).pop(),
    extension: ext.replace(".", "") || "none",
    sizeBytes: info.size,
    sha256: info.size <= hashLargeLimitBytes ? await sha256File(fullPath) : null,
    sha256Status: info.size <= hashLargeLimitBytes ? "ok" : "skipped_large_file_metadata_only",
    type: typeForExtension(ext),
    category,
    classification,
    keywordHits: hits,
    R_est: metricsFor(classification).R_est,
    Phi_eff_est: metricsFor(classification).Phi_eff_est,
    integrationRecommendation: recommendationFor(classification, category),
    licenseBoundary: licenseBoundaryFor(normalized),
    notes: notesFor(normalized, classification, category),
  });
}

async function inspectZip(root, fullPath, info, includeZip, fileHits) {
  const zipSha256 = info.size <= hashLargeLimitBytes ? await sha256File(fullPath) : null;
  const classification = classifyPath(normalizePath(fullPath), ".zip");
  const report = {
    path: fullPath,
    relativePath: relative(root, fullPath),
    sizeBytes: info.size,
    sha256: zipSha256,
    classification,
    ok: false,
    entryCount: 0,
    includedEntries: 0,
    error: null,
  };
  if (includeZip) {
    entries.push({
      id: stableId("zip", fullPath),
      sourceKind: "zip",
      sourceRoot: root,
      path: fullPath,
      relativePath: relative(root, fullPath),
      filename: fullPath.split(/[\\/]/).pop(),
      extension: "zip",
      sizeBytes: info.size,
      sha256: zipSha256,
      sha256Status: zipSha256 ? "ok" : "skipped_large_file_metadata_only",
      type: "archive",
      category: "zip_container",
      classification,
      keywordHits: fileHits,
      R_est: metricsFor(classification).R_est,
      Phi_eff_est: metricsFor(classification).Phi_eff_est,
      integrationRecommendation: recommendationFor(classification, "zip_container"),
      licenseBoundary: licenseBoundaryFor(fullPath),
      notes: "ZIP container inventoried only. No code or asset payload was executed or copied.",
    });
  }
  try {
    const zipEntries = await listZipEntries(fullPath);
    report.ok = true;
    report.entryCount = zipEntries.length;
    totals.zipEntriesSeen += zipEntries.length;
    const zipPathRelevant = includeZip || fileHits.length > 0;
    for (const zipEntry of zipEntries) {
      const normalizedEntry = normalizePath(zipEntry.name);
      const entryHits = keywordHits(normalizedEntry);
      if (!zipPathRelevant && entryHits.length === 0) continue;
      if (!relevantExtensions.has(extname(zipEntry.name).toLowerCase()) && entryHits.length === 0) continue;
      const entryClassification = classifyPath(`${normalizePath(fullPath)}/${normalizedEntry}`, extname(zipEntry.name).toLowerCase());
      const entryCategory = categorizePath(normalizedEntry, extname(zipEntry.name).toLowerCase());
      const entryHash = entryClassification === "reference_only" || entryClassification === "reject"
        ? { sha256: null, status: "container_hash_only_for_protected_or_rejected_entry" }
        : await sha256ZipEntry(fullPath, zipEntry).catch(error => ({ sha256: null, status: `hash_failed:${messageOf(error)}` }));
      if (entryHash.sha256) totals.zipEntriesHashed += 1;
      totals.zipEntriesIncluded += 1;
      report.includedEntries += 1;
      entries.push({
        id: stableId("zip-entry", `${fullPath}::${zipEntry.name}`),
        sourceKind: "zip_entry",
        sourceRoot: root,
        path: `${fullPath}::${zipEntry.name}`,
        relativePath: `${relative(root, fullPath)}::${zipEntry.name}`,
        filename: zipEntry.name.split(/[\\/]/).pop(),
        extension: extname(zipEntry.name).replace(".", "").toLowerCase() || "none",
        sizeBytes: zipEntry.uncompressedSize,
        compressedSizeBytes: zipEntry.compressedSize,
        sha256: entryHash.sha256,
        sha256Status: entryHash.status,
        containerSha256: zipSha256,
        compressionMethod: zipEntry.compressionMethod,
        type: typeForExtension(extname(zipEntry.name).toLowerCase()),
        category: entryCategory,
        classification: entryClassification,
        keywordHits: entryHits.length > 0 ? entryHits : fileHits,
        R_est: metricsFor(entryClassification).R_est,
        Phi_eff_est: metricsFor(entryClassification).Phi_eff_est,
        integrationRecommendation: recommendationFor(entryClassification, entryCategory),
        licenseBoundary: licenseBoundaryFor(`${fullPath}/${zipEntry.name}`),
        notes: "ZIP entry hashed in memory when size/method allowed; no extraction to disk and no execution.",
      });
    }
  } catch (error) {
    report.error = messageOf(error);
  }
  zipReports.push(report);
}

async function expandRoots(inputRoots) {
  const targets = [];
  for (const root of inputRoots.map(value => resolve(value))) {
    const lower = normalizePath(root).toLowerCase();
    const focus = [];
    if (lower.endsWith("/-=l.r.gonzalez=-")) {
      focus.push(
        "artifacts/duat-city",
        "research/geodia-social-observatory",
        "research/duat-predictive-registry",
        "packages/open-dev/duat-genesis",
        "game-private",
        "MEDIOEVO_LIVE_TREE/01_SOURCE_CARDS",
        "docs/product",
        "docs/developer",
        "docs/intake",
      );
    } else if (lower.endsWith("/-= brain_os =-")) {
      focus.push(
        "DUAT ASSETS",
        "03_DUAT",
        "03_DUAT_GEODIA",
        "06_BOOKS_RPG_PROTECTED",
        "01_SOURCE_CARDS",
        "00_START_HERE/LIVE_STATE",
        "08_QA_WITNESSLOG",
        "-=LR WORKING BENCH=-/Assets Du WABI",
      );
      await addMatchingFiles(root, root, targets);
    } else {
      focus.push(".");
    }
    for (const item of focus) {
      const path = resolve(root, item);
      if (existsSync(path)) targets.push({ root, path });
    }
  }
  const unique = new Map();
  for (const target of targets) unique.set(target.path.toLowerCase(), target);
  return [...unique.values()];
}

async function addMatchingFiles(root, dir, targets) {
  let handle;
  try {
    handle = await opendir(dir);
  } catch {
    return;
  }
  for await (const item of handle) {
    const fullPath = resolve(dir, item.name);
    if (item.isDirectory()) continue;
    const normalized = normalizePath(fullPath);
    if (keywordHits(normalized).length > 0 || extname(item.name).toLowerCase() === ".zip") {
      targets.push({ root, path: fullPath });
    }
  }
}

async function listZipEntries(fullPath) {
  const file = await open(fullPath, "r");
  try {
    const info = await file.stat();
    const tailSize = Math.min(info.size, 66_000);
    const tail = Buffer.alloc(tailSize);
    await file.read(tail, 0, tailSize, info.size - tailSize);
    let eocd = -1;
    for (let i = tail.length - 22; i >= 0; i--) {
      if (tail.readUInt32LE(i) === 0x06054b50) {
        eocd = i;
        break;
      }
    }
    if (eocd < 0) throw new Error("zip_eocd_not_found");
    const entryCount = tail.readUInt16LE(eocd + 10);
    const cdSize = tail.readUInt32LE(eocd + 12);
    const cdOffset = tail.readUInt32LE(eocd + 16);
    if (entryCount === 0xffff || cdOffset === 0xffffffff || cdSize === 0xffffffff) {
      throw new Error("zip64_not_supported_metadata_only");
    }
    const central = Buffer.alloc(cdSize);
    await file.read(central, 0, cdSize, cdOffset);
    const entriesOut = [];
    let offset = 0;
    while (offset < central.length) {
      if (central.readUInt32LE(offset) !== 0x02014b50) throw new Error(`bad_central_directory_signature_at_${offset}`);
      const flags = central.readUInt16LE(offset + 8);
      const compressionMethod = central.readUInt16LE(offset + 10);
      const compressedSize = central.readUInt32LE(offset + 20);
      const uncompressedSize = central.readUInt32LE(offset + 24);
      const nameLength = central.readUInt16LE(offset + 28);
      const extraLength = central.readUInt16LE(offset + 30);
      const commentLength = central.readUInt16LE(offset + 32);
      const localHeaderOffset = central.readUInt32LE(offset + 42);
      const encoding = (flags & 0x800) ? "utf8" : "latin1";
      const name = central.subarray(offset + 46, offset + 46 + nameLength).toString(encoding);
      entriesOut.push({ name, compressionMethod, compressedSize, uncompressedSize, localHeaderOffset });
      offset += 46 + nameLength + extraLength + commentLength;
    }
    return entriesOut;
  } finally {
    await file.close();
  }
}

async function sha256ZipEntry(fullPath, zipEntry) {
  if (zipEntry.name.endsWith("/") || zipEntry.uncompressedSize === 0) return { sha256: null, status: "directory_or_empty" };
  if (zipEntry.uncompressedSize > zipEntryHashLimitBytes || zipEntry.compressedSize > zipEntryHashLimitBytes) {
    return { sha256: null, status: "skipped_large_zip_entry_metadata_only" };
  }
  if (![0, 8].includes(zipEntry.compressionMethod)) return { sha256: null, status: `unsupported_compression_${zipEntry.compressionMethod}` };
  const file = await open(fullPath, "r");
  try {
    const header = Buffer.alloc(30);
    await file.read(header, 0, 30, zipEntry.localHeaderOffset);
    if (header.readUInt32LE(0) !== 0x04034b50) throw new Error("bad_local_header_signature");
    const nameLength = header.readUInt16LE(26);
    const extraLength = header.readUInt16LE(28);
    const dataOffset = zipEntry.localHeaderOffset + 30 + nameLength + extraLength;
    const compressed = Buffer.alloc(zipEntry.compressedSize);
    await file.read(compressed, 0, zipEntry.compressedSize, dataOffset);
    const data = zipEntry.compressionMethod === 0 ? compressed : inflateRawSync(compressed);
    return { sha256: createHash("sha256").update(data).digest("hex").toUpperCase(), status: "ok" };
  } finally {
    await file.close();
  }
}

function isRelevantPath(normalized, ext, hits) {
  if (hits.length > 0) return true;
  if (isDuatCitySource(normalized)) return true;
  if (normalized.toLowerCase().includes("/duat assets/")) return true;
  if (normalized.toLowerCase().includes("/03_duat")) return true;
  if (normalized.toLowerCase().includes("/03_duat_geodia")) return true;
  if (normalized.toLowerCase().includes("/06_books_rpg_protected")) return true;
  if (normalized.toLowerCase().includes("/active_asset-")) return true;
  return ext === ".zip" && normalized.toLowerCase().includes("medioevo");
}

function isDuatCitySource(normalized) {
  const value = normalized.toLowerCase();
  return value.includes("/artifacts/duat-city/src/")
    || value.includes("/artifacts/duat-city/public/")
    || value.includes("/artifacts/duat-city/docs/")
    || value.includes("/artifacts/duat-city/tools/")
    || value.includes("/artifacts/duat-city/dist/winapp/");
}

async function keywordHitsInText(fullPath) {
  let content;
  try {
    content = await readFile(fullPath, "utf8");
  } catch {
    return [];
  }
  const sample = content.slice(0, 1_000_000).toLowerCase();
  return keywords.filter(keyword => sample.includes(keyword));
}

function keywordHits(value) {
  const lower = value.toLowerCase();
  return keywords.filter(keyword => lower.includes(keyword));
}

function classifyPath(value, ext) {
  const lower = normalizePath(value).toLowerCase();
  if (lower.includes("/.git/") || lower.includes("/node_modules/") || lower.includes("/.env") || lower.includes("secret") || lower.includes("token") || lower.includes("credential")) return "reject";
  if (lower.includes("/06_books_rpg_protected/") || lower.includes("/game-private/") || lower.includes("/metaevo-tcg/") || lower.includes("/tcg/") || lower.includes("/runtime/game_bridge/") || lower.includes("books_rpg_protected") || lower.includes("lore_raw") || lower.includes("libros_es_completos")) return "reference_only";
  if (lower.includes("/artifacts/duat-city/src/") || lower.includes("/artifacts/duat-city/public/") || lower.includes("/artifacts/duat-city/dist/winapp/") || lower.includes("/artifacts/duat-city/docs/") || lower.includes("/artifacts/duat-city/tools/")) return "allowlist";
  if (lower.includes("/duat assets/") || lower.includes("/03_duat") || lower.includes("/03_duat_geodia") || lower.includes("/active_asset-") || ext === ".zip") return "adapt";
  return "reference_only";
}

function categorizePath(value, ext) {
  const lower = normalizePath(value).toLowerCase();
  if (ext === ".zip") return "zip_container";
  if ([".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"].includes(ext)) return "asset_visual";
  if ([".wav", ".mp3", ".ogg"].includes(ext)) return "asset_audio";
  if ([".ts", ".tsx", ".js", ".jsx", ".mjs", ".css", ".html"].includes(ext)) return "code";
  if (ext === ".json") return lower.includes("manifest") ? "manifest" : "data";
  if ([".md", ".txt"].includes(ext)) return lower.includes("lore") || lower.includes("rpg") ? "lore" : "reference_doc";
  if (ext === ".exe") return "executable";
  if (lower.includes("audio") || lower.includes("gamefeel") || lower.includes("game-feel")) return "audio_gamefeel";
  if (lower.includes("brain")) return "brainruntime";
  if (lower.includes("rpg") || lower.includes("metroidvania")) return "rpg_bridge";
  return "reference";
}

function typeForExtension(ext) {
  if ([".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"].includes(ext)) return "asset";
  if ([".wav", ".mp3", ".ogg"].includes(ext)) return "audio";
  if ([".ts", ".tsx", ".js", ".jsx", ".mjs", ".css", ".html"].includes(ext)) return "code";
  if (ext === ".json") return "json";
  if ([".md", ".txt"].includes(ext)) return "text";
  if (ext === ".zip") return "archive";
  if (ext === ".exe") return "executable";
  return "other";
}

function metricsFor(classification) {
  if (classification === "allowlist") return { R_est: 0.14, Phi_eff_est: 0.84 };
  if (classification === "adapt") return { R_est: 0.29, Phi_eff_est: 0.68 };
  if (classification === "reference_only") return { R_est: 0.42, Phi_eff_est: 0.56 };
  return { R_est: 0.62, Phi_eff_est: 0.31 };
}

function recommendationFor(classification, category) {
  if (classification === "allowlist") return "keep_integrated_and_test";
  if (classification === "adapt") return category === "zip_container" ? "metadata_review_then_selective_extraction_only" : "adapt_only_with_ficha_hash_and_tests";
  if (classification === "reference_only") return "reference_only_no_copy_no_public_release";
  return "reject_from_integration_and_release";
}

function licenseBoundaryFor(value) {
  const lower = normalizePath(value).toLowerCase();
  if (lower.includes("duat-city") || lower.includes("duat assets") || lower.includes("active_asset-")) return "OWNER_PROVIDED / INTERNAL_PROTECTED_IP";
  if (lower.includes("06_books_rpg_protected") || lower.includes("lore") || lower.includes("rpg")) return "OWNER_PROVIDED / PRIVATE_RPG_OR_LORE";
  return "UNKNOWN_REVIEW_REQUIRED";
}

function notesFor(value, classification, category) {
  if (classification === "allowlist") return "Already inside DUAT app/reviewed artifact lane; validate by tests, build and QA.";
  if (classification === "adapt") return "Candidate for selective extraction only. Needs ficha, provenance, target lane and test evidence before copy.";
  if (classification === "reference_only") return `Private/protected or lore-heavy material. Use as design reference only; do not copy payload into app/release. Category=${category}.`;
  return "Rejected by safety boundary, secret-like path, vendor/generated state or unsupported integration risk.";
}

function normalizePath(value) {
  return String(value).replaceAll("\\", "/");
}

function pathParts(value) {
  return value.split(/[\\/]/).filter(Boolean);
}

function countBy(items, key) {
  return items.reduce((acc, item) => {
    const value = item[key] ?? "unknown";
    acc[value] = (acc[value] ?? 0) + 1;
    return acc;
  }, {});
}

function stableId(prefix, value) {
  return `${prefix}-${createHash("sha256").update(value).digest("hex").slice(0, 16)}`;
}

function messageOf(error) {
  return error instanceof Error ? error.message : String(error);
}

function sha256File(fullPath) {
  return new Promise((resolveHash, rejectHash) => {
    const hash = createHash("sha256");
    const stream = createReadStream(fullPath);
    stream.on("error", rejectHash);
    stream.on("data", chunk => hash.update(chunk));
    stream.on("end", () => resolveHash(hash.digest("hex").toUpperCase()));
  });
}
