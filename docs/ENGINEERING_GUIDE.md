# Engineering reference — Inertia Control Studio 4.1


## Version 4.1: multi-link swing-up fix

- Replaced the multi-link energy-only attempt with constrained trajectory optimization and feedback tracking.
- Default two-link capture: 6.001 s; peak actual force 10.37 N; maximum cart travel 0.458 m.
- Default three-link capture: 7.001 s; peak actual force 13.36 N; maximum cart travel 0.662 m.
- Both remain balanced through 30 s, with zero rail hits, at 1 ms and 0.5 ms integration steps.
- Independent test seed 83421: 20/20 successful trials for each count with 5% physical uncertainty,
  randomized downward starts, sensor perturbations and a 0.1 N·s cart disturbance.
  This is a limited test result, not a guarantee for arbitrary models or disturbances.
- The checks dashboard now tests actual downward-start swing-up for both link counts.
- The main physics, actuator limits, gravity and renderer are unchanged by this fix.

## Version 4 changes and recommended presets

- Default bearing losses are explicit. Joint viscous damping is 0.006 N·m·s/rad.
  Smooth dry bearing friction is 0.0006 N·m, with a 0.05 rad/s transition scale.
  These are illustrative bench parameters, not identified hardware measurements.
- A failed capture attempt stops requesting motor force after 12 seconds.
  Motion then decays under physical losses. No state is frozen or overwritten.
  Retry controller starts a new attempt.
- Speeds: 1×, 2×, 4× and 8×, plus the existing slow-motion modes.
  The RK4 step does not increase at higher playback speeds.
  The display reports achieved speed as well as requested speed. A slow CPU can limit playback.
- Every tab has presets. Laboratory presets use a 0.5 ms integration step.
- Start with **Passive · 3** to inspect energy decay. Motor force stays zero.
- Use **Swing-up · 1** for a tested downward-start demonstration.
- Use **Swing-up · 2** or **Swing-up · 3** for downward-rest swing-up followed by LQR balance.
  These presets use the default physical model and a 0.5 ms integration step.
- In Optimization, select **Guided tuning demo**, then **Start training**.
  The demo deliberately starts with an insufficient energy gain and tunes that gain.
  It uses real simulations, separate validation and unseen tests. It does not fake improvement.
  Select **Apply best and run** to see the result in the laboratory.
- Use **Tune current controller** for your own settings and **500-trial robustness** for a longer study.
- New test reports cover passive energy decay, independent Euler–Lagrange equations,
  precision presets, capture timeout, and both worker and compatibility execution.

Long motion is not always a numerical error. An active controller supplies energy.
A deliberately low-loss model also takes longer to settle. The normal presets now show
clear physical energy decay, while lossless reference checks intentionally conserve energy.

## Open the app

Open **index.html** in a current desktop Chrome, Edge, or Firefox browser.
The file includes the 3D renderer. No internet connection, API key, account, or build step is needed.
WebGL 2 is needed for the 3D view. A canvas view is used if WebGL is unavailable.

For localhost, install Python 3 and run:

    python start_server.py

On Windows, you can instead double-click **Start-Windows.bat**.
Open http://127.0.0.1:8000/index.html if the browser does not open automatically.
Press Ctrl+C in the terminal to stop the server.

## Laboratory

The cart starts at rest. All links hang downward. The controller is off.
Select 1, 2, or 3 links. Select LQR, PID, or a Sugeno fuzzy controller.
Press Start controller to enable swing-up and stabilization. Use LQR for two or three links.
Their coordinated swing-up uses force-reference tracking followed by stationary LQR.
Drag a body to apply a bounded external spring-damper force. The physical state is not teleported.
Use the impulse controls for a known cart disturbance.
The emergency stop sets the command to zero. Actual force decays through the motor dynamics.

The scene includes machined rods, bearings, fasteners, linear rails, end stops, a motor housing,
a frame, studio lights, and shadows. Camera controls affect the view only.
Use Studio, Front, or Close views, mouse-wheel zoom, full screen, and PNG snapshots.

Monitors show every link angle and angular velocity, cart position, commanded and actual force,
kinetic and potential energy, and a phase plot. Point at a plot for sample values. Click a legend
to hide a series. Use the wheel to change the vertical scale. Expand a plot for full-screen use.
Freeze affects monitors only. Recording uses simulation-time samples, not animation frames.
CSV exports contain SI data and absolute link angles in radians. Screen angle plots use degrees.

## Engineering

Use the numeric control cards. No raw JSON editing is needed.
Apply settings starts a new experiment and switches control off.
Mass and length changes do not silently change the center of mass or inertia.
After changing a rod's dimensions, use its **Use uniform rod COM and inertia** button when appropriate.
For a uniform slender rod, COM = L/2 and J = m L²/12.
Custom COM and inertia are allowed within geometric bounds.
Model JSON files store physical parameters and gains for later use.

## Optimization

1. Set the physical model and the manual controller in Engineering.
2. Open Optimization. Select Controller auto-tuning.
3. Select ranges and cost weights. Start with a small candidate budget to check runtime.
4. Press Start training. Pause, Continue, and Stop remain available between simulation chunks. The live candidate display shows actual trial positions and progress. If a browser blocks workers, the same optimizer runs in cooperative compatibility mode.
5. After training, the worker runs the original and best validated controller on the same unseen test set.
6. Save a checkpoint or the best model. Apply best loads the result into the laboratory.

Auto uses Differential Evolution. Random search is also implemented.
Every candidate is evaluated on fixed training and separate validation conditions.
The controller is designed for the nominal plant; it does not receive the hidden randomized model.
The randomization changes masses, dimensions, losses, motor strength and lag, sensor noise and delay.
Initial states and cart impulses also vary. Gravity is never tuned during balancing.
Eight progressive levels are available. Validation and final tests always use the full selected difficulty.
No improvement is promised. If no candidate beats the baseline within the validation safeguards,
the original model remains the best. The final iteration does not overwrite a better checkpoint.

Validation rejects higher failure rates, higher rail failure rates, and unacceptable cart-travel increases.
Hard actuator limits still apply in every trial. A rail contact ends a training trial as a failure.
Success requires two continuous seconds at the end of the episode with all angles below 0.06 rad,
all angular velocities below 0.3 rad/s, and cart position within 0.15 m of the center.

The eight weights apply to normalized angle RMS, cart RMS, actuator effort, settling time,
saturation, rail failure, stabilization failure, and recovery. Switching adds a small penalty.
Angle RMS includes the whole swing-up, not just balanced motion.
Control effort is the integral of force squared. Mechanical work is the integral of absolute force times cart velocity.
Neither is electrical energy consumption.

Checkpoints store the original model, best model, optimizer population, RNG state, cost weights,
experiment settings, validation scores, version, and training history.
A stopped job can resume from its most recent completed iteration.
Once testing starts, that run is locked against further tuning. Start automatically selects a fresh seed if the previous seed was used. The new seed is shown in the dashboard.
Test-set locks and the latest checkpoint are stored on the device where browser storage is available.
Download checkpoints for portable copies. Applying an old successful model does not erase the test lock.

## Physical calibration

Calibration is separate from controller tuning. Import at least 30 measured CSV samples:

    time,cart_position,cart_velocity,theta1,omega1,control_force

For two or three links, also include theta2,omega2 and theta3,omega3 as applicable.
All values use SI units. Angles are absolute, with zero upright.
The force column must be actual measured cart force, not a motor command or voltage.
Each data segment is replayed with the same recorded force using a zero-order hold.
This version estimates cart viscous/Coulomb friction and relative joint damping.
Mass, length, COM, inertia, gravity, and actuator capability remain fixed during calibration.
Actuator identification from commanded inputs is not implemented in this release.

The first 60% of samples form the training segment, the next 20% validation, and the last 20% test.
Segments start from their measured initial state. Fit error is a normalized state RMSE with wrapped angle differences.
A dataset whose test segment has already been used cannot be reused for further calibration in the same saved study.
For strong experimental evidence, use separate physical recordings under varied excitation.
Importing a file does not prove that it came from hardware. The app never labels imported data as verified hardware evidence.

## Physics and limits

The model uses a coupled nonlinear rigid-body mass matrix for a translating cart and up to three serial links.
It includes COM rotational inertia, gravity, relative joint damping, smooth dry bearing friction, smooth Coulomb/viscous cart friction,
first-order motor lag, slew rate, force dead zone, saturation, sensor noise, encoder quantization, and delay.
RK4 integrates the mechanical state and motor force together. Default step: 1 ms. Precision presets use 0.5 ms. Controller period: 10 ms.
Rail impacts use coupled impulses with restitution and discrete penetration correction.

The main model is planar and rigid. It does not model flexible rods, structural resonances,
static stiction, joint backlash, rail compliance, motor electrical losses, heating, or sensor-specific filtering.
The single noise setting uses native SI units for each observed mechanical state. This is a simplified sensor model.
LQR feedback assumes motor force and mechanical state measurements are available.
The displayed assembly is a visualization of the idealized model, not a manufacturing CAD specification.

Two- and three-link LQR controllers now swing up from downward rest with the default plant.
They use offline optimized force references and time-varying LQR feedback for 6 and 7 seconds,
then stationary LQR. The controller only commands the physical cart motor. Reference states
are used to calculate feedback errors; they never overwrite the simulated state.
The force references include nominal rod inertia, bearing losses and motor lag.
The plan starts within 0.2 rad of downward, 0.2 m of cart center and 0.4 native SI velocity.
Custom physical models, large disturbances, PID and fuzzy multi-link controllers do not have
the same validated operating range. Use the supplied presets to reproduce the successful runs.
Energy gain and energy-swing centering/damping apply to energy shaping, not the multi-link
force plan. The optimization UI excludes these inactive gains for multi-link LQR.
A failed trial remains a failure. The app does not reset the plant or add an invisible torque to make a controller succeed.
RL and neural motion generation are not implemented.

## Verification

- Energy conservation and local LQR balance checked for 1–3 links.
- Single-link small-angle frequency checked against its analytical expression.
- Delayed controller start, force bounds, and force slew bounds checked.
- Synthetic calibration distinguishes the exact model from incorrect friction.
- Worker pause/stop, exact checkpoint recovery, validation improvement, and untouched plant parameters checked.
- DOM tests checked engineering forms, buttons, worker completion, model export, test locks, and the checks dashboard.
- Numerical and Monte Carlo outputs are in the `reports/` directory in this package.

Browser UI and canvas fallback were inspected in headless Chromium for the public release. This does not establish WebGL quality or performance on a physical GPU.
No real laboratory dataset was supplied. Experimental hardware calibration remains unverified.

## Source and rebuild

The src folder separates physics, experiments, application controls, monitors, and rendering.
To rebuild the standalone HTML after editing source, run:

    python build.py

The bundled Three.js 0.185.1 renderer uses the MIT license. See vendor/THREE-LICENSE.txt.
No external runtime scripts are fetched by the app.

Optional source tests need Node.js 22.22.2+ or 24.15+. Run `npm install`, then `npm test`.
Run `npm run validate` for the seeded Monte Carlo report and RK4 convergence check.
The DOM test is a source-level interface test. It is not a full browser or GPU test.

Run `npm run test:compat` to check the worker-blocked compatibility mode.
Run `npm run test:demo` to check the guided demonstration through the interface.
The guided demonstration is an optimization demonstration, not a claim of general robustness.
In the recorded 20-trial demo test, successful stabilization improved from 0/20 to 12/20.
The deliberately weak starting gain is stated in the preset. See demo-tests.json.

## Reproduce the swing-up references

The shipped HTML includes the references; Python optimization is not required to run it.
For regeneration, install CasADi, NumPy and SciPy, then run from the parent of `inertia`:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 inertia/tools/solve_swing.py 2 6
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 inertia/tools/solve_swing.py 3 7
python3 inertia/tools/export_swing.py 2 6
python3 inertia/tools/export_swing.py 3 7
python3 inertia/tools/install_references.py
python3 inertia/build.py
node inertia/tests/test-swing.cjs
node inertia/tests/validate-multi.cjs
```

Optimization: multiple shooting with RK4, IPOPT, bounded cart travel, actual force, command force,
force slew and velocity. Dense 10 ms references have a backward discrete Riccati tracking gain.
The runtime applies feedback through the same motor and physics integrator as manual control.
Method references: [MIT trajectory optimization](https://underactuated.mit.edu/trajopt.html)
and [CasADi documentation](https://web.casadi.org/docs/).
