# Informe

## Intro

### Objetivos y metas

El problema original al que nos enfrentamos se basa en dar respuesta a la pregunta: ¿cuántos clientes se pierden en promedio cada día en el lavadero de coches dadas las condiciones planteadas? Algo que podemos solucionar de manera directa utilizando tanto modelos matemáticos como de simulación; pero que también da paso a otras interrogantes que enriquecen al grueso de nuestro proyecto como:

- ¿Cómo se comporta el sistema si los clientes se impacientan y abandonan la cola?
- ¿Será más eficiente el negocio si se tiene una cola con dos servidores, que dos colas por cada servidor?(Una pregunta que intuitivamente parece indicar que sí) ¿Qué sucederá si las colas se mantienen balanceadas?
- ¿Existe alguna relación entre las variables que se encuentran bajo análisis? ¿Y si es así, de qué tipo?
- ¿Qué comportamiento presentan dichas variables? ¿Siguen alguna distribución en particular?

Las respuestas a estás cuestiones constituyen los objetivos y metas de nuestro trabajo.

### Sistema específico. Variables de interés

El **sistema** tratado es un lavadero de autos, representado como un conjunto de máquinas de lavado (servidores) y un conjunto de coches.

Para **modelarlo** abstrajimos el sistema original como una lista de enteros (donde cada coche está representado por uno de estos) y variables booleanas (indican si alguno de los servidores se encuentra en funcionamiento o no). Encontramos este modelo suficiente, dado que contiene la información necesaria para dar respuesta a las interrogantes que enfrentamos, manteniendo solo los detalles indispensables.

Los **estados** del modelo están caracterizados por:

- Cantidad de coches en la cola
- Cantidad de coches siendo atendidos

Las **entidades** del modelo son:

- Coches
- Servidores (máquinas de lavado)

, cuyos **atributos** son:

- identificadores para los coches
- identificadores para los servidores
- estado de funcionamiento de los servidores

Los **eventos** principales del modelo son:

- Arribo de un nuevo coche
- Finalización de lavado de un coche
- Partida de un coche por impaciencia

#### Variables de interés

Para dar soluciones a las objetivos del proyecto tomamos como variables de interés:

- Tiempo de uso de los servidores
- Cantidad de coches perdidos
- Tiempo promedio de espera
- Tiempo inter-arribos promedio

### Variables que describen el problema 

<!-- Son las que están en el latex -->

## Detalles de Implementación

Para la implementación del proyecto nos basamos en el **Event Scheduling/Time Advance Algorithm** (presente en el libro Discrete Event Simulation de Jerry Banks), el cual lo llevamos al contexto de nuestro problema manteniendo una lista de eventos futuros (cuyos posibles tipos fueron comentados previamente) y avanzando el reloj (clock) de evento más inminente al siguiente, mientras las simulaciones son ejecutadas y los futuros eventos son generados.

Como pseudocódigo:

```pseudo
while clock < duration:
    pop imminent event
    advance clock

    if arrival event:
        generate arrival
        generate impatience
        simulate arrival
    
    if departure event:
        simulate departure

    if server available:
        generate departure
        simulate car serving
```