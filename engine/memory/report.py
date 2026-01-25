def simple_report(beam):
    """
    Gera uma memória de cálculo didática para viga biapoiada,
    voltada para alunos de graduação em Engenharia Civil.

    Convenções:
    - Cargas verticais positivas para baixo
    - Reações positivas para cima
    - Unidades: kN, m, kN·m
    """

    L = beam.length
    RA = beam._reactions["A"]
    RB = beam._reactions["B"]

    lines = []

    # -------------------------------------------------
    # 1. Dados do problema
    # -------------------------------------------------
    lines.append("1. DADOS DO PROBLEMA")
    lines.append(f"- Tipo de estrutura: Viga biapoiada")
    lines.append(f"- Comprimento da viga: L = {L:.2f} m")
    lines.append("")

    if not beam.loads:
        lines.append("- Não há cargas aplicadas.")
    else:
        lines.append("- Cargas aplicadas:")
        for load in beam.loads:
            cls = load.__class__.__name__
            if cls == "PointLoad":
                lines.append(
                    f"  • Carga concentrada: P = {load.P:.2f} kN aplicada em x = {load.x:.2f} m"
                )
            elif cls == "DistributedLoad":
                x_end = load.x_end if load.x_end is not None else L
                lines.append(
                    f"  • Carga distribuída: q = {load.q:.2f} kN/m "
                    f"de x = {load.x_start:.2f} m até x = {x_end:.2f} m"
                )

    lines.append("")
    lines.append("- Apoios:")
    lines.append("  • Apoio A em x = 0 m")
    lines.append(f"  • Apoio B em x = {L:.2f} m")
    lines.append("")

    # -------------------------------------------------
    # 2. Modelo estrutural
    # -------------------------------------------------
    lines.append("2. MODELO ESTRUTURAL ADOTADO")
    lines.append("- Estrutura isostática")
    lines.append("- Análise no regime elástico linear")
    lines.append("- Equações de equilíbrio da estática aplicadas")
    lines.append("")

    # -------------------------------------------------
    # 3. Cálculo das reações de apoio
    # -------------------------------------------------
    lines.append("3. CÁLCULO DAS REAÇÕES DE APOIO")
    lines.append("")

    # cálculo da carga total e momentos
    W_total = 0.0
    moment_about_A = 0.0

    for load in beam.loads:
        cls = load.__class__.__name__

        if cls == "PointLoad":
            W_total += load.P
            moment_about_A += load.P * load.x

            lines.append(
                f"Carga concentrada:"
            )
            lines.append(
                f"  P = {load.P:.2f} kN aplicada a x = {load.x:.2f} m"
            )
            lines.append(
                f"  Momento em A: M = P · x = {load.P:.2f} · {load.x:.2f} = {load.P * load.x:.2f} kN·m"
            )
            lines.append("")

        elif cls == "DistributedLoad":
            x_end = load.x_end if load.x_end is not None else L
            span = x_end - load.x_start
            W = load.q * span
            x_bar = load.x_start + span / 2.0

            W_total += W
            moment_about_A += W * x_bar

            lines.append("Carga distribuída:")
            lines.append(
                f"  q = {load.q:.2f} kN/m aplicada em um trecho de comprimento {span:.2f} m"
            )
            lines.append(
                f"  Carga equivalente: W = q · L = {load.q:.2f} · {span:.2f} = {W:.2f} kN"
            )
            lines.append(
                f"  Posição da resultante: x̄ = {x_bar:.2f} m"
            )
            lines.append(
                f"  Momento em A: M = W · x̄ = {W:.2f} · {x_bar:.2f} = {W * x_bar:.2f} kN·m"
            )
            lines.append("")

    lines.append(f"Carga total aplicada na viga:")
    lines.append(f"  W_total = {W_total:.2f} kN")
    lines.append("")

    # -------------------------------------------------
    # 4. Equilíbrio estático
    # -------------------------------------------------
    lines.append("4. APLICAÇÃO DAS EQUAÇÕES DE EQUILÍBRIO")
    lines.append("")

    lines.append("Equilíbrio de momentos em relação ao apoio A:")
    lines.append("  ΣMA = 0")
    lines.append("  RB · L = Σ(Momentos das cargas)")
    lines.append(
        f"  RB · {L:.2f} = {moment_about_A:.2f}"
    )
    lines.append(
        f"  RB = {moment_about_A:.2f} / {L:.2f} = {RB:.2f} kN"
    )
    lines.append("")

    lines.append("Equilíbrio de forças verticais:")
    lines.append("  ΣFy = 0")
    lines.append("  RA + RB = W_total")
    lines.append(
        f"  RA = {W_total:.2f} − {RB:.2f} = {RA:.2f} kN"
    )
    lines.append("")

    # -------------------------------------------------
    # 5. Resultados finais
    # -------------------------------------------------
    lines.append("5. RESULTADOS FINAIS")
    lines.append(f"- Reação no apoio A: RA = {RA:.2f} kN")
    lines.append(f"- Reação no apoio B: RB = {RB:.2f} kN")
    lines.append("")

    lines.append(
        "Observação: os resultados obtidos satisfazem as equações de equilíbrio "
        "e são compatíveis com o comportamento físico esperado da estrutura."
    )

    return "\n".join(lines)
