# Architecture

Inertia runs completely in the browser. No backend, account, external API or runtime package download is needed. The HTML build embeds the local copy of Three.js and the application scripts.

```text
index.html                 Built, self-contained browser demo
src/layout.html            UI structure
src/style.css              Dark engineering dashboard styles
src/core.js                Nonlinear plant, state, actuator, sensor and controllers
src/swing-data.js          Precomputed 2- and 3-link nominal references
src/optimizer.js           Trial evaluation, search, validation and calibration
src/app.js                 Application state and user interaction
src/display.js             Signal monitors and plotted metrics
src/presets.js             Laboratory and optimization presets
src/scene.js               Three.js scene and 2D canvas fallback
vendor/three.cjs           Offline Three.js distribution (MIT)
build.py                   Generates index.html from source + vendor
tests/                    Node.js numerical and DOM tests
reports/                  Recorded outcomes and reference test results
tools/                    Optional Python swing-up reference regeneration
```

## Model

The physical model uses a coupled mass matrix for the cart and one to three serial rigid links. State integration uses RK4 with a nominal 1 ms step and 0.5 ms precision presets. The model includes gravity, bearing friction, viscous losses, motor lag, slew limits, saturation, simplified sensor errors, and discrete rail-contact impulses.

Control options include LQR, PID and Sugeno fuzzy feedback. Two- and three-link default swing-up presets use pre-optimized force references with time-varying LQR tracking, then stationary balancing. References are commands and feedback targets; they do not replace the simulated state.

## Developer workflow

Edit the `src/` files, then run `python build.py`. Track both source changes and the newly generated `index.html` in the same commit. The Pages workflow rebuilds the HTML and publishes only the standalone file.

The `tests/` scripts produce JSON outputs in `reports/`. Those outputs are test results; they are not embedded training labels, authenticated hardware readings, or scientific measurements.
