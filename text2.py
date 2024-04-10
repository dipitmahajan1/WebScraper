def solution(A):
    # Implement your solution here


    a = sorted(A)

    print(a)

    res_a = set(a)

    final_a = list(res_a)

    size = len(final_a)

    if final_a[size-1] < 0 :

        return 1
    else :

        for i in range(size-1) :

            if final_a[i+1] - final_a[i] == 1 :

                continue 
            else :


                return final_a[i] + 1

        return final_a[size-1]  + 1
   
    pass



x = solution( [1, 3, 6, 4, 1, 2])


print(x)