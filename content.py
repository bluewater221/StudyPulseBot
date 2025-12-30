# Content for Civil Engineering GATE Bot

QUESTIONS = [
    {
        "question": "In a consolidation test, if the drainage path for double drainage is 'd', what is the thickness of the clay layer?",
        "options": ["A) d", "B) 2d", "C) d/2", "D) 4d"],
        "answer": "B"
    },
    {
        "question": "Which of the following fluids exhibits a linear relationship between shear stress and rate of shear strain?",
        "options": ["A) Dilatant fluid", "B) Bingham plastic", "C) Newtonian fluid", "D) Pseudoplastic fluid"],
        "answer": "C"
    },
    {
        "question": "The Maximum Bending Moment in a simply supported beam of span L carrying a uniformly distributed load 'w' per unit length is:",
        "options": ["A) wL^2/8", "B) wL^2/4", "C) wL/2", "D) wL^2/12"],
        "answer": "A"
    },
    {
        "question": "As per IS 456:2000, the minimum grade of concrete for reinforced concrete work in 'Severe' exposure condition is:",
        "options": ["A) M20", "B) M25", "C) M30", "D) M35"],
        "answer": "C"
    },
    {
        "question": "The ratio of inertia force to viscous force is known as:",
        "options": ["A) Froude Number", "B) Reynolds Number", "C) Mach Number", "D) Weber Number"],
        "answer": "B"
    }
]

FACTS = [
    "The slenderness ratio of a column is defined as the ratio of its effective length to its least radius of gyration.",
    "BOD (Biochemical Oxygen Demand) is a measure of the amount of oxygen required by aerobic microorganisms to decompose organic matter.",
    "In a soil sample, if the void ratio is 'e', the porosity 'n' is given by n = e / (1 + e).",
    "Bernoulli's equation is based on the principle of conservation of energy.",
    "The Point of Contraflexure is the point where the Bending Moment changes its sign.",
    "For a logically determinate truss with 'm' members and 'j' joints, the condition for stability is m = 2j - 3.",
    "Quick sand condition occurs when the effective stress in the soil becomes zero due to upward seepage pressure."
]

FORMULAS = [
    {
        "title": "Reynolds Number (Re)",
        "formula": "Re = (rho * v * D) / mu",
        "explanation": "Where rho=density, v=velocity, D=characteristic length, mu=dynamic viscosity. Re < 2000 implies Laminar flow."
    },
    {
        "title": "Darcy's Law (Groundwater Flow)",
        "formula": "q = k * i * A",
        "explanation": "Where q=discharge, k=permeability, i=hydraulic gradient, A=cross-sectional area."
    },
    {
        "title": "Bending Equation",
        "formula": "M/I = sigma/y = E/R",
        "explanation": "M=Moment, I=Moment of Inertia, sigma=Bending Stress, y=Dist. from NA, E=Young's Modulus, R=Radius of Curvature."
    },
    {
        "title": "Void Ratio & Porosity",
        "formula": "e = n / (1 - n)",
        "explanation": "Relationship between Void Ratio (e) and Porosity (n). Also, Se = wG (Saturation * Void Ratio = Water Content * Specific Gravity)."
    },
     {
        "title": "Euler's Buckling Load",
        "formula": "P_cr = (pi^2 * E * I) / (L_eff)^2",
        "explanation": "Critical load for a column. L_eff depends on end conditions (e.g., L_eff = L for pinned-pinned)."
    }
]
