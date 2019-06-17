Function fibonacci(n as integer) as integer
    ' codigo do raphael costa
    dim flag as boolean
    
    flag = false
    if n = 0 then
        fibonacci = 1
        flag = true
    end if

    if n = 1 then 
        fibonacci = 1
        flag = true
    end if

    if flag = false then
        fibonacci = fibonacci(n-2) + fibonacci(n-1)
    end if

End Function
Sub Main()
    print fibonacci(5)
End Sub