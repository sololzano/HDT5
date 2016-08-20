# Universidad del Valle de Guatemala
# Hugo Elvira 15249
# Carlos Solorzano
# Hoja de trabajo 5



import simpy
import random



def proceso(sienv, t_proceso, nombre, ram, cant_mem, cant_ins, inst_t):
    
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
                #tiempo de espera para operaciones de entrada y salida
                yield sienv.timeout(1)                
                print('tiempo: %f - %s (waiting) realizadas operaciones (i/o)' % (sienv.now, nombre))
    

    #(exit - terminated)
    #cantidad de ram que retorna
    yield ram.put(cant_mem)
    print('tiempo: %f - %s (terminated), retorna %d de memoria ram' % (sienv.now, nombre, cant_mem))


#Definicion de variables
inst_t = 3.0 #3 instrucciones/tiempo
memoria_ram= 100 #se define memoria ram de 100
cant_procesos = 100 # cantidad de procesos a ejecutar


sienv = simpy.Environment()  #crear ambiente de simulacion
cpu = simpy.Resource (sienv, capacity=1) #cola para acceso a cpu
ram = simpy.Container(sienv, init=memoria_ram, capacity=memoria_ram) #se crea el simulador para memoria ram
espera = simpy.Resource (sienv, capacity=1) #cola para acceso a operaciones i/o

# Crear semilla para random 
random.seed(1997)
rango = 10 #  numero de intervalos


# Se creean los procesos a simular
for i in range(cant_procesos):
    t_proceso = random.expovariate(1.0 / rango)
    cant_ins = random.randint(1,10) #Se genera una cantidad aleatoria de instrucciones
    cant_mem = random.randint(1,10) #Se genera una cantidad aleatoria de memoria a utilizar
    sienv.process(proceso(sienv, t_proceso, 'Proceso %d' % i, ram, cant_mem, cant_ins, inst_t))

# comienza la simulacion
sienv.run()
