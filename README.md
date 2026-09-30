# Factory Delivery AMR: AutoCAD, Fusion 360, URDF and ROS 2 guide

This guide is based on the local 28-page scanned PDF `Thiết kế Robot - C1-C3.pdf` (two slides per scanned page; slide numbers 1–56 are visible in this excerpt). The document is a **concept and systems-engineering study**, not a released manufacturing drawing or a complete robot specification. Keep the source requirements, chosen concepts and engineering assumptions separate throughout the project.

## 1. What the source does—and does not—specify

| Item | PDF evidence | How to use it |
|---|---|---|
| Mission | Slide 7: transport a parts tray from warehouse A to stations B–C–D, avoid people/obstacles, return to charging station. | Use as the top-level operational scenario. |
| Load | Slide 7 shows payload 20 kg; requirement table R01 on slide 34 says **payload >20 kg**. | Resolve the inconsistency with stakeholders. Do not design a 20 kg-only structure as compliant with R01. |
| Speed | At least 1.2 m/s (slides 7, 12, 18, 34). | Verify under the agreed loaded condition; detailed test procedure needed. |
| Aisle | Minimum aisle width 1.2 m (slides 7, 12, 18, 34). | Includes robot, load, localization uncertainty and safety clearance. The source gives no robot envelope. |
| Docking | Position error ≤ ±30 mm (slides 7, 12, 18, 34). | Define reference datum, orientation tolerance and success rate before testing. |
| Runtime | At least 4 hours (slides 7, 12, 18, 34). | Requires a duty-cycle/energy budget and loaded endurance test; not derivable from geometry alone. |
| Person detection | At least 3 m (slide 34, R06). | Detection is not equivalent to protective stopping distance or functional safety. Validate separately. |
| Other functions | Avoid moving obstacles; emergency stop; autonomous return to charge; MES/WMS connection (slides 7 and 34). | Allocate to safety, mission-management and integration work packages. |
| Mobility concept | Differential drive scored 4.70 vs mecanum 3.50, Ackermann 3.55 and swerve 2.85 (slide 50). | Preferred concept at this decision gate, not a finalized drivetrain. Mecanum may be reconsidered if lateral maneuverability becomes dominant. |
| Mechanical transfer | Slide 46 lists a fixed tray for the leading concept; slide 48 says to first choose the mechanism category. | Tray dimensions, docking interface, loading/unloading action and retention remain undecided. |
| Sensors/computing | Candidate 2D LiDAR/SLAM, depth camera, IMU, wheel encoder; SBC/Jetson with MCU; BLDC drive (slides 52–56). | Candidates only: exact parts, interfaces and split of responsibilities were not selected. |
| Control/software | Slide 56 suggests high-level SBC/Jetson, low-level MCU and motor driver; slide 55 lists SLAM, planning, obstacle avoidance and docking. | Treat as a proposed architecture to evaluate, not a fixed bill of materials. |

**Important requirement conflict:** the narrative says 20 kg while R01 says `>20 kg`. Use the stricter value only after the project owner defines the test load and margin. Do not silently pick one. The PDF supplies no chassis dimensions, wheel diameter/track, center of mass, battery capacity, motor torque, material/thickness, or CAD tolerances.

## 2. Establish a controlled design baseline

Before detailed CAD, create a requirements/traceability matrix (RTM) with at least: requirement ID, exact wording, source page, owner, operating conditions, verification method, acceptance threshold, linked CAD component/ROS frame, test evidence and status. The PDF recommends tracing need → system requirement → design element → test (slides 18 and 36–38).

Resolve these open questions at SRR/PDR before production-intent design:

1. Is R01 20 kg or strictly greater than 20 kg? What payload envelope and center-of-gravity range?
2. Does the 1.2 m aisle mean wall-to-wall clear width? What additional clearance is required for people, swept turns and localization error?
3. Is 1.2 m/s required loaded, unloaded, or both? What acceleration, braking distance, grade and floor condition?
4. How is ±30 mm docking measured, from which datum, at what approach speed, and with what repeatability/confidence?
5. What duty cycle and charge policy constitute 4 h runtime? Which battery chemistry, voltage and charging interface?
6. What is the load-transfer action (fixed tray, rollers, lift, conveyor), retention method and station interface?
7. What safety controller, E-stop circuit, scanner coverage, speed zones and risk-assessment process are required?
8. What MES/WMS message contract, network and failure behavior are required?

Document trade studies and assumptions in version control. The source calls for iterative design, test evidence, risk tracking and formal Go/Rework/Stop reviews (slides 14–25).

## 3. AutoCAD 2D drafting workflow

### 3.1 Drawing package

Create at least these model-space views at **1:1 in millimeters**:

1. **Plan view:** overall vehicle/load envelope, axle line, wheel outlines, sensor field-of-view placeholder, tray footprint, mounting/datums, aisle walls and turning/swept envelope.
2. **Side elevation:** floor datum, wheel radius, chassis/tray heights, sensor height, payload envelope and dock interface.
3. **Front elevation:** wheel track, total width, payload overhang, sensor placement and aisle-clearance dimensions.
4. **Interface/detail view:** station docking datums and load-transfer interface once chosen.

Do not turn the illustrative URDF dimensions into a production drawing. Use the PDF requirement table and identify all unknown dimensions as `TBD`/`CONCEPT`; replace each with approved mechanical design data before fabrication.

### 3.2 Recommended layers

| Layer | Contents | Example color / linetype |
|---|---|---|
| `OUTLINE` | Robot and payload visible edges | White/continuous |
| `HIDDEN` | Hidden/alternate geometry | Gray/hidden |
| `CENTER` | Axle, symmetry and datum axes | Green/center |
| `DIM` | Dimensions and leaders | Red/continuous |
| `SENSOR` | Sensor location, scan/FOV envelope | Cyan/continuous |
| `KEEP_OUT` | Safety/clearance and swept envelopes | Magenta/dashed |
| `ENVIRONMENT` | Aisle and station context | Gray/continuous |
| `CONSTRUCTION` | Temporary geometry; freeze before issue | Gray/dashed |
| `TITLE` | Notes, title block, revision and source references | White/continuous |

Use named dimension styles and annotative text; keep dimensions associative. Put actual geometry on model space, paper-space viewports on layouts, and set the plotted sheet scale intentionally. Add title, units, projection convention, scale, drawing number, revision, author/checker, status (`CONCEPT`/`NOT FOR MANUFACTURE`), source requirements and unresolved assumptions.

### 3.3 Order of work and checks

1. Set `UNITS` to Decimal / millimeters; use a consistent XY floor plane and a documented origin at the drive-axle midpoint. Keep front as +X, left as +Y.
2. Create layers, linetypes, dimension style, text style and title block before geometry.
3. Draw centerlines and datum origins first, then chassis/tray/payload envelopes, wheels and sensors. Use `RECTANG`, `CIRCLE`, `OFFSET`, `MIRROR`, `FILLET` only where design intent calls for it; constrain symmetric features using centerlines rather than independent eyeballing.
4. Add dimensions from datums, not chained dimensions. Show overall length/width, wheel track, wheel size, ground clearance, tray/load envelope, mounting coordinates and sensor heights as soon as those are released.
5. Add the 1.2 m aisle as an environment constraint, not as a robot dimension. Check static clearance and the swept path at turns; show the assumed payload and safety margins.
6. Add sensor FOV as a labeled *nominal visualization only* until sensor make/model and safety function are approved. A LiDAR drawing range does not prove R06 or a safe stopping distance.
7. `AUDIT`, `OVERKILL` (after review), `DIMREASSOCIATE` if needed, inspect `DIST`/`AREA`, verify units, check closed profiles, layer states, lineweights, external references and missing fonts.
8. Export DWG plus an exchange DXF only when needed; reopen the exported file and recheck dimensions/layers. Issue a PDF plot and record its revision alongside source DWG.

**Concept-only envelope in the example URDF** (not prescribed by the PDF): chassis 650 × 500 × 160 mm, wheel radius 80 mm, wheel track 560 mm, fixed tray 500 × 450 × 20 mm, approximate payload proxy 380 × 380 × 250 mm. If these numbers are reused to make a teaching drawing, mark it `ILLUSTRATIVE ONLY — NOT FOR MANUFACTURE` and replace them after packaging, load, stability and aisle checks.

## 4. Fusion 360 3D model workflow

### 4.1 Component structure and origins

Use a Fusion **component per rigid body/link**, not a single unstructured body. Suggested components: `base_link`, `left_wheel_link`, `right_wheel_link`, `transfer_tray`, `payload_proxy` (simulation only), `front_lidar_link`, and support-wheel/roller components. Apply rigid joints for fixed components and revolute joints for drive wheels. The support spheres in the ROS starter are only numerical placeholders; production modeling should use chosen swivel casters or engineered rollers.

Use millimeters in Fusion. Set the assembly origin at the drive-axle midpoint projected to the floor. Orient +X forward, +Y left and +Z up. Keep wheel axes along +Y. Place each component origin in the **link frame to be exported**, then assemble using explicit, measured transforms. The example ROS model uses a temporary 650 × 500 × 160 mm chassis centered at z=240 mm from the floor; tray center at z=360 mm and a 20 kg placeholder load. These are packaging assumptions only.

### 4.2 Parametric feature order

1. Create top-level user parameters for the approved envelope, wheel radius/width/track, chassis plate thickness, tray interface, sensor mounting coordinates, ground clearance and payload limits.
2. Sketch a fully constrained chassis plan; extrude the actual plate/frame structure rather than a solid block when detailed structural CAD begins. Add mounting patterns from shared datums.
3. Model wheels, hubs, gearbox/motor envelopes, battery/BMS, compute enclosure, E-stop, scanner and charging contacts as separate components. Use real catalog envelopes and reserve cable/maintenance clearances.
4. Add the tray/load-retention mechanism only after station interface and safety requirements are chosen.
5. Use joints with named datums and check interferences, wheel-ground contact, payload support, center of mass, fastener access and maintenance envelope. Simulate the loaded and unloaded configurations.
6. Run mass properties using actual assigned materials; record mass, center of gravity and principal inertias. Do not use the conceptual block inertia in place of a real BOM.
7. Save the native Fusion design and revisioned neutral exports. Preserve a link-to-component and frame-transform table for URDF work.

### 4.3 URDF mesh export rules

Export each link's visual mesh in that link's own coordinate frame, with consistent +X/+Y/+Z axes and millimeter-to-meter conversion documented. Prefer separate simplified collision meshes (or URDF primitives) over complex visual meshes. Avoid applying the same assembly transform both in the mesh and in `<joint><origin>`; this common double-transform error moves links twice. Keep mesh origins, units and handedness explicit. Re-import each exported mesh into a clean Fusion design and verify orientation, scale, hole/clearance and origin before authoring the URDF.

## 5. URDF structure and frame convention

The starter `src/factory_delivery_amr/urdf/factory_delivery_amr.urdf` includes a source/assumption ledger at the top. It uses:

```text
odom  --(Gazebo diff-drive plugin)-->  base_footprint
base_footprint --(fixed, z=0.24 m)--> base_link
base_link --(continuous, axis +Y)--> left_wheel_link / right_wheel_link
base_link --(fixed)--> transfer_tray, payload_proxy, front_lidar_link, supports
```

* URDF uses SI units: meters, kilograms, seconds, radians. Fusion dimensions in millimeters need a factor of 0.001 for translations and mesh scale.
* `base_footprint` is floor-level at the axle midpoint. `base_link` is at the chassis-envelope center; this keeps planar odometry separate from body height.
* Joint `<origin>` is expressed in the **parent link** frame. `<axis>` is in the joint frame. Wheel cylinder visuals are rotated so the cylinder axle lies on the +Y drive axis.
* Each physical link separates inertial, visual and collision geometry. The example's primitive inertias are computed from `Ibox = m/12 diag(y²+z², x²+z², x²+y²)`, the solid-cylinder axial/transverse formula, and `Isphere = 2/5 mr²`. They are valid only for the assumed masses, dimensions and COMs in the ledger.
* Differential-drive kinematics: `v = r(ωR+ωL)/2`, `ωz = r(ωR−ωL)/b`; invert to obtain wheel speeds. In the sample, `r=0.08 m`, `b=0.56 m`; max linear speed must be tested with the actual motors, load and floor.
* The payload proxy is fixed to the tray only to emulate a loaded case. It does not implement picking, release, load sensing or docking.

Never infer joint transforms, mesh units, joint signs, mass or center of gravity from a picture. Verify each transform against the Fusion assembly and a frame table. A structural URDF pass cannot prove the geometry is in the right place.

## 6. ROS 2 Humble + Gazebo Classic simulation

The package `factory_delivery_amr` is a **Gazebo Classic** example (ROS 2 Humble, Gazebo 11), not Gazebo Sim / Ignition. It simulates a 1.2 m clear aisle, two differential-drive wheels, a fixed LiDAR and one static obstacle. The Gazebo diff-drive plugin publishes `odom -> base_footprint`; `publish_wheel_tf` is disabled so `robot_state_publisher` is the single source for wheel and fixed-link transforms from `/joint_states`. The two nodes therefore both publish on `/tf`, but own different transforms. It is not a Nav2 navigation stack or a safety/person-detection demonstration.

### Build and launch

From the workspace root (the repository root):

```bash
source /opt/ros/humble/setup.bash
colcon build --packages-select factory_delivery_amr
source install/setup.bash
ros2 launch factory_delivery_amr simulation.launch.py
```

For a headless server, use `ros2 launch factory_delivery_amr simulation.launch.py gui:=false`. Gazebo Classic must be installed with the ROS plugins. The launch spawns the URDF, runs `robot_state_publisher`, publishes joint states, `/odom`, `/tf` and a simulated `/scan`.

In a second sourced terminal, inspect topics and command a short low-speed motion:

```bash
ros2 topic list
ros2 topic echo /scan --once
ros2 topic echo /odom --once
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 0.15}, angular: {z: 0.0}}'
```

Stop/inspect the robot in Gazebo; do not leave it moving unattended. Check that `odom -> base_footprint -> base_link`, wheel transforms and `front_lidar_link` exist and have the intended direction/height. The static box is an obstacle surrogate, not a person or a validated safety target.

### Navigation development (next step, not included in starter)

Add `slam_toolbox` for map creation or provide a known map/localization setup, then configure Nav2 with the actual footprint, inflation, speed/acceleration limits, LiDAR topic/frame, odometry and recovery behavior. Define station poses for A/B/C/D/charger, mission state transitions, MES/WMS adapter and explicit communication-loss behavior. Build docking with a local marker/reflector/camera strategy and test the source's ±30 mm acceptance across repeated trials. Use recorded bags and world/parameter revisions for repeatability.

Simulation cannot establish braking performance, people-detection distance, 4-hour runtime, load stability, functional safety, docking accuracy, hardware thermal margin or regulatory compliance. Those need physical measurement, a hazard analysis and appropriate safety review.

## 7. Verification and acceptance plan

| Requirement | Suggested verification | Record |
|---|---|---|
| R01 payload >20 kg vs 20 kg narrative | Approved specification; static/proof load test on qualified structure | Load, deflection, permanent set, pass/fail |
| R02 ≥1.2 m/s | Loaded speed test on representative level floor | Calibrated speed log, battery state, load, surface |
| R03 docking ≤±30 mm | Repeated docking trials; measure position error and define yaw criterion | Per-trial x/y error, orientation, success rate, approach direction |
| R04 runtime ≥4 h | Mission-profile endurance test | Runtime, SOC, voltage/current/power/temperature, payload and duty cycle |
| R05 1.2 m aisle | CAD envelope/swept path, then physical clearance test | Clear aisle width, turn path, clearance and localization state |
| R06 person detection ≥3 m | Sensor detection characterization and independent safety validation | Target, lighting, angle, reflectivity, missed/false detections; stop distance separately |
| R07 avoid moving obstacles | Scenario-based demonstration/test, including occlusion and failures | Scenario, speed, clearance, intervention and failure log |
| R08 E-stop | Inspection + demonstration for each operating mode; validate safe energy removal | Response time, stopping distance, reset/fault behavior |
| R09 autonomous return/charge | Mission test with low-battery and station fault cases | Docking success, charging confirmation, retries and exceptions |
| R10 MES/WMS | Interface test including delay, duplicate, disconnect and recovery | Messages, timing, state transitions, error handling |

Maintain evidence from unit tests through integration, loaded system test and final demonstration. Record the robot software/configuration, CAD drawing/model revision, test setup, calibrated instruments, raw data and pass/fail decision. Apply the PDF's Go/Rework/Stop design-review gates rather than treating a successful visualization as system verification.

## 8. Starter file map and status

* `README.md` — this technical workflow and requirements guide.
* `src/factory_delivery_amr/urdf/factory_delivery_amr.urdf` — assumption-led loaded AMR model and ledger.
* `src/factory_delivery_amr/worlds/factory_aisle.world` — 1.2 m aisle world with static obstacle.
* `src/factory_delivery_amr/launch/simulation.launch.py` — Gazebo Classic launch and robot spawn.
* `src/factory_delivery_amr/package.xml`, `CMakeLists.txt` — ROS package metadata and install rules.

No AutoCAD DWG/DXF or Fusion design is generated here: those proprietary authoring applications are not part of this ROS workspace, and the source PDF does not define a dimensioned manufacturing design. The 2D and 3D sections above are actionable drafting/modeling workflows, while all sample geometry remains explicitly provisional.