Sub main()
    ' adaptado da sabrina

    dim fizz as integer
    dim buzz as integer
    dim fizzbuzz as integer
    dim n as integer
    dim tres as integer
    dim cinco as integer
    dim flag as boolean

    n = INPUT
    fizz = 10000
    buzz = 20000
    fizzbuzz = 30000
    flag = True

    while n > 0
        tres = (n - (n / 3 * 3))
        cinco = (n - (n / 5 * 5))

        print n
        'print tres
        'print cinco

        if (tres = 0) and (cinco = 0) then
            print fizzbuzz
            flag = False
        end if

        if (tres = 0) and (flag = True) then
            print fizz
            flag = False
        end if

        if (cinco = 0) and (flag = True) then
            print buzz
            flag = False
        end if

        flag = True
        n = n - 1
    wend
end sub