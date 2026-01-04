# Content for Civil Engineering GATE Bot
# Organized by topic with difficulty levels

# Topic codes:
# SM - Soil Mechanics, FM - Fluid Mechanics, SA - Structural Analysis
# RCC - Reinforced Concrete, STEEL - Steel Structures, GEO - Geomatics
# ENV - Environmental Engineering, TRANS - Transportation, HYDRO - Hydrology
# CONST - Construction Management

QUESTIONS = [
    # Soil Mechanics
    {
        "question": "In a consolidation test, if the drainage path for double drainage is 'd', what is the thickness of the clay layer?",
        "options": ["A) d", "B) 2d", "C) d/2", "D) 4d"],
        "answer": "B",
        "topic": "SM",
        "difficulty": "medium"
    },
    {
        "question": "Quick sand condition occurs when:",
        "options": ["A) Upward hydraulic gradient equals critical gradient", "B) Downward hydraulic gradient equals critical gradient", "C) Void ratio becomes zero", "D) Water table is at ground level"],
        "answer": "A",
        "topic": "SM",
        "difficulty": "medium"
    },
    {
        "question": "The coefficient of earth pressure at rest (K₀) for normally consolidated clay is typically:",
        "options": ["A) Equal to 1", "B) Greater than 1", "C) Less than 1", "D) Equal to Rankine's active pressure coefficient"],
        "answer": "C",
        "topic": "SM",
        "difficulty": "easy"
    },
    {
        "question": "Sensitivity of clay is defined as the ratio of:",
        "options": ["A) Undisturbed to remoulded shear strength", "B) Remoulded to undisturbed shear strength", "C) Liquid limit to plastic limit", "D) Cohesion to angle of friction"],
        "answer": "A",
        "topic": "SM",
        "difficulty": "easy"
    },
    {
        "question": "In a triaxial UU test on saturated clay, the angle of internal friction (φ) is:",
        "options": ["A) Maximum", "B) Minimum but not zero", "C) Zero", "D) Equal to drained angle"],
        "answer": "C",
        "topic": "SM",
        "difficulty": "hard"
    },
    
    # Fluid Mechanics
    {
        "question": "Which of the following fluids exhibits a linear relationship between shear stress and rate of shear strain?",
        "options": ["A) Dilatant fluid", "B) Bingham plastic", "C) Newtonian fluid", "D) Pseudoplastic fluid"],
        "answer": "C",
        "topic": "FM",
        "difficulty": "easy"
    },
    {
        "question": "The ratio of inertia force to viscous force is known as:",
        "options": ["A) Froude Number", "B) Reynolds Number", "C) Mach Number", "D) Weber Number"],
        "answer": "B",
        "topic": "FM",
        "difficulty": "easy"
    },
    {
        "question": "For a hydraulic jump in a rectangular channel, the energy loss is maximum when the Froude number is:",
        "options": ["A) Very low (< 1.7)", "B) Between 2.5 and 4.5", "C) Very high (> 9)", "D) Equal to 1"],
        "answer": "C",
        "topic": "FM",
        "difficulty": "hard"
    },
    {
        "question": "The velocity distribution in a pipe flow is parabolic for:",
        "options": ["A) Turbulent flow only", "B) Laminar flow only", "C) Both laminar and turbulent", "D) Transition flow"],
        "answer": "B",
        "topic": "FM",
        "difficulty": "medium"
    },
    {
        "question": "Euler's equation of motion represents:",
        "options": ["A) Conservation of mass", "B) Conservation of momentum", "C) Conservation of energy", "D) Continuity"],
        "answer": "B",
        "topic": "FM",
        "difficulty": "medium"
    },
    
    # Structural Analysis
    {
        "question": "The Maximum Bending Moment in a simply supported beam of span L carrying a uniformly distributed load 'w' per unit length is:",
        "options": ["A) wL²/8", "B) wL²/4", "C) wL/2", "D) wL²/12"],
        "answer": "A",
        "topic": "SA",
        "difficulty": "easy"
    },
    {
        "question": "The Point of Contraflexure is the point where:",
        "options": ["A) Shear force is zero", "B) Bending moment is maximum", "C) Bending moment changes sign", "D) Shear force is maximum"],
        "answer": "C",
        "topic": "SA",
        "difficulty": "easy"
    },
    {
        "question": "For a statically determinate structure, the degree of static indeterminacy is:",
        "options": ["A) Greater than zero", "B) Less than zero", "C) Equal to zero", "D) Equal to number of reactions"],
        "answer": "C",
        "topic": "SA",
        "difficulty": "easy"
    },
    {
        "question": "The influence line for reaction at a simply supported beam is:",
        "options": ["A) Parabolic", "B) Linear (triangular)", "C) Constant", "D) Hyperbolic"],
        "answer": "B",
        "topic": "SA",
        "difficulty": "medium"
    },
    {
        "question": "In the moment distribution method, the carry-over factor for a prismatic member with far end fixed is:",
        "options": ["A) 1", "B) 1/2", "C) 1/3", "D) 2/3"],
        "answer": "B",
        "topic": "SA",
        "difficulty": "medium"
    },
    
    # RCC Design
    {
        "question": "As per IS 456:2000, the minimum grade of concrete for reinforced concrete work in 'Severe' exposure condition is:",
        "options": ["A) M20", "B) M25", "C) M30", "D) M35"],
        "answer": "C",
        "topic": "RCC",
        "difficulty": "medium"
    },
    {
        "question": "The modular ratio for M25 grade concrete as per IS 456 is approximately:",
        "options": ["A) 7", "B) 9", "C) 11", "D) 13"],
        "answer": "C",
        "topic": "RCC",
        "difficulty": "medium"
    },
    {
        "question": "As per IS 456, the minimum percentage of steel in a RCC column is:",
        "options": ["A) 0.4%", "B) 0.8%", "C) 1.0%", "D) 1.5%"],
        "answer": "B",
        "topic": "RCC",
        "difficulty": "easy"
    },
    {
        "question": "Development length in tension is increased by what factor for bars in compression?",
        "options": ["A) No change", "B) Reduced by 20%", "C) Increased by 25%", "D) Reduced by 25%"],
        "answer": "D",
        "topic": "RCC",
        "difficulty": "hard"
    },
    {
        "question": "The neutral axis depth factor (xu/d) for a balanced section of Fe500 steel is approximately:",
        "options": ["A) 0.53", "B) 0.48", "C) 0.46", "D) 0.42"],
        "answer": "C",
        "topic": "RCC",
        "difficulty": "hard"
    },
    
    # Steel Structures
    {
        "question": "The slenderness ratio of a compression member is the ratio of:",
        "options": ["A) Effective length to radius of gyration", "B) Actual length to depth", "C) Effective length to moment of inertia", "D) Depth to thickness"],
        "answer": "A",
        "topic": "STEEL",
        "difficulty": "easy"
    },
    {
        "question": "As per IS 800:2007, the maximum slenderness ratio for a compression member in a building is:",
        "options": ["A) 120", "B) 150", "C) 180", "D) 200"],
        "answer": "C",
        "topic": "STEEL",
        "difficulty": "medium"
    },
    {
        "question": "In a fillet weld, the effective throat thickness is taken as:",
        "options": ["A) 0.5 × leg size", "B) 0.707 × leg size", "C) leg size", "D) 0.6 × leg size"],
        "answer": "B",
        "topic": "STEEL",
        "difficulty": "medium"
    },
    {
        "question": "The mode of failure in short columns is typically:",
        "options": ["A) Buckling", "B) Crushing", "C) Local buckling", "D) Lateral torsional buckling"],
        "answer": "B",
        "topic": "STEEL",
        "difficulty": "easy"
    },
    {
        "question": "Gusset plates are used in truss connections to:",
        "options": ["A) Reduce weight", "B) Transfer loads between members", "C) Increase stiffness only", "D) Prevent corrosion"],
        "answer": "B",
        "topic": "STEEL",
        "difficulty": "easy"
    },
    
    # Environmental Engineering
    {
        "question": "BOD (Biochemical Oxygen Demand) is a measure of:",
        "options": ["A) Dissolved oxygen in water", "B) Oxygen required to decompose organic matter", "C) Total suspended solids", "D) Alkalinity of water"],
        "answer": "B",
        "topic": "ENV",
        "difficulty": "easy"
    },
    {
        "question": "The detention time in a primary sedimentation tank is typically:",
        "options": ["A) 30 minutes", "B) 1-2 hours", "C) 4-6 hours", "D) 12-24 hours"],
        "answer": "B",
        "topic": "ENV",
        "difficulty": "medium"
    },
    {
        "question": "Chlorine dosage in water treatment is typically expressed as:",
        "options": ["A) mg/L", "B) percentage", "C) kg/m³", "D) ppm/hour"],
        "answer": "A",
        "topic": "ENV",
        "difficulty": "easy"
    },
    {
        "question": "The standard 5-day BOD at 20°C is approximately what percentage of ultimate BOD?",
        "options": ["A) 50%", "B) 68%", "C) 80%", "D) 95%"],
        "answer": "B",
        "topic": "ENV",
        "difficulty": "hard"
    },
    {
        "question": "In an activated sludge process, F/M ratio typically ranges from:",
        "options": ["A) 0.05-0.15", "B) 0.2-0.5", "C) 0.6-1.0", "D) 1.5-2.0"],
        "answer": "B",
        "topic": "ENV",
        "difficulty": "hard"
    },
    
    # Transportation Engineering
    {
        "question": "The stopping sight distance depends on:",
        "options": ["A) Only reaction time", "B) Only braking distance", "C) Reaction time and braking distance", "D) Only design speed"],
        "answer": "C",
        "topic": "TRANS",
        "difficulty": "easy"
    },
    {
        "question": "The ruling minimum radius of horizontal curve for a design speed of 80 kmph (e=0.07, f=0.15) is approximately:",
        "options": ["A) 150 m", "B) 230 m", "C) 320 m", "D) 420 m"],
        "answer": "B",
        "topic": "TRANS",
        "difficulty": "hard"
    },
    {
        "question": "CBR value is used for designing:",
        "options": ["A) Concrete pavement only", "B) Flexible pavement", "C) Bridge foundations", "D) Retaining walls"],
        "answer": "B",
        "topic": "TRANS",
        "difficulty": "easy"
    },
    {
        "question": "The recommended coefficient of friction for design of horizontal curves as per IRC is:",
        "options": ["A) 0.10-0.12", "B) 0.15-0.18", "C) 0.25-0.30", "D) 0.35-0.40"],
        "answer": "B",
        "topic": "TRANS",
        "difficulty": "medium"
    },
    {
        "question": "As per IRC, the minimum width of a single lane in hilly terrain is:",
        "options": ["A) 2.5 m", "B) 3.0 m", "C) 3.5 m", "D) 3.75 m"],
        "answer": "C",
        "topic": "TRANS",
        "difficulty": "medium"
    },
    
    # Hydrology
    {
        "question": "The unit hydrograph theory assumes:",
        "options": ["A) Variable base time", "B) Constant rainfall intensity", "C) Linearity and time invariance", "D) Non-uniform rainfall distribution"],
        "answer": "C",
        "topic": "HYDRO",
        "difficulty": "medium"
    },
    {
        "question": "The Rational Formula Q = CIA is used to estimate:",
        "options": ["A) Total runoff volume", "B) Peak discharge", "C) Base flow", "D) Infiltration rate"],
        "answer": "B",
        "topic": "HYDRO",
        "difficulty": "easy"
    },
    {
        "question": "Evapotranspiration is the sum of:",
        "options": ["A) Evaporation and precipitation", "B) Evaporation and transpiration", "C) Runoff and infiltration", "D) Precipitation and interception"],
        "answer": "B",
        "topic": "HYDRO",
        "difficulty": "easy"
    },
    {
        "question": "The S-curve in hydrology is used to derive:",
        "options": ["A) Unit hydrograph of different duration", "B) Flood frequency curve", "C) Mass curve", "D) Rating curve"],
        "answer": "A",
        "topic": "HYDRO",
        "difficulty": "hard"
    },
    {
        "question": "Khosla's theory is used for design of:",
        "options": ["A) Earthen dams", "B) Weirs on permeable foundation", "C) Spillways", "D) Canal lining"],
        "answer": "B",
        "topic": "HYDRO",
        "difficulty": "medium"
    },
    
    # Geomatics / Surveying
    {
        "question": "In a closed traverse, the sum of interior angles should be equal to:",
        "options": ["A) (2n+4) × 90°", "B) (2n-4) × 90°", "C) n × 180°", "D) (n-2) × 180°"],
        "answer": "B",
        "topic": "GEO",
        "difficulty": "medium"
    },
    {
        "question": "The curvature correction in leveling is:",
        "options": ["A) Always added", "B) Always subtracted", "C) Added for staff reading", "D) Depends on refraction"],
        "answer": "B",
        "topic": "GEO",
        "difficulty": "medium"
    },
    {
        "question": "Contour lines that cross a valley form:",
        "options": ["A) V-shape pointing uphill", "B) V-shape pointing downhill", "C) U-shape", "D) Parallel lines"],
        "answer": "A",
        "topic": "GEO",
        "difficulty": "easy"
    },
    {
        "question": "The principle of EDM (Electronic Distance Measurement) is based on:",
        "options": ["A) Triangulation", "B) Electromagnetic wave propagation", "C) Mechanical measurement", "D) Optical refraction"],
        "answer": "B",
        "topic": "GEO",
        "difficulty": "easy"
    },
    {
        "question": "GPS positioning requires a minimum of how many satellites for 3D position fix?",
        "options": ["A) 2", "B) 3", "C) 4", "D) 6"],
        "answer": "C",
        "topic": "GEO",
        "difficulty": "medium"
    },
    
    # Construction Management
    {
        "question": "In CPM, the critical path is the path with:",
        "options": ["A) Shortest duration", "B) Longest duration", "C) Maximum float", "D) Minimum activities"],
        "answer": "B",
        "topic": "CONST",
        "difficulty": "easy"
    },
    {
        "question": "PERT uses which probability distribution for activity duration?",
        "options": ["A) Normal", "B) Uniform", "C) Beta", "D) Exponential"],
        "answer": "C",
        "topic": "CONST",
        "difficulty": "medium"
    },
    {
        "question": "The expected time in PERT is calculated as:",
        "options": ["A) (a + 4m + b)/6", "B) (a + m + b)/3", "C) (a + 2m + b)/4", "D) (a + b)/2"],
        "answer": "A",
        "topic": "CONST",
        "difficulty": "easy"
    },
    {
        "question": "Free float of an activity is the:",
        "options": ["A) Total float minus head event slack", "B) Difference between total float and interfering float", "C) Always equal to total float", "D) Always zero on critical path"],
        "answer": "B",
        "topic": "CONST",
        "difficulty": "hard"
    },
    {
        "question": "The term 'Crashing' in project management refers to:",
        "options": ["A) Project failure", "B) Reducing project duration by adding resources", "C) Cost overrun", "D) Activity overlap"],
        "answer": "B",
        "topic": "CONST",
        "difficulty": "medium"
    }
]

FACTS = [
    # Soil Mechanics
    "The slenderness ratio of a column is defined as the ratio of its effective length to its least radius of gyration.",
    "In a soil sample, if the void ratio is 'e', the porosity 'n' is given by n = e / (1 + e).",
    "Quick sand condition occurs when the effective stress in the soil becomes zero due to upward seepage pressure.",
    "For a logically determinate truss with 'm' members and 'j' joints, the condition for stability is m = 2j - 3.",
    "The critical hydraulic gradient for quick sand condition is approximately 1.0 for most soils.",
    "Sensitivity of clay ranges from 1 (insensitive) to over 16 (extra-sensitive/quick clays).",
    
    # Fluid Mechanics
    "Bernoulli's equation is based on the principle of conservation of energy.",
    "The Point of Contraflexure is the point where the Bending Moment changes its sign.",
    "Reynolds number less than 2000 indicates laminar flow in pipes.",
    "Froude number is the ratio of inertia force to gravity force and is critical in open channel flow.",
    "Chezy's formula for open channel flow is V = C√(RS), where R is hydraulic radius and S is bed slope.",
    
    # RCC Design
    "As per IS 456:2000, minimum cover for RCC in moderate exposure is 30mm.",
    "The partial safety factor for concrete (γc) in limit state design is 1.5.",
    "The partial safety factor for steel (γs) in limit state design is 1.15.",
    "Maximum water-cement ratio for severe exposure condition is 0.45 as per IS 456.",
    "Minimum cement content for M30 concrete in severe exposure is 320 kg/m³.",
    
    # Steel Structures
    "As per IS 800:2007, yield stress of Fe410 grade steel is 250 MPa.",
    "The effective throat thickness of a fillet weld is 0.707 times the leg size.",
    "High Strength Friction Grip (HSFG) bolts resist loads through friction.",
    "Minimum pitch of rivets/bolts should not be less than 2.5 times the nominal diameter.",
    
    # Environmental Engineering
    "BOD (Biochemical Oxygen Demand) is a measure of the amount of oxygen required by aerobic microorganisms to decompose organic matter.",
    "The standard BOD test is conducted for 5 days at 20°C.",
    "Coagulation removes colloidal particles by destabilizing their electric charge.",
    "Breakpoint chlorination is the point where free chlorine residual starts appearing.",
    
    # Transportation
    "IRC specifies design speed of 120 kmph for expressways in plain terrain.",
    "The sight distance on horizontal curves is measured along the center line of the inner lane.",
    "Superelevation helps counteract centrifugal force on horizontal curves.",
    
    # General
    "Euler's buckling load formula: Pcr = π²EI/(Le)², where Le is the effective length.",
    "The modulus of elasticity of concrete can be estimated as 5000√fck MPa.",
    "Coefficient of variation is the ratio of standard deviation to mean, expressed as percentage."
]

FORMULAS = [
    # Fluid Mechanics
    {
        "title": "Reynolds Number (Re)",
        "formula": "Re = (ρ × v × D) / μ = (v × D) / ν",
        "explanation": "ρ=density, v=velocity, D=characteristic length, μ=dynamic viscosity, ν=kinematic viscosity. Re < 2000 → Laminar, Re > 4000 → Turbulent.",
        "topic": "FM"
    },
    {
        "title": "Bernoulli's Equation",
        "formula": "P₁/ρg + v₁²/2g + z₁ = P₂/ρg + v₂²/2g + z₂",
        "explanation": "P=pressure, v=velocity, z=elevation. Applicable for steady, incompressible, frictionless flow along a streamline.",
        "topic": "FM"
    },
    {
        "title": "Darcy-Weisbach Equation",
        "formula": "hf = f × (L/D) × (v²/2g)",
        "explanation": "hf=head loss, f=friction factor, L=pipe length, D=diameter. For laminar flow: f = 64/Re.",
        "topic": "FM"
    },
    
    # Soil Mechanics
    {
        "title": "Darcy's Law (Groundwater Flow)",
        "formula": "q = k × i × A",
        "explanation": "q=discharge, k=permeability coefficient, i=hydraulic gradient (h/L), A=cross-sectional area.",
        "topic": "SM"
    },
    {
        "title": "Void Ratio & Porosity Relationship",
        "formula": "e = n/(1-n)  and  n = e/(1+e)",
        "explanation": "e=void ratio, n=porosity. Also: Se = wG (Saturation × Void Ratio = Water Content × Specific Gravity).",
        "topic": "SM"
    },
    {
        "title": "Terzaghi's Bearing Capacity",
        "formula": "qu = cNc + γDfNq + 0.5γBNγ",
        "explanation": "qu=ultimate bearing capacity, c=cohesion, γ=unit weight, Df=depth of foundation, B=width. Nc, Nq, Nγ are bearing capacity factors.",
        "topic": "SM"
    },
    {
        "title": "Coefficient of Consolidation",
        "formula": "cv = Tv × H²/t",
        "explanation": "cv=coefficient of consolidation, Tv=time factor, H=drainage path length, t=time. For 50% consolidation, Tv ≈ 0.197.",
        "topic": "SM"
    },
    
    # Structural Analysis
    {
        "title": "Bending Equation",
        "formula": "M/I = σ/y = E/R",
        "explanation": "M=Bending Moment, I=Moment of Inertia, σ=Bending Stress, y=Distance from Neutral Axis, E=Young's Modulus, R=Radius of Curvature.",
        "topic": "SA"
    },
    {
        "title": "Euler's Buckling Load",
        "formula": "Pcr = π²EI/(Le)²",
        "explanation": "Critical load for a column. Le=effective length. For pinned-pinned: Le=L, Fixed-fixed: Le=0.5L, Fixed-free: Le=2L.",
        "topic": "SA"
    },
    {
        "title": "Moment Distribution - Distribution Factor",
        "formula": "DF = K/(ΣK) where K = I/L",
        "explanation": "K=stiffness, I=moment of inertia, L=length. For fixed far end, K=4EI/L. For hinged far end, K=3EI/L.",
        "topic": "SA"
    },
    
    # RCC Design
    {
        "title": "Ultimate Moment of Resistance (Rectangular Beam)",
        "formula": "Mu = 0.87fy × Ast × d × (1 - Ast×fy/(bd×fck))",
        "explanation": "Mu=ultimate moment, fy=steel yield strength, Ast=steel area, d=effective depth, b=width, fck=concrete characteristic strength.",
        "topic": "RCC"
    },
    {
        "title": "Development Length",
        "formula": "Ld = (φ × σs)/(4 × τbd)",
        "explanation": "Ld=development length, φ=bar diameter, σs=stress in steel, τbd=design bond stress. As per IS 456: Ld = φ×0.87fy/(4×τbd).",
        "topic": "RCC"
    },
    {
        "title": "Shear Strength of Concrete",
        "formula": "τc = 0.85√(0.8fck)(√(1+5β)-1)/(6β), β = 0.8fck/6.89Pt",
        "explanation": "τc=design shear strength, Pt=percentage of tension reinforcement. Simplified tables are provided in IS 456 Table 19.",
        "topic": "RCC"
    },
    
    # Steel Structures
    {
        "title": "Weld Strength (Fillet Weld)",
        "formula": "Strength = 0.707 × s × L × (fy/√3)/γmw",
        "explanation": "s=leg size, L=effective length, fy=yield stress, γmw=partial safety factor (1.25 for shop, 1.50 for site welds).",
        "topic": "STEEL"
    },
    {
        "title": "Bolt Shear Capacity",
        "formula": "Vdsb = (fub × Anb × nn + fub × Asb × ns)/(√3 × γmb)",
        "explanation": "fub=ultimate tensile strength, Anb=net shear area, Asb=shank area, nn, ns=number of shear planes, γmb=1.25.",
        "topic": "STEEL"
    },
    
    # Transportation
    {
        "title": "Stopping Sight Distance",
        "formula": "SSD = 0.278Vt + V²/(254f)",
        "explanation": "V=speed (kmph), t=reaction time (2.5s), f=longitudinal friction (0.35-0.40). First term is reaction distance, second is braking distance.",
        "topic": "TRANS"
    },
    {
        "title": "Superelevation",
        "formula": "e + f = V²/(127R)",
        "explanation": "e=superelevation (max 0.07), f=coefficient of friction (0.15), V=speed (kmph), R=radius (m).",
        "topic": "TRANS"
    },
    
    # Hydrology
    {
        "title": "Rational Formula",
        "formula": "Q = CIA/360",
        "explanation": "Q=peak discharge (m³/s), C=runoff coefficient (0-1), I=rainfall intensity (mm/hr), A=catchment area (hectares).",
        "topic": "HYDRO"
    },
    {
        "title": "Manning's Equation",
        "formula": "V = (1/n) × R^(2/3) × S^(1/2)",
        "explanation": "V=velocity (m/s), n=Manning's roughness coefficient, R=hydraulic radius (A/P), S=bed slope.",
        "topic": "HYDRO"
    },
    
    # Environmental Engineering
    {
        "title": "BOD First Order Kinetics",
        "formula": "BODt = BODu(1 - e^(-kt))",
        "explanation": "BODt=BOD at time t, BODu=ultimate BOD, k=rate constant (0.23/day at 20°C). BOD5 ≈ 0.68 × BODu.",
        "topic": "ENV"
    },
    {
        "title": "Hydraulic Loading Rate",
        "formula": "HLR = Q/A (m³/m²/day)",
        "explanation": "Q=flow rate, A=surface area. Typical values: Primary settling tank: 25-50 m³/m²/day, Secondary: 15-30 m³/m²/day.",
        "topic": "ENV"
    }
]

# Motivational messages for daily posts
MOTIVATIONAL_MESSAGES = [
    "🎯 Consistency beats intensity. Keep solving daily!",
    "💪 GATE 2025 is your year. Believe in yourself!",
    "📖 One formula a day keeps panic away!",
    "🏆 Every expert was once a beginner. Keep going!",
    "⏰ Time invested in preparation is never wasted.",
    "🧠 Understanding concepts > Memorizing solutions",
    "📊 Track your progress - what gets measured gets improved!",
    "🔥 Your competition is yourself from yesterday.",
    "💡 Smart work + Hard work = Success in GATE",
    "🎓 Dream big, work hard, stay focused!"
]

# Study tips
STUDY_TIPS = [
    "📚 Revise formulas before sleeping - memory consolidation happens during sleep!",
    "✍️ Practice numerical problems daily - GATE has about 55% numerical questions.",
    "📝 Make short notes for quick revision during the last month.",
    "⏱️ Practice with a timer - time management is crucial in GATE.",
    "🔄 Revisit wrong answers after a week to reinforce learning.",
    "📊 Analyze your mock tests - focus on weak areas, not just score.",
    "☕ Take regular breaks - 25 min study + 5 min break (Pomodoro technique).",
    "📖 Read NPTEL lectures for conceptual clarity.",
    "🧪 Attempt previous year questions topic-wise first, then mixed.",
    "💤 Get 7-8 hours of sleep before the exam - rest is crucial!"
]

# Beginner Exercise Tips with Images (from free-exercise-db)
EXERCISE_TIPS = [
    {"name": "🧘 Stretching", "desc": "Try 5 minutes of gentle stretching for every 2 hours of sitting.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/seated_calf_stretch/0.jpg"},
    {"name": "🚶 Walking", "desc": "A 10-minute walk after lunch aids digestion and clears your mind.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/walking_treadmill/0.jpg"},
    {"name": "💪 Wall Push-ups", "desc": "Do 10 wall push-ups during your study breaks to get the blood flowing.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/push-up_wall/0.jpg"},
    {"name": "🙆 Posture Reset", "desc": "Stand up and reach for the ceiling. Hold for 15 seconds to realign your spine.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/standing_reach/0.jpg"},
    {"name": "🦶 Ankle Rotations", "desc": "Rotate your ankles 10 times in both directions while sitting to improve circulation.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/ankle_circles/0.jpg"},
    {"name": "🦵 Squats", "desc": "Do 10 bodyweight squats to strengthen your legs and boost energy.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/squat/0.jpg"},
    {"name": "🤸 Lunges", "desc": "Try 5 lunges per leg to stretch your hip flexors and improve balance.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/lunge/0.jpg"},
    {"name": "💆 Neck Rolls", "desc": "Gently roll your neck in circles to relieve tension from reading.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/neck_circles/0.jpg"},
    {"name": "🏋️ Shoulder Shrugs", "desc": "Lift shoulders to ears, hold 5 seconds, release. Repeat 10 times.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/shoulder_shrug/0.jpg"},
    {"name": "🧎 Plank Hold", "desc": "Hold a plank for 20-30 seconds to build core strength.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/plank/0.jpg"},
    {"name": "🦋 Butterfly Stretch", "desc": "Sit with feet together, knees out. Gently press knees down for hip stretch.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/butterfly_stretch/0.jpg"},
    {"name": "🙏 Wrist Circles", "desc": "Rotate your wrists 10 times each direction to prevent strain from writing.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/wrist_circles/0.jpg"},
    {"name": "🦵 Calf Raises", "desc": "Stand on your toes, lower slowly. Do 15 reps to improve blood flow.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/calf_raise/0.jpg"},
    {"name": "🔄 Torso Twist", "desc": "Sit upright, twist left and right slowly. Great for spine mobility.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/seated_twist/0.jpg"},
    {"name": "👐 Chest Opener", "desc": "Clasp hands behind back, pull shoulders back. Hold 15 seconds.", "image": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/chest_stretch/0.jpg"}
]

# Beginner Hygiene Tips
HYGIENE_TIPS = [
    {"name": "🚿 Shower", "desc": "A quick morning shower can wake up your brain better than coffee!"},
    {"name": "🪥 Dental", "desc": "Oral hygiene is linked to focus. Don't skip brushing even during late grinds."},
    {"name": "🧼 Sanitize", "desc": "Wash your hands regularly, especially after using shared library desks."},
    {"name": "👕 Freshness", "desc": "Change into fresh clothes before starting a long study session to feel 'reset'."},
    {"name": "🛏️ Room", "desc": "Spend 2 minutes tidying your desk. A clean space reduces mental clutter."}
]

# Beginner General Health Tips
GENERAL_HEALTH_TIPS = [
    {"name": "💧 Hydration", "desc": "Stay hydrated! Keep a water bottle on your desk to avoid brain fog."},
    {"name": "🍎 Nutrition", "desc": "Swap one junk snack for a fruit. Better nutrition = better retention."},
    {"name": "👀 Eyes", "desc": "20-20-20 Rule: Every 20 mins, look 20 feet away for 20 seconds."},
    {"name": "👂 Focus", "desc": "Keep your phone in another room or on 'Do Not Disturb' to lower stress levels."},
    {"name": "🍌 Energy", "desc": "Eat a banana or some nuts for sustained energy instead of sugary energy drinks."}
]

# Beginner Language Learning Fallbacks (Chinese, Marathi, Telugu, Japanese)
LANGUAGE_FALLBACKS = [
    {
        "language": "Japanese",
        "word": "こんにちは (Konnichiwa)",
        "phonetic": "Kon-ni-chi-wa",
        "meaning": "Hello / Good Afternoon",
        "usage": "Use this to greet anyone during the day.",
        "tip": "In Japan, a small bow usually accompanies this greeting."
    },
    {
        "language": "Chinese",
        "word": "你好 (Nǐ hǎo)",
        "phonetic": "Nee-how",
        "meaning": "Hello",
        "usage": "The most common greeting in China.",
        "tip": "Nǐ means 'you' and hǎo means 'good'."
    },
    {
        "language": "Marathi",
        "word": "नमस्कार (Namaskar)",
        "phonetic": "Na-mas-kar",
        "meaning": "Hello / Respectful Greeting",
        "usage": "Standard polite greeting in Maharashtra.",
        "tip": "It is used regardless of the time of day."
    },
    {
        "language": "Telugu",
        "word": "నమస్కారం (Namaskaram)",
        "phonetic": "Na-mas-ka-ram",
        "meaning": "Hello / Respectful Greeting",
        "usage": "Formal greeting in Andhra Pradesh and Telangana.",
        "tip": "Adding 'andi' at the end makes it even more polite (Namaskaram andi)."
    }
]

# Interview Tips for Govt Jobs
INTERVIEW_TIPS = [
    {"name": "📋 Research the Organization", "desc": "Know the department's history, recent achievements, and current projects. Interviewers love candidates who show genuine interest."},
    {"name": "👔 Dress Professionally", "desc": "For govt interviews, wear formal attire. Men: light shirt, dark trousers, tie. Women: saree or formal suit."},
    {"name": "⏰ Arrive Early", "desc": "Reach the venue 30 minutes before your slot. Carry all original documents in a neat folder."},
    {"name": "🗣️ Speak Clearly", "desc": "Use simple, clear language. Avoid jargon. If you don't know something, say 'I don't know' honestly."},
    {"name": "🎯 Know Current Affairs", "desc": "Read newspapers daily for 2 weeks before the interview. Focus on govt schemes, budget, and national events."},
    {"name": "📝 Prepare Your DAF", "desc": "For UPSC, know every detail of your Detailed Application Form. They WILL ask about hobbies and hometown."},
    {"name": "🧘 Stay Calm", "desc": "Take a deep breath before answering. It's okay to pause for 2-3 seconds to gather your thoughts."},
    {"name": "🤝 Body Language", "desc": "Maintain eye contact, sit upright, and keep hands visible on the table. Don't fidget or cross arms."},
    {"name": "💡 Give Examples", "desc": "Support your answers with real-life examples or experiences. 'In my college project, I learned...'"},
    {"name": "🙏 Be Humble", "desc": "Show respect to the panel. Don't argue. Accept feedback gracefully even if you disagree."},
    {"name": "📚 Know Your Subject", "desc": "Expect technical questions from your graduation subject. Revise basics thoroughly."},
    {"name": "🌍 Know India", "desc": "Geography, constitution, economy basics are must. Know your state's CM, Governor, and key facts."},
    {"name": "❓ Prepare for 'Tell Me About Yourself'", "desc": "Have a 2-minute intro ready: education, achievements, why this service, future goals."},
    {"name": "🔄 Mock Interviews", "desc": "Practice with friends or join coaching mock interviews. Feedback is invaluable."},
    {"name": "📱 Turn Off Phone", "desc": "Switch off your phone before entering. Nothing worse than a phone ringing during your interview!"}
]

# Common Interview Questions for Govt Jobs
INTERVIEW_QUESTIONS = [
    {"q": "Tell me about yourself.", "tip": "2-min intro covering education, achievements, why this job, and goals. Keep it professional."},
    {"q": "Why do you want to join government service?", "tip": "Talk about job security, serving the nation, making a difference in society."},
    {"q": "What are your strengths and weaknesses?", "tip": "Give genuine strengths with examples. For weakness, mention one you're working to improve."},
    {"q": "Why should we select you?", "tip": "Highlight unique qualities, relevant experience, and passion for public service."},
    {"q": "What do you know about this department/organization?", "tip": "Mention its functions, recent initiatives, and how you can contribute."},
    {"q": "What are the current challenges facing India?", "tip": "Discuss 2-3 issues like unemployment, climate change, healthcare with balanced views."},
    {"q": "What is your opinion on [Current Issue]?", "tip": "Give a balanced view, acknowledge multiple perspectives, suggest solutions."},
    {"q": "Describe a difficult situation you handled.", "tip": "Use STAR method: Situation, Task, Action, Result. Be specific."},
    {"q": "Where do you see yourself in 5 years?", "tip": "Show ambition within the service. Talk about gaining expertise and leadership."},
    {"q": "What are the qualities of a good administrator?", "tip": "Integrity, empathy, decisiveness, communication, adaptability. Give examples."},
    {"q": "How do you handle stress?", "tip": "Mention healthy coping: exercise, prioritization, staying calm under pressure."},
    {"q": "What is the role of civil servants in democracy?", "tip": "Policy implementation, public welfare, neutrality, accountability, bridging govt-citizen gap."},
    {"q": "Any questions for us?", "tip": "Ask about training programs, posting locations, or growth opportunities. Never say 'No questions'."},
    {"q": "What are three recent government schemes?", "tip": "Know details of PM schemes in your sector: eligibility, budget, impact."},
    {"q": "How will you handle a corrupt senior officer?", "tip": "Diplomatic answer: follow rules, document evidence, use proper channels, maintain integrity."}
]
