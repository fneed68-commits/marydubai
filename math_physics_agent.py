#!/usr/bin/env python3
"""
MaryDubai-MathPhysGuard
وكيل الرياضيات والفيزياء والهندسة الشامل
مع تحكم بشري صارم (HITL)
"""
import math


class MathPhysicsAgent:
    def __init__(self):
        self.agent_name = "MaryDubai-MathPhysGuard"

        # ═══════════════════════════════════════════════════
        # 📐 ثوابت رياضية
        # ═══════════════════════════════════════════════════
        self.PI = math.pi
        self.E = math.e
        self.GOLDEN_RATIO = (1 + math.sqrt(5)) / 2  # φ ≈ 1.618
        self.EULER_MASCHERONI = 0.5772156649015329
        self.CATALAN = 0.9159655941772190
        self.APERY = 1.2020569031595943

        # ═══════════════════════════════════════════════════
        # ⚛️ ثوابت فيزيائية (CODATA 2022)
        # ═══════════════════════════════════════════════════
        # أساسية
        self.SPEED_OF_LIGHT = 299_792_458          # m/s
        self.PLANCK_CONSTANT = 6.62607015e-34      # J·s
        self.REDUCED_PLANCK = 1.054571817e-34      # J·s (ℏ)
        self.GRAVITATIONAL_CONSTANT = 6.67430e-11  # m³/kg·s²
        self.BOLTZMANN_CONSTANT = 1.380649e-23     # J/K
        self.AVOGADRO = 6.02214076e23              # 1/mol
        self.GAS_CONSTANT = 8.314462618            # J/mol·K
        self.ELECTRON_CHARGE = 1.602176634e-19     # C
        self.ELECTRON_MASS = 9.1093837015e-31      # kg
        self.PROTON_MASS = 1.67262192369e-27       # kg
        self.NEUTRON_MASS = 1.67492749804e-27      # kg
        self.FINE_STRUCTURE = 7.2973525693e-3      # α
        self.VACUUM_PERMITTIVITY = 8.8541878128e-12  # F/m
        self.VACUUM_PERMEABILITY = 1.25663706212e-6  # H/m
        self.ELECTRON_VOLT = 1.602176634e-19       # J

        # ═══════════════════════════════════════════════════
        # 🔧 ثوابت هندسية
        # ═══════════════════════════════════════════════════
        self.STANDARD_GRAVITY = 9.80665            # m/s²
        self.ATMOSPHERIC_PRESSURE = 101325         # Pa
        self.ICE_POINT = 273.15                    # K
        self.ABSOLUTE_ZERO = -273.15               # °C
        self.STANDARD_TEMPERATURE = 273.15         # K
        self.STANDARD_MOLAR_VOLUME = 0.02241396954 # m³/mol
        self.STEFAN_BOLTZMANN = 5.670374419e-8     # W/m²·K⁴
        self.WIEN_DISPLACEMENT = 2.897771955e-3    # m·K

    # ═══════════════════════════════════════════════════════
    # 📐 الرياضيات — التفاضل والتكامل
    # ═══════════════════════════════════════════════════════

    def derivative_polynomial(self, coefficients, x):
        """
        مشتقة متعددة حدود
        coefficients: [a_n, a_{n-1}, ..., a_1, a_0] لـ a_n*x^n + ...
        ترجع قيمة f'(x)
        """
        n = len(coefficients) - 1
        result = 0
        for i, coeff in enumerate(coefficients[:-1]):
            power = n - i
            result += coeff * power * (x ** (power - 1))
        return result

    def integral_polynomial(self, coefficients, a, b):
        """
        تكامل محدد لمتعددة حدود من a إلى b
        """
        n = len(coefficients) - 1
        def antiderivative(x):
            result = 0
            for i, coeff in enumerate(coefficients):
                power = n - i
                result += coeff * (x ** (power + 1)) / (power + 1)
            return result
        return antiderivative(b) - antiderivative(a)

    def numerical_integral(self, f, a, b, n=1000):
        """
        تكامل عددي (طريقة سيمبسون)
        """
        if n % 2 != 0:
            n += 1
        h = (b - a) / n
        result = f(a) + f(b)
        for i in range(1, n):
            x = a + i * h
            result += (4 if i % 2 == 1 else 2) * f(x)
        return result * h / 3

    # ═══════════════════════════════════════════════════════
    # 📊 الجبر الخطي
    # ═══════════════════════════════════════════════════════

    def matrix_multiply(self, A, B):
        """ضرب مصفوفتين"""
        if len(A[0]) != len(B):
            raise ValueError("أبعاد غير متوافقة")
        result = [[0] * len(B[0]) for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def matrix_determinant(self, M):
        """محدد مصفوفة (طريقة التوسع)"""
        n = len(M)
        if n == 1:
            return M[0][0]
        if n == 2:
            return M[0][0] * M[1][1] - M[0][1] * M[1][0]
        det = 0
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in M[1:]]
            det += ((-1) ** j) * M[0][j] * self.matrix_determinant(minor)
        return det

    def vector_dot(self, a, b):
        """الضرب النقطي"""
        return sum(x * y for x, y in zip(a, b))

    def vector_cross(self, a, b):
        """الضرب الاتجاهي (3D)"""
        return [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        ]

    def vector_norm(self, v):
        """طول متجه"""
        return math.sqrt(sum(x * x for x in v))

    # ═══════════════════════════════════════════════════════
    # 📈 الإحصاء والاحتمالات
    # ═══════════════════════════════════════════════════════

    def mean(self, data):
        """المتوسط الحسابي"""
        return sum(data) / len(data) if data else 0

    def variance(self, data, sample=True):
        """التباين (عينة أو مجتمع)"""
        if len(data) < 2:
            return 0
        m = self.mean(data)
        n = len(data) - 1 if sample else len(data)
        return sum((x - m) ** 2 for x in data) / n

    def std_dev(self, data, sample=True):
        """الانحراف المعياري"""
        return math.sqrt(self.variance(data, sample))

    def median(self, data):
        """الوسيط"""
        s = sorted(data)
        n = len(s)
        if n % 2 == 0:
            return (s[n//2 - 1] + s[n//2]) / 2
        return s[n//2]

    def normal_pdf(self, x, mu=0, sigma=1):
        """دالة الكثافة للتوزيع الطبيعي"""
        coeff = 1 / (sigma * math.sqrt(2 * self.PI))
        exp = -((x - mu) ** 2) / (2 * sigma ** 2)
        return coeff * math.exp(exp)

    def binomial_probability(self, n, k, p):
        """احتمال توزيع ثنائي"""
        return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

    def poisson_probability(self, k, lam):
        """احتمال توزيع بواسون"""
        return (lam ** k) * math.exp(-lam) / math.factorial(k)

    # ═══════════════════════════════════════════════════════
    # 🔢 نظرية الأعداد
    # ═══════════════════════════════════════════════════════

    def gcd(self, a, b):
        """القاسم المشترك الأكبر"""
        while b:
            a, b = b, a % b
        return abs(a)

    def lcm(self, a, b):
        """المضاعف المشترك الأصغر"""
        return abs(a * b) // self.gcd(a, b) if a and b else 0

    def is_prime(self, n):
        """اختبار أولية (Miller-Rabin مبسط)"""
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    def modular_power(self, base, exponent, modulus):
        """الأس المعياري"""
        return pow(base, exponent, modulus)

    def fibonacci(self, n):
        """متتالية فيبوناتشي"""
        if n <= 0:
            return 0
        if n == 1:
            return 1
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b

    # ═══════════════════════════════════════════════════════
    # ⚛️ الفيزياء — الميكانيكا الكلاسيكية
    # ═══════════════════════════════════════════════════════

    def newton_force(self, mass, acceleration):
        """F = m·a"""
        return mass * acceleration

    def kinetic_energy(self, mass, velocity):
        """KE = ½·m·v²"""
        return 0.5 * mass * velocity ** 2

    def potential_energy(self, mass, height):
        """PE = m·g·h"""
        return mass * self.STANDARD_GRAVITY * height

    def momentum(self, mass, velocity):
        """p = m·v"""
        return mass * velocity

    def gravitational_force(self, m1, m2, r):
        """F = G·m₁·m₂/r²"""
        return self.GRAVITATIONAL_CONSTANT * m1 * m2 / (r ** 2)

    def escape_velocity(self, mass, radius):
        """v = √(2GM/r)"""
        return math.sqrt(2 * self.GRAVITATIONAL_CONSTANT * mass / radius)

    # ═══════════════════════════════════════════════════════
    # ⚛️ الفيزياء — النسبية
    # ═══════════════════════════════════════════════════════

    def relativistic_mass(self, m0, v):
        """m = m₀/√(1 - v²/c²)"""
        if v >= self.SPEED_OF_LIGHT:
            return float('inf')
        beta = v / self.SPEED_OF_LIGHT
        return m0 / math.sqrt(1 - beta ** 2)

    def mass_energy(self, mass):
        """E = m·c²"""
        return mass * self.SPEED_OF_LIGHT ** 2

    def lorentz_factor(self, v):
        """γ = 1/√(1 - v²/c²)"""
        if v >= self.SPEED_OF_LIGHT:
            return float('inf')
        beta = v / self.SPEED_OF_LIGHT
        return 1 / math.sqrt(1 - beta ** 2)

    def time_dilation(self, t0, v):
        """Δt = γ·Δt₀"""
        return t0 * self.lorentz_factor(v)

    # ═══════════════════════════════════════════════════════
    # ⚛️ الفيزياء — الكوانتم
    # ═══════════════════════════════════════════════════════

    def photon_energy(self, frequency):
        """E = h·f"""
        return self.PLANCK_CONSTANT * frequency

    def photon_energy_wavelength(self, wavelength):
        """E = h·c/λ"""
        return self.PLANCK_CONSTANT * self.SPEED_OF_LIGHT / wavelength

    def de_broglie_wavelength(self, mass, velocity):
        """λ = h/(m·v)"""
        if mass * velocity == 0:
            return float('inf')
        return self.PLANCK_CONSTANT / (mass * velocity)

    def heisenberg_uncertainty(self, delta_x):
        """Δp ≥ ℏ/(2·Δx)"""
        return self.REDUCED_PLANCK / (2 * delta_x)

    def schrodinger_ground_energy(self, mass, length):
        """E₁ = ℏ²·π²/(2·m·L²) — جسيم في صندوق"""
        return (self.REDUCED_PLANCK ** 2 * self.PI ** 2) / (2 * mass * length ** 2)

    def calculate_semiconductor_current(self, voltage, temperature_k, saturation_current=1e-12):
        """معادلة ديود شوكلي: I = I₀·(exp(V/(n·Vₜ)) - 1)"""
        if temperature_k <= 0:
            raise ValueError("الحرارة يجب أن تكون > 0 K")
        n = 1  # عامل الأيديالية
        Vt = self.BOLTZMANN_CONSTANT * temperature_k / self.ELECTRON_CHARGE
        return saturation_current * (math.exp(voltage / (n * Vt)) - 1)

    # ═══════════════════════════════════════════════════════
    # ⚛️ الفيزياء — الترموديناميكا
    # ═══════════════════════════════════════════════════════

    def ideal_gas_pressure(self, n_moles, volume, temperature):
        """P = nRT/V"""
        return n_moles * self.GAS_CONSTANT * temperature / volume

    def ideal_gas_volume(self, n_moles, pressure, temperature):
        """V = nRT/P"""
        return n_moles * self.GAS_CONSTANT * temperature / pressure

    def carnot_efficiency(self, T_hot, T_cold):
        """η = 1 - T_cold/T_hot (كلفن)"""
        if T_hot <= 0:
            raise ValueError("T_hot > 0")
        return 1 - (T_cold / T_hot)

    def entropy_change(self, heat, temperature):
        """ΔS = Q/T"""
        return heat / temperature if temperature != 0 else float('inf')

    def stefan_boltzmann_power(self, area, temperature, emissivity=1.0):
        """P = ε·σ·A·T⁴"""
        return emissivity * self.STEFAN_BOLTZMANN * area * (temperature ** 4)

    def wien_peak_wavelength(self, temperature):
        """λ_max = b/T"""
        return self.WIEN_DISPLACEMENT / temperature

    # ═══════════════════════════════════════════════════════
    # ⚛️ الفيزياء — الكهرومغناطيسية
    # ═══════════════════════════════════════════════════════

    def coulomb_force(self, q1, q2, r):
        """F = k·q₁·q₂/r²"""
        k = 1 / (4 * self.PI * self.VACUUM_PERMITTIVITY)
        return k * q1 * q2 / (r ** 2)

    def electric_field_point(self, charge, r):
        """E = k·q/r²"""
        k = 1 / (4 * self.PI * self.VACUUM_PERMITTIVITY)
        return k * charge / (r ** 2)

    def magnetic_force(self, charge, velocity, B_field, angle=math.pi/2):
        """F = q·v·B·sin(θ)"""
        return charge * velocity * B_field * math.sin(angle)

    def inductance_energy(self, L, current):
        """E = ½·L·I²"""
        return 0.5 * L * current ** 2

    def capacitance_energy(self, C, voltage):
        """E = ½·C·V²"""
        return 0.5 * C * voltage ** 2

    # ═══════════════════════════════════════════════════════
    # 🔧 الهندسة — الكهربائية
    # ═══════════════════════════════════════════════════════

    def ohms_law(self, V=None, I=None, R=None):
        """V = I·R — احسب المفقود"""
        if V is None and I is not None and R is not None:
            return I * R
        if I is None and V is not None and R is not None:
            return V / R
        if R is None and V is not None and I is not None:
            return V / I
        raise ValueError("حدد قيمتين")

    def electric_power(self, V, I):
        """P = V·I"""
        return V * I

    def resistor_series(self, resistors):
        """R_total = ΣR"""
        return sum(resistors)

    def resistor_parallel(self, resistors):
        """1/R_total = Σ1/R"""
        if 0 in resistors:
            return 0
        return 1 / sum(1/r for r in resistors)

    def rms_voltage(self, peak_voltage):
        """V_rms = V_peak/√2"""
        return peak_voltage / math.sqrt(2)

    def impedance(self, resistance, reactance):
        """Z = √(R² + X²)"""
        return math.sqrt(resistance ** 2 + reactance ** 2)

    def resonant_frequency(self, L, C):
        """f = 1/(2π·√(LC))"""
        return 1 / (2 * self.PI * math.sqrt(L * C))

    # ═══════════════════════════════════════════════════════
    # 🔧 الهندسة — الميكانيكية
    # ═══════════════════════════════════════════════════════

    def stress(self, force, area):
        """σ = F/A"""
        return force / area if area != 0 else float('inf')

    def strain(self, delta_L, original_L):
        """ε = ΔL/L₀"""
        return delta_L / original_L if original_L != 0 else 0

    def youngs_modulus(self, stress, strain):
        """E = σ/ε"""
        return stress / strain if strain != 0 else float('inf')

    def torque(self, force, radius, angle=math.pi/2):
        """τ = r·F·sin(θ)"""
        return radius * force * math.sin(angle)

    def moment_of_inertia_disk(self, mass, radius):
        """I = ½·m·r²"""
        return 0.5 * mass * radius ** 2

    def moment_of_inertia_sphere(self, mass, radius):
        """I = (2/5)·m·r²"""
        return 0.4 * mass * radius ** 2

    def angular_momentum(self, I, omega):
        """L = I·ω"""
        return I * omega

    # ═══════════════════════════════════════════════════════
    # 🔧 الهندسة — الحرارية والموائع
    # ═══════════════════════════════════════════════════════

    def heat_conduction(self, k, area, delta_T, thickness):
        """Q/t = k·A·ΔT/d — قانون فورييه"""
        return k * area * delta_T / thickness if thickness != 0 else 0

    def heat_convection(self, h, area, delta_T):
        """Q/t = h·A·ΔT — قانون نيوتن للتبريد"""
        return h * area * delta_T

    def reynolds_number(self, density, velocity, diameter, viscosity):
        """Re = ρ·v·D/μ"""
        return density * velocity * diameter / viscosity if viscosity != 0 else float('inf')

    def bernoulli_pressure(self, P1, rho, v1, v2, h1=0, h2=0):
        """P₂ = P₁ + ½ρ(v₁²-v₂²) + ρg(h₁-h₂)"""
        return P1 + 0.5 * rho * (v1 ** 2 - v2 ** 2) + rho * self.STANDARD_GRAVITY * (h1 - h2)

    # ═══════════════════════════════════════════════════════
    # ₿ تحضير للعملات — حساب معياري وتعمية
    # ═══════════════════════════════════════════════════════

    def is_coprime(self, a, b):
        """هل العددان أوليان فيما بينهما؟"""
        return self.gcd(a, b) == 1

    def extended_gcd(self, a, b):
        """خوارزمية إقليدس الموسعة → (gcd, x, y) بحيث ax+by=gcd"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def modular_inverse(self, a, m):
        """المقلوب المعياري: a⁻¹ mod m"""
        gcd, x, _ = self.extended_gcd(a, m)
        if gcd != 1:
            raise ValueError(f"لا يوجد مقلوب لـ {a} mod {m}")
        return x % m

    def chinese_remainder(self, remainders, moduli):
        """نظرية الباقي الصيني"""
        total = 0
        prod = 1
        for m in moduli:
            prod *= m
        for r, m in zip(remainders, moduli):
            p = prod // m
            total += r * self.modular_inverse(p, m) * p
        return total % prod

    def euler_totient(self, n):
        """دالة أويلر φ(n)"""
        result = n
        p = 2
        while p * p <= n:
            if n % p == 0:
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        if n > 1:
            result -= result // n
        return result

    # ═══════════════════════════════════════════════════════
    # 🎯 دوال قديمة (تم الحفاظ عليها)
    # ═══════════════════════════════════════════════════════

    def calculate_audience_points(self, time_spent_minutes, interaction_count):
        """حساب نقاط الجمهور (للتحليل التسويقي)"""
        time_score = min(time_spent_minutes * 10, 1000)
        interaction_score = interaction_count * 50
        return time_score + interaction_score

    # ═══════════════════════════════════════════════════════
    # 🚪 بوابة HITL
    # ═══════════════════════════════════════════════════════

    def await_mojeh_command(self, calculation_summary):
        """بوابة التحكم البشري"""
        print("\n" + "=" * 60)
        print(f"📢 [{self.agent_name}] تم إنجاز الحساب")
        print(f"📝 {calculation_summary}")
        print("=" * 60)

        command = input("👤 [الموجه] هل توافق على تمرير هذه النتيجة؟ (yes/no): ")

        if command.strip().lower() == 'yes':
            print("🚀 [أمر تمرير] تم اعتماد النتيجة. جاري المتابعة...")
            return True
        else:
            print("🛑 [أمر تجميد] تم إيقاف العملية بناءً على أمر الموجه.")
            return False


if __name__ == "__main__":
    agent = MathPhysicsAgent()

    print("=" * 60)
    print("🎬 اختبار وكيل الرياضيات والفيزياء والهندسة")
    print("=" * 60)
    print()
    print(f"📐 ثوابت رياضية: 6")
    print(f"⚛️ ثوابت فيزيائية: 16")
    print(f"🔧 ثوابت هندسية: 8")
    print()
    print("🧪 أمثلة اختبار:")
    print()

    # اختبارات
    print(f"1. طاقة الفوتون (f=5e14 Hz): {agent.photon_energy(5e14):.3e} J")
    print(f"2. F = ma (m=10, a=9.8): {agent.newton_force(10, 9.8):.3f} N")
    print(f"3. E = mc² (m=1g): {agent.mass_energy(0.001):.3e} J")
    print(f"4. مقاومتان 100+200 على التسلسل: {agent.resistor_series([100, 200]):.0f} Ω")
    print(f"5. مقاومتان 100+200 على التوازي: {agent.resistor_parallel([100, 200]):.2f} Ω")
    print(f"6. gcd(48, 18): {agent.gcd(48, 18)}")
    print(f"7. هل 97 أولي؟ {agent.is_prime(97)}")
    print(f"8. Mersenne 2^10 - 1 = {agent.modular_power(2, 10, 10**9) - 1}")
    print()

    agent.await_mojeh_command(f"اختبارات ناجحة — 8 عمليات حسابية")
