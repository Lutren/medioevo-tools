import type { QMeaning, QState } from "./types";

export function encodeQState(presence: boolean, difference: boolean): QState {
  if (!presence && !difference) return "00";
  if (!presence && difference) return "01";
  if (presence && !difference) return "10";
  return "11";
}

export function decodeQState(state: QState): { presence: boolean; difference: boolean } {
  return {
    presence: state === "10" || state === "11",
    difference: state === "01" || state === "11",
  };
}

export function qStateToIndex(state: QState): 0 | 1 | 2 | 3 {
  if (state === "00") return 0;
  if (state === "01") return 1;
  if (state === "10") return 2;
  return 3;
}

export function qStateFromIndex(index: number): QState {
  if (index === 1) return "01";
  if (index === 2) return "10";
  if (index === 3) return "11";
  return "00";
}

export function qStateMeaning(state: QState): QMeaning {
  if (state === "00") return "SILENCE_STABLE";
  if (state === "01") return "ABSENCE_SIGNIFICANT";
  if (state === "10") return "PRESENCE_STABLE";
  return "EVENT_ACTIVE";
}

export function qStateLabel(state: QState): string {
  if (state === "00") return "silence stable";
  if (state === "01") return "absence significant";
  if (state === "10") return "presence stable";
  return "event active";
}

export function qStateColor(state: QState): string {
  if (state === "00") return "rgba(30, 39, 52, 0.20)";
  if (state === "01") return "rgba(255, 170, 48, 0.78)";
  if (state === "10") return "rgba(54, 216, 170, 0.58)";
  return "rgba(105, 228, 255, 0.86)";
}

