def QUANC8(FUN, A, B, ABSERR, RELERR, RESULT, ERREST, NOFUN, FLAG):
    QRIGHT = [0.0 for I in range(31)]
    F = [0.0 for I in range(16)]
    X = [0.0 for I in range(16)]
    FSAVE = [[0.0 for J in range(30)] for I in range(8)]
    XSAVE = [[0.0 for J in range(30)] for I in range(8)]
    LEVMIN, LEVMAX, LEVOUT, NOMAX, NOFIN, LEV, NIM = 0, 0, 0, 0, 0, 0, 0
    W0, W1, W2, W3, W4 = 0.0, 0.0, 0.0, 0.0, 0.0
    COR11, AREA, X0, F0, STONE, STEP = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    QPREV, QNOW, QDIFF, QLEFT, ESTERR, TOLERR = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    if A == B:
        return

    # Stage 1
    LEVMIN = 1
    LEVMAX = 30
    LEVOUT = 6
    NOMAX = 5000
    NOFIN = NOMAX - 8 * (LEVMAX - LEVOUT + 2 ** (LEVOUT + 1))

    W0 = 3956 / 14175
    W1 = 23552 / 14175
    W2 = -3712 / 14175
    W3 = 41974 / 14175
    W4 = -18160 / 14175

    RESULT = 0.0
    ERREST = 0.0
    NOFUN = 0
    FLAG = 0.0

    # Stage 2
    NIM = 1
    X0 = A
    X[15] = B
    F0 = FUN(X0)
    STONE = (B - A) / 16
    X[7] = (X0 + X[15]) / 2
    X[3] = (X0 + X[7]) / 2
    X[11] = (X[7] + X[15]) / 2
    X[1] = (X0 + X[3]) / 2
    X[5] = (X[3] + X[7]) / 2
    X[9] = (X[7] + X[11]) / 2
    X[13] = (X[11] + X[15]) / 2
    for J in range(1, 15, 2):
        F[J] = FUN(X[J])
    NOFUN = 9

    def trenta():
        nonlocal X, F
        X[0] = (X0 + X[2]) / 2
        F[0] = FUN(X[0])
        for J in range(2, 14, 2):
            X[J] = (X[J - 1] + X[J + 1]) / 2
            F[J] = FUN(X[J])
        nonlocal NOFUN
        NOFUN += 8
        nonlocal STEP
        STEP = (X[15] - X0) / 16
        nonlocal QLEFT
        QLEFT = (W0 * (F0 + F[7])
                 + W1 * (F[0] + F[6])
                 + W2 * (F[1] + F[5])
                 + W3 * (F[2] + F[4])
                 + W4 * F[3]) * STEP
        nonlocal QRIGHT
        QRIGHT[LEV + 1] = (W0 * (F[7] + F[15])
                           + W1 * (F[8] + F[14])
                           + W2 * (F[9] + F[13])
                           + W3 * (F[10] + F[12])
                           + W4 * F[11]) * STEP
        nonlocal QNOW
        QNOW = QLEFT + QRIGHT[LEV + 1]
        nonlocal QDIFF
        QDIFF = QNOW - QPREV
        nonlocal AREA
        AREA += QDIFF

    def fifty():
        nonlocal NIM
        NIM *= 2
        nonlocal LEV
        LEV += 1

    def sixty():
        nonlocal NOFIN
        NOFIN *= NOFIN
        nonlocal LEVMAX
        LEVMAX = LEVOUT
        nonlocal FLAG
        FLAG += (B - X0) / (B - A)
        seventy()

    def sixty_two():
        nonlocal FLAG
        FLAG += 1

    def seventy():
        nonlocal RESULT
        RESULT += QNOW
        nonlocal ERREST
        ERREST += ESTERR
        nonlocal COR11
        COR11 += QDIFF / 1023

    def eighty():
        nonlocal RESULT
        RESULT += COR11
        nonlocal ERREST
        if ERREST == 0.0:
            return
        while abs(RESULT) + ERREST == abs(RESULT):
            ERREST *= 2
        return

    trenta()

    # Stage 4
    ESTERR = abs(QDIFF) / 1023
    if ABSERR > (RELERR * abs(AREA)) * (STEP / STONE):
        TOLERR = ABSERR
    else:
        TOLERR = (RELERR * abs(AREA)) * (STEP / STONE)
    if LEV < LEVMIN:
        fifty()
    if LEV >= LEVMAX:
        sixty_two()
    if NOFUN > NOFIN:
        sixty()
    if ESTERR <= TOLERR:
        seventy()

    for I in range(8):
        FSAVE[I][LEV] = F[I + 8]
        XSAVE[I][LEV] = X[I + 8]
    QPREV = QLEFT
    for I in range(8):
        J = -I - 1
        F[2 * J + 17] = F[J + 9]
        X[2 * J + 17] = X[J + 9]
    trenta()

    while NIM % 2 != 0:
        NIM /= 2
        LEV -= 1
    NIM += 1
    if LEV <= 0:
        eighty()
    QPREV = QRIGHT[LEV]
    X0 = X[15]
    F0 = F[15]
    for I in range(8):
        F[2 * I + 1] = FSAVE[I][LEV]
        X[2 * I + 1] = XSAVE[I][LEV]
    trenta()
