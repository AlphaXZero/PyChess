def draw_knight(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE
    # rectangle nez
    canvas.create_rectangle(
        x + gp(20),
        y + gp(40),
        x + gp(90),
        y + gp(60),
        **settings,
    )
    # triangle nez
    canvas.create_polygon(
        x + gp(20),
        y + gp(40),
        x + gp(68),
        y + gp(40),
        x + gp(70),
        y + gp(20),
        **settings,
    )
    # rectangle corps
    canvas.create_rectangle(
        x + gp(60),
        y + gp(20),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # base
    canvas.create_rectangle(
        x + gp(40),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # triangle pied
    canvas.create_polygon(
        x + gp(40),
        y + gp(80),
        x + gp(70),
        y + gp(60),
        x + gp(70),
        y + gp(80),
        **settings,
    )
    # rectanle oreille
    canvas.create_rectangle(
        x + gp(60),
        y + gp(10),
        x + gp(80),
        y + gp(20),
        **settings,
    )
    # rectangle oreille
    canvas.create_line(x + gp(60), y + gp(10), x + gp(60), y + gp(24), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(10), x + gp(80), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(60), y + gp(10), x + gp(80), y + gp(10), **LINE_SETTINGS)
    # ligne droite oreille
    canvas.create_line(x + gp(80), y + gp(20), x + gp(90), y + gp(20), **LINE_SETTINGS)
    # corps ligne vertical
    canvas.create_line(x + gp(90), y + gp(20), x + gp(90), y + gp(90), **LINE_SETTINGS)
    # pied
    canvas.create_line(x + gp(40), y + gp(90), x + gp(90), y + gp(90), **LINE_SETTINGS)
    # pied gauche
    canvas.create_line(x + gp(40), y + gp(80), x + gp(40), y + gp(90), **LINE_SETTINGS)
    # hyppotenuse pied
    canvas.create_line(x + gp(40), y + gp(80), x + gp(60), y + gp(65), **LINE_SETTINGS)
    # mileu gauche
    canvas.create_line(x + gp(60), y + gp(66), x + gp(60), y + gp(62), **LINE_SETTINGS)
    # mileu horizontal
    canvas.create_line(x + gp(20), y + gp(62), x + gp(60), y + gp(62), **LINE_SETTINGS)
    # nez vertical
    canvas.create_line(x + gp(20), y + gp(62), x + gp(20), y + gp(40), **LINE_SETTINGS)
    # nez hyppotenuse
    canvas.create_line(x + gp(20), y + gp(40), x + gp(60), y + gp(23), **LINE_SETTINGS)

    # cercle oeil
    settings["fill"] = "black"
    canvas.create_oval(x + gp(60), y + gp(30), x + gp(70), y + gp(40), **settings)


def draw_rook(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE

    # rectanngle corps
    canvas.create_rectangle(
        x + gp(30),
        y + gp(40),
        x + gp(70),
        y + gp(80),
        **settings,
    )
    # rectangle sommet
    canvas.create_rectangle(
        x + gp(24),
        y + gp(20),
        x + gp(76),
        y + gp(40),
        **settings,
    )
    # petit rectangles sommets
    canvas.create_rectangle(
        x + gp(24),
        y + gp(10),
        x + gp(34),
        y + gp(20),
        **settings,
    )
    canvas.create_rectangle(
        x + gp(44),
        y + gp(10),
        x + gp(56),
        y + gp(20),
        **settings,
    )
    canvas.create_rectangle(
        x + gp(66),
        y + gp(10),
        x + gp(76),
        y + gp(20),
        **settings,
    )
    # base
    settings.update({"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS["fill"]})
    canvas.create_rectangle(
        x + gp(20),
        y + gp(70),
        x + gp(80),
        y + gp(90),
        **settings,
    )
    # petites lignes base
    canvas.create_line(x + gp(20), y + gp(70), x + gp(30), y + gp(70), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(70), x + gp(70), y + gp(70), **LINE_SETTINGS)
    # corps
    canvas.create_line(x + gp(30), y + gp(70), x + gp(30), y + gp(40), **LINE_SETTINGS)
    canvas.create_line(x + gp(70), y + gp(70), x + gp(70), y + gp(40), **LINE_SETTINGS)
    # petutes lignes bas ehaut
    canvas.create_line(x + gp(24), y + gp(40), x + gp(76), y + gp(40), **LINE_SETTINGS)
    canvas.create_line(x + gp(76), y + gp(40), x + gp(70), y + gp(40), **LINE_SETTINGS)
    # haut cotés
    canvas.create_line(x + gp(24), y + gp(40), x + gp(24), y + gp(10), **LINE_SETTINGS)
    canvas.create_line(x + gp(76), y + gp(40), x + gp(76), y + gp(10), **LINE_SETTINGS)
    # petites lignes sommet
    canvas.create_line(x + gp(24), y + gp(10), x + gp(34), y + gp(10), **LINE_SETTINGS)
    canvas.create_line(x + gp(44), y + gp(10), x + gp(56), y + gp(10), **LINE_SETTINGS)
    canvas.create_line(x + gp(66), y + gp(10), x + gp(76), y + gp(10), **LINE_SETTINGS)
    # petites lignes sommet bas
    canvas.create_line(x + gp(34), y + gp(20), x + gp(44), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(66), y + gp(20), x + gp(56), y + gp(20), **LINE_SETTINGS)
    # peties lignes verticales
    canvas.create_line(x + gp(24), y + gp(10), x + gp(24), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(34), y + gp(10), x + gp(34), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(44), y + gp(10), x + gp(44), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(56), y + gp(10), x + gp(56), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(66), y + gp(10), x + gp(66), y + gp(20), **LINE_SETTINGS)


def draw_pawn(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(20),
        y + gp(70),
        x + gp(80),
        y + gp(90),
        **settings,
    )
    # trapeze corps
    canvas.create_polygon(
        x + gp(30),
        y + gp(70),
        x + gp(40),
        y + gp(50),
        x + gp(60),
        y + gp(50),
        x + gp(70),
        y + gp(70),
        **settings,
    )
    # rectangle sommet
    settings.update({"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS["fill"]})
    canvas.create_rectangle(x + gp(34), y + gp(30), x + gp(66), y + gp(50), **settings)
    # rond sommmet

    canvas.create_oval(x + gp(40), y + gp(10), x + gp(60), y + gp(30), **settings)
    # base
    canvas.create_line(x + gp(20), y + gp(90), x + gp(80), y + gp(90), **LINE_SETTINGS)
    canvas.create_line(x + gp(20), y + gp(90), x + gp(20), y + gp(70), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(90), x + gp(80), y + gp(70), **LINE_SETTINGS)
    # base haut
    canvas.create_line(x + gp(80), y + gp(70), x + gp(70), y + gp(70), **LINE_SETTINGS)
    canvas.create_line(x + gp(20), y + gp(70), x + gp(30), y + gp(70), **LINE_SETTINGS)
    # triangle coté
    canvas.create_line(x + gp(30), y + gp(70), x + gp(40), y + gp(50), **LINE_SETTINGS)
    canvas.create_line(x + gp(70), y + gp(70), x + gp(60), y + gp(50), **LINE_SETTINGS)


def draw_bishop(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE
    settings.update({"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS["fill"]})

    # ovale corps
    canvas.create_oval(
        x + gp(35),
        y + gp(20),
        x + gp(65),
        y + gp(80),
        **settings,
    )
    # rond sommmet
    canvas.create_oval(
        x + gp(46),
        y + gp(10),
        x + gp(54),
        y + gp(20),
        **settings,
    )
    # base
    canvas.create_rectangle(
        x + gp(25),
        y + gp(75),
        x + gp(75),
        y + gp(90),
        **settings,
    )


def draw_queen(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(10),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # grand triangle
    canvas.create_polygon(
        x + gp(20),
        y + gp(80),
        x + gp(80),
        y + gp(80),
        x + gp(50),
        y + gp(40),
        **settings,
    )
    settings.update({"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS["fill"]})
    # petit triangle
    canvas.create_polygon(
        x + gp(50),
        y + gp(44),
        x + gp(30),
        y + gp(20),
        x + gp(70),
        y + gp(20),
        **settings,
    )
    # rond sommet

    canvas.create_oval(
        x + gp(46),
        y + gp(10),
        x + gp(54),
        y + gp(20),
        **settings,
    )
    # base
    canvas.create_line(x + gp(10), y + gp(90), x + gp(90), y + gp(90), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(90), x + gp(10), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(90), x + gp(90), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(80), x + gp(20), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(80), x + gp(80), y + gp(80), **LINE_SETTINGS)
    # trianle bas
    canvas.create_line(x + gp(20), y + gp(80), x + gp(50), y + gp(44), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(80), x + gp(50), y + gp(44), **LINE_SETTINGS)


def draw_king(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(10),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # traèze
    canvas.create_polygon(
        x + gp(20),
        y + gp(80),
        x + gp(80),
        y + gp(80),
        x + gp(70),
        y + gp(50),
        x + gp(30),
        y + gp(50),
        **settings,
    )
    # sommet vertical
    settings.update({"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS["fill"]})
    canvas.create_rectangle(
        x + gp(46),
        y + gp(50),
        x + gp(54),
        y + gp(10),
        **settings,
    )
    # sommet horizontal

    canvas.create_rectangle(
        x + gp(28),
        y + gp(24),
        x + gp(72),
        y + gp(28),
        **settings,
    )
    # base
    canvas.create_line(x + gp(10), y + gp(90), x + gp(90), y + gp(90), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(90), x + gp(10), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(90), x + gp(90), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(80), x + gp(20), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(80), x + gp(80), y + gp(80), **LINE_SETTINGS)
    # trapèze
    canvas.create_line(x + gp(20), y + gp(80), x + gp(30), y + gp(50), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(80), x + gp(70), y + gp(50), **LINE_SETTINGS)
    canvas.create_line(x + gp(30), y + gp(50), x + gp(70), y + gp(50), **LINE_SETTINGS)
