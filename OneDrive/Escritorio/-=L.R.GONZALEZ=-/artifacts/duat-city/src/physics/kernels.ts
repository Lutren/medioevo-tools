import type { CityState } from "../core/types";
import type { PhysicsBody, PhysicsWorld } from "./types";
import { applyForces, integrateBody } from "./integrator";
import { resolveBounds, resolveSolidTileCollision } from "./collisions";

export interface PhysicsKernel {
  step: (state: CityState, bodies: PhysicsBody[], dt: number) => number;
}

export const NewtonianKernel: PhysicsKernel = {
  step: (state, bodies, dt) => {
    let resolved = 0;
    const bounds = { x: 0, y: 0, width: state.width, height: state.height };
    for (const body of bodies) {
      const force = applyForces(body, state);
      integrateBody(body, dt, force.ax, force.ay);
      if (resolveBounds(body, bounds)) { /* handle bounds */ }
      if (resolveSolidTileCollision(body, state)) resolved++;
    }
    return resolved;
  }
};

export const FractalKernel: PhysicsKernel = {
  step: (state, bodies, dt) => {
    // Non-Euclidean Integration: Force field based on distance from center (Nexus)
    const centerX = state.width / 2;
    const centerY = state.height / 2;
    
    for (const body of bodies) {
      const dx = body.x - centerX;
      const dy = body.y - centerY;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;
      
      // Warped space: Force scales with inverse distance, creating "gravity wells"
      const warpFactor = 10 / (dist * 0.1 + 1);
      
      // Rotate force vector to simulate non-euclidean "spiral" motion
      const forceX = -dy * warpFactor * 0.05;
      const forceY = dx * warpFactor * 0.05;
      
      body.vx += forceX * dt;
      body.vy += forceY * dt;
      body.x += body.vx * dt;
      body.y += body.vy * dt;
    }
    return 0;
  }
};
