# Universidad del Valle de Guatemala
# Hugo Elvira 15249
# Carlos Solorzano 08832
# Hoja de trabajo 5
# Codigo de simulacion basado en ejemplos de clase y anteriores



import simpy
import random


def proceso(sienv, t_proceso, nombre, ram, cant_mem, cant_ins, inst_t):
    global t_total
    global tiempos
    
    #Simulacion del tiempo al llegar el proceso (parte new)
    yield sienv.timeout(t_proceso)
    print('tiempo: %f - %s (new) solicita %d de memoria ram' % (sienv.now, nombre, cant_mem))
    tiempo_al_llegar = sienv.now 
    
    #Se solicita RAM (admited - ready)
    yield ram.get(cant_mem)
    print('tiempo: %f - %s (admited) solicitud aceptada por %d de memoria ram' % (sienv.now, nombre, cant_mem))

    #almacenara el numero de instrucciones completadas
    ins_complete = 0
    
    while ins_complete < cant_ins:

    
        #se pide conexion con CPU (ready)
        with cpu.request() as req:
            yield req
            #Se determina la instruccion que va a realizarse
            if (cant_ins-ins_complete)>=inst_t:
                efectuar=inst_t
            else:
                efectuar=(cant_ins-ins_complete)

            print('tiempo: %f - %s (ready) cpu ejecutara %d instrucciones' % (sienv.now, nombre, efectuar))
            #tiempo de ejecucion con el numero(efectuar) de instrucciones a ejecutar
            yield sienv.timeout(efectuar/inst_t)

            #Se guarda el numero total de instrucciones completadas
            ins_complete += efectuar
            print('tiempo: %f - %s (runing) cpu (%d/%d) completado' % (sienv.now, nombre, ins_complete, cant_ins))

        #Si atender es 1 espera en cola, si es 2 se va a ready
        atender = random.randint(1,2)

        if atender == 1 and ins_complete<cant_ins:
            #(waiting)
            with espera.request() as req2:
                yield req2
                #tiempo supuesto de espera para operaciones de entrada y salida
                yield sienv.timeout(1)                
                print('tiempo: %f - %s (waiting) realizadas operaciones (entrada/salida)' % (sienv.now, nombre))
    

    #(exit - terminated)
    #cantidad de ram que retorna
    yield ram.put(cant_mem)
    print('tiempo: %f - %s (terminated), retorna %d de memoria ram' % (sienv.now, nombre, cant_mem))
    t_total += (sienv.now - tiempo_al_llegar) #se guarda el total de tiempo por todos los procesos
    tiempos.append(sienv.now - tiempo_al_llegar) #se guarda cada tiempo 
#Definicion de variables
inst_t = 3.0 # cantidad de instrucciones/tiempo
memoria_ram= 100 #se define cantidad de memoria ram
cant_procesos = 25 # cantidad de procesos a ejecutar
t_total=0.0 #inicializa la variable que almacenara el tiempo total de los procesos
tiempos=[] #se guardara cada tiempo individual para extraer la desviacion estandar


sienv = simpy.Environment()  #crear ambiente de simulacion
cpu = simpy.Resource (sienv, capacity=2) #cola para acceso a cpu
ram = simpy.Container(sienv, init=memoria_ram, capacity=memoria_ram) #se crea el simulador para memoria ram
espera = simpy.Resource (sienv, capacity=2) #cola para acceso a operaciones i/o

# Crear semilla para random 
random.seed(1997)
rango = 1 #  numero de intervalos


# Se creean los procesos a simular
for i in range(cant_procesos):
    t_proceso = random.expovariate(1.0 / rango)
    cant_ins = random.randint(1,10) #Se genera una cantidad aleatoria de instrucciones
    cant_mem = random.randint(1,10) #Se genera una cantidad aleatoria de memoria a utilizar
    sienv.process(proceso(sienv, t_proceso, 'Proceso %d' % i, ram, cant_mem, cant_ins, inst_t))

# comienza la simulacion
sienv.run()

#Tiempo promedio por procesos
print " "
prom=(t_total/cant_procesos)
print('El tiempo promeido es: %f' % (prom))


#Desviaccion estandar
sumatoria=0

for xi in tiempos:
    sumatoria+=(xi-prom)**2

desviacions=(sumatoria/(cant_procesos-1))**0.5

print " "
print('La desviacion estandar es: %f' %(desviacions))
