def simple_report(beam):
    L = beam.length
    RA = beam._reactions['A']
    RB = beam._reactions['B']
    lines = []
    lines.append(f"Viga biapoiada, comprimento L = {L} m")
    lines.append("")
    lines.append("Equilíbrio vertical: ΣFy = 0 -> RA + RB = W_total")
    lines.append(f"RA + RB = {RA:.3f} + {RB:.3f} = {RA+RB:.3f} kN (soma das reações)")
    lines.append("")
    lines.append("Momento em A: ΣMA = 0 -> RB * L = Σ (load * x)")
    lines.append(f"RB * L = {RB:.3f} * {L} = {RB*L:.3f} kN·m")
    lines.append("")
    lines.append("(Relatório gerado automaticamente — confira unidades e sinais.)")
    return "\n\n".join(lines)
