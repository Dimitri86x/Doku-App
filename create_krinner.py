import ezdxf
import math

def create_krinner_v114_dxf(filename="Krinner_V114_2000.dxf"):
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # Originalmaße Krinner V 114 x 2000
    L = 2000          # Gesamtlänge
    D = 114           # Rohrdurchmesser
    F_D = 160         # Flanschdurchmesser
    F_T = 15          # Flanschdicke (ca. 15mm Stahl)
    G_L = 600         # Gewindelänge (konisch zulaufend)

    # --- SEITENANSICHT ---
    # Flansch (Oben)
    msp.add_lwpolyline([(-F_D/2, 0), (F_D/2, 0), (F_D/2, -F_T), (-F_D/2, -F_T), (-F_D/2, 0)])

    # Rohrschaft (bis zum Gewindeanfang)
    msp.add_line((-D/2, -F_T), (-D/2, -(L - G_L)))
    msp.add_line((D/2, -F_T), (D/2, -(L - G_L)))

    # Konische Spitze
    msp.add_line((-D/2, -(L - G_L)), (0, -L))
    msp.add_line((D/2, -(L - G_L)), (0, -L))

    # Grobes Gewinde (Zickzack-Visualisierung)
    pitch = 50
    for i in range(0, G_L, pitch):
        y_start = -(L - G_L + i)
        y_mid = y_start - (pitch / 2)
        # Radiusberechnung für Konus an dieser Stelle
        r_curr = (D/2) * (1 - (i / G_L))
        r_next = (D/2) * (1 - ((i + pitch/2) / G_L))

        # Gewindegang rechts
        msp.add_line((r_curr, y_start), (r_curr + 15, y_mid))
        msp.add_line((r_curr + 15, y_mid), (r_next, y_mid - pitch/2))

    # --- DRAUFSICHT (Rechts daneben versetzt) ---
    offset = 300
    msp.add_circle((offset, 0), F_D/2) # Außenkante Flansch
    msp.add_circle((offset, 0), D/2)   # Rohrinnenkante

    # Lochkreis für 6 Schrauben (typisch für Krinner V-Serie)
    hole_circle_r = 135 / 2 # Angenommener Lochkreisradius
    for a in range(0, 360, 60):
        rad = math.radians(a)
        x = offset + hole_circle_r * math.cos(rad)
        y = hole_circle_r * math.sin(rad)
        msp.add_circle((x, y), 9) # 18mm Bohrungen

    doc.saveas(filename)
    print(f"Datei '{filename}' wurde erstellt.")

create_krinner_v114_dxf()
