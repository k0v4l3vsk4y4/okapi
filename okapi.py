
import src.markbw as markbw
import src.plothistset as plothistset


aux = True
while (aux):
    print("OPTIONS:")
    print("[1] mark-bw")
    print("[2] plot-hist-set")
    print("[3] other")  
    print("[4] exit")

    opcion = input("Write the number opcion (\"1\", \"2\", \"3\" or \"4\"): ")
    if opcion == "1'":
        markbw.markbw(False)
    elif opcion == "1":
        markbw.markbw(True)
    elif opcion == "2'":
        plothistset.plothistset(False)
    elif opcion == "2":
        plothistset.plothistset(True)
    elif opcion == "3":
        print("Elegiste la opción 3")
    elif opcion == "4":
        print("Exit.")
        aux = False
    else:
        print("Opción no válida")
   
