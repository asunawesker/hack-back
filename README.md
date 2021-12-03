# Track 3 - ¿Cómo agilizar la atención de los pacientes?

## #3 - HALCONES CON H

Backend hecho con **python, flask, google vision y mysql** para consumo de aplicación móvil y aplicación web.

Con este back buscamos reconocer el nombre en las identificaciones oficiales (INE), porteriormente, procesando este dato, se ocupa en un POST que sirve para que la aplicación móvil se comunique con el OCR de Google Vision, procese el texto y se almacene este dato en la base de datos que hemos creado al lado del código de color que muestra el tipo de urgencia que ha llegado. También se hizo la implementación de un GET para que la aplicación web pueda comunicarse con la base de datos y le muestre a los médicos los pacientes que hay en el área de urgencias y la prioridad que tienen.
