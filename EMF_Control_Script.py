import sys
import numpy as np
sys.path.append("/home/jacklin/EMF/emf")
from emf import Phase2D, EMFAnalysis2D

 # name, x, y, wire diameter, voltage, current, phase angle, # wires, spacing

V_PHASE = 76.2e3         # 76.2 kV phase-to-ground (from 132 kV L-L / sqrt(3))
I_PHASE = 320            # A 
H = 9.03                     # m height above ground
R_CONDUCTOR = 0.01575      # m (~31.5 mm diameter)
BUNDLE_COUNT = 2         # 2
BUNDLE_SPACING = 0.380     # 380mm separation

phases = [
    # name, x, y, wire diameter, voltage, current, phase angle, # wires, spacing
    # Circuit 1 (left)
    Phase2D("R1", -2.15, 24.40, R_CONDUCTOR, V_PHASE, I_PHASE,   0, BUNDLE_COUNT, BUNDLE_SPACING),
    Phase2D("W1",  -2.15, 21.44, R_CONDUCTOR, V_PHASE, I_PHASE, 120, BUNDLE_COUNT, BUNDLE_SPACING),
    Phase2D("B1",  -2.15, 18.48, R_CONDUCTOR, V_PHASE, I_PHASE, 240, BUNDLE_COUNT, BUNDLE_SPACING),

    # Circuit 2 (right)
    Phase2D("R2",   2.15, 18.48, R_CONDUCTOR, V_PHASE, I_PHASE,   0, BUNDLE_COUNT, BUNDLE_SPACING),
    Phase2D("W2",   2.15, 21.44, R_CONDUCTOR, V_PHASE, I_PHASE, 120, BUNDLE_COUNT, BUNDLE_SPACING),
    Phase2D("B2",  2.15,  24.40, R_CONDUCTOR, V_PHASE, I_PHASE, 240, BUNDLE_COUNT, BUNDLE_SPACING),
]
emf = EMFAnalysis2D(phases)

ax = emf.plot_geometry()
ax.figure.savefig("emf_geometry.png", dpi=200)

# Horizontal sample range and height
xs = np.linspace(-30, 30, 401)
ys = (1,)  # 1m

# === ELECTRIC FIELD ===
axE = emf.plot_elec_field_profiles(xs=xs, ys=ys)
axE.set_yscale("linear")  
lineE = axE.get_lines()[0]
xdataE, ydataE = lineE.get_xdata(), lineE.get_ydata()
Emax, xEmax = ydataE.max(), xdataE[ydataE.argmax()]

print(f"Maximum Electric Field at {ys[0]} m: {Emax:.2f} V/m at x = {xEmax:.2f} m")

# Formatting stuff - see official documentation
axE.set_title(f"E-field at {ys[0]} m (max ≈ {Emax:.2f} V/m)")
axE.axvline(xEmax, color="red", ls="--", alpha=0.6)
axE.text(xEmax, Emax, f"{Emax:.1f} V/m", color="red", ha="center", va="bottom")
axE.figure.savefig("E_profile_1m_with_max.png", dpi=220)
print("Saved: E_profile_1m_with_max.png")

# === MAGNETIC FIELD ===
axB = emf.plot_mag_field_profiles(xs=xs, ys=ys)
axB.set_yscale("linear")  
lineB = axB.get_lines()[0]
xdataB, ydataB = lineB.get_xdata(), lineB.get_ydata()
Bmax, xBmax = ydataB.max(), xdataB[ydataB.argmax()]

print(f"Maximum Magnetic Field at {ys[0]} m: {Bmax:.6f} T at x = {xBmax:.2f} m")

# Formatting stuff
axB.set_title(f"B-field at {ys[0]} m (max ≈ {Bmax:.6f} T)")
axB.axvline(xBmax, color="red", ls="--", alpha=0.6)
axB.text(xBmax, Bmax, f"{Bmax:.6e} T", color="red", ha="center", va="bottom")
axB.figure.savefig("B_profile_1m_with_max.png", dpi=220)
print("Saved: B_profile_1m_with_max.png")
