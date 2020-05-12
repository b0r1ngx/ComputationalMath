def QUANC8(FUN, A, B, ABSERR, RELERR, RESULT, ERREST, NOFUN, FLAG):
    QRIGHT = (0.0 for i in range(31))
    F, X = (0.0 for i in range(16))
    FSAVE, XSAVE = (0.0 for j in range(30) for i in range(8))
    LEVMIN, LEVMAX, LEVOUT, NOMAX, NOFIN, LEV, NIM = 0
    W0, W1, W2, W3, W4, COR11, AREA, X0, F0, STONE, STEP = 0.0
    QPREV, QNOW, QDIFF, QLEFT, ESTERR, TOLERR = 0.0

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

    FLAG = 0.0
    RESULT = 0.0
    ERREST = 0.0
    NOFUN = 0

    # Stage 2
    NIM = 1
    X0 = A
    X[16] = B
    F0 = FUN(X0)
    STONE = (B - A) / 16
    X[8] = (X0 + X[16]) / 2
    X[4] = (X0 + X[8]) / 2
    X[12] = (X[8] + X[16]) / 2
    X[2] = (X0 + X[4]) / 2
    X[6] = (X[4] + X[8]) / 2
    X[10] = (X[8] + X[12]) / 2
    X[14] = (X[12] + X[16]) / 2
    for J in range(2, 16, 2):
        F[J] = FUN(X[J])
    NOFUN = 9

    def trenta():
        X[1] = (X0 + X[2]) / 2
        F[1] = FUN(X[1])
        for J in range(3, 15, 2):
            X[J] = (X[J - 1] + X[J + 1]) / 2
            F[J] = FUN(X[J])
        nonlocal NOFUN
        NOFUN += 8
        STEP = (X[16] - X0) / 16
        QLEFT = (W0 * (F0 + F[8])
                 + W1 * (F[1] + F[7])
                 + W2 * (F[2] + F[6])
                 + W3 * (F[3] + F[5])
                 + W4 * F[4]) * STEP
        QRIGHT[LEV + 1] = (W0 * (F[8] + F[16])
                           + W1 * (F[9] + F[15])
                           + W2 * (F[10] + F[14])
                           + W3 * (F[11] + F[13])
                           + W4 * F[12]) * STEP
        QNOW = QLEFT + QRIGHT[LEV + 1]
        QDIFF = QNOW - QPREV
        nonlocal AREA
        AREA += QDIFF

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

    def fifty():
        nonlocal NIM
        NIM *= 2
        nonlocal LEV
        LEV += 1
        for I in range(8):
            FSAVE[I][LEV] = F[I + 8]
            XSAVE[I][LEV] = X[I + 8]
        QPREV = QLEFT
        for I in range(8):
            J = -I
            F[2 * J + 18] = F[J + 9]
            X[2 * J + 18] = X[J + 9]
        trenta()

    def sixty():
        nonlocal NOFIN
        NOFIN *= NOFIN
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
        nonlocal NIM
        nonlocal LEV
        while NIM % 2 != 0:
            NIM /= 2
            LEV -= 1
        NIM += 1
        if LEV <= 0:
            eighty()
        QPREV = QRIGHT[LEV]
        X0 = X[16]
        F0 = F[16]
        for I in range(8):
            F[2 * I] = FSAVE[I][LEV]
            X[2 * I] = XSAVE[I][LEV]
        trenta()

    def eighty():
        nonlocal RESULT
        RESULT += COR11
        nonlocal ERREST
        if ERREST == 0.0:
            return
        while abs(RESULT) + ERREST == abs(RESULT):
            ERREST *= 2
        return