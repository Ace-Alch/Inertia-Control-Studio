# Validation notes

These results describe **numerical simulation and source-level tests**, not experiments on actual hardware. Refer to the JSON files in [`reports/`](../reports) for the exact configurations and recorded outputs.

## Default multi-link swing-up

The provided release report `multi-validation.json` contains 20 randomized trials for each system, using seed 83421, 5% physical parameter uncertainty, small cart impulse disturbances and randomized downward initial conditions.

| Links | Successful trials | Reported nominal capture time | Default peak actual force | Nominal maximum cart travel |
| --- | ---: | ---: | ---: | ---: |
| 2 | 20/20 | ~6.001 s | ~10.37 N | ~0.457 m |
| 3 | 20/20 | ~7.001 s | ~13.36 N | ~0.662 m |

The capture/force/travel data come from `swing-tests.json`; the randomized success rates come from `multi-validation.json`. They are distinct tests and should not be interpreted as one combined dataset.

**Conditions and limits:** results apply to the included default plant and prescribed disturbance envelope. Custom geometries, controller settings, disturbances, sensor errors, or true hardware can produce different results. These results are not a general stabilization guarantee.

## Additional verification

- Euler–Lagrange residual comparisons and passive energy decay: `realism-tests.json`.
- Local balance, delayed controller start, actuator limits, and synthetic calibration: `physics-tests.json`.
- Numerical RK4 convergence and single-link randomized outcomes: `validation-report.json`.
- Interactive DOM workflows and optimization checks: `dom-tests.json`, `compatibility-tests.json`, `demo-tests.json`.
- The guided optimization demonstration improved from 0/20 to 12/20 successful trials in the recorded case. This is a *deliberately weak baseline*, not an estimate of general AI or controller performance.

## Reproduce

```bash
npm ci
python build.py
npm test
npm run validate
npm run validate:multi
npm run test:compat
npm run test:demo
```

Node.js 22.22.2+ or 24.15+ and Python 3 are used for these commands. Optional trajectory re-optimization has additional Python dependencies; see the [engineering guide](ENGINEERING_GUIDE.md).

## Limits

The planar model excludes flexible-body behavior, motor electrical/thermal losses, joint backlash, rail compliance, and hardware-specific actuator and sensor effects. The source-level DOM suite is not a complete GPU/WebGL or cross-device test. The included screenshot shows the headless-browser canvas fallback, and should not be interpreted as physical validation.
