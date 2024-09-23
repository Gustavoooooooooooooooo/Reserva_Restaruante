create database restaurante_reserva;
use restaurante_reserva;
create table mesa(
id_mesa int auto_increment primary key,
estado ENUM('libre', 'ocupado') NOT NULL,
reservador varchar(50),
cantidad_personas int,
fecha_reserva date,
ubicacion_mesa varchar(50)
);
