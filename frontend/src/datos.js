// ==================================================================
// ARCHIVO  : datos.js
// PARTE 1  : VET (reserva de citas de la veterinaria)
// ROL      : DATOS ESCRITOS A MANO con la MISMA FORMA que la API del Lab 8
//            (/api/insumos/ y /api/citas/; los decimales como TEXTO).
// ------------------------------------------------------------------
// LAB 9 - EJ 5 : insumos -> ARREGLO de la entidad principal (lista con map y key).
// LAB 9 - EJ 7 : citas   -> relación 1:N (cada cita trae su arreglo de CONSUMOS).
// LAB 11 - EJ 10: citasPanel -> registros del PANEL DE CITAS (estado en PanelCitas).
// ------------------------------------------------------------------
// USADO EN : ./Vet.jsx y ./components/PanelCitas.jsx
// ==================================================================

export const insumos = [
  { id: 1, nombre: 'Jeringa 5ml', unidad: 'unidad', stock: 100 },
  { id: 2, nombre: 'Vacuna antirrabica', unidad: 'dosis', stock: 12 },
  { id: 3, nombre: 'Suero fisiologico', unidad: 'frasco', stock: 1 },
  { id: 4, nombre: 'Antiparasitario', unidad: 'tableta', stock: 0 },
  { id: 5, nombre: 'Gasa esteril', unidad: 'paquete', stock: 40 },
]

export const citas = [
  {
    id: 1, mascota: 'Firulais', dueno: 'Marta Quispe', servicio: 'Vacunacion',
    fecha: '2026-10-20', hora: '09:00', estado: 'Atendida',
    veterinario: { id: 1, nombre: 'Dra. Ana Torres', colegiatura: 'CMVP-1234', especialidad: 'Medicina general' },
    ficha: { peso_kg: '12.50', diagnostico: 'Sano', tratamiento: 'Vacuna antirrabica', proximo_control: '2027-10-20' },
    consumos: [
      { insumo: 'Jeringa 5ml', cantidad: 1, precio_unitario: '1.50', subtotal: '1.50' },
      { insumo: 'Vacuna antirrabica', cantidad: 1, precio_unitario: '25.00', subtotal: '25.00' },
    ],
  },
  {
    id: 2, mascota: 'Michi', dueno: 'Jorge Paredes', servicio: 'Consulta',
    fecha: '2026-11-05', hora: '10:30', estado: 'Confirmada',
    veterinario: { id: 2, nombre: 'Dr. Luis Gamarra', colegiatura: 'CMVP-5678', especialidad: 'Felinos' },
    ficha: null,
    consumos: [],
  },
  {
    id: 3, mascota: 'Rocky', dueno: 'Carla Rios', servicio: 'Cirugia',
    fecha: '2026-11-08', hora: '15:00', estado: 'Pendiente',
    veterinario: { id: 1, nombre: 'Dra. Ana Torres', colegiatura: 'CMVP-1234', especialidad: 'Medicina general' },
    ficha: null,
    consumos: [
      { insumo: 'Suero fisiologico', cantidad: 2, precio_unitario: '8.00', subtotal: '16.00' },
      { insumo: 'Gasa esteril', cantidad: 3, precio_unitario: '2.50', subtotal: '7.50' },
    ],
  },
  {
    id: 4, mascota: 'Luna', dueno: 'Pedro Soto', servicio: 'Consulta',
    fecha: '2026-11-12', hora: '11:15', estado: 'Pendiente',
    veterinario: { id: 2, nombre: 'Dr. Luis Gamarra', colegiatura: 'CMVP-5678', especialidad: 'Felinos' },
    ficha: null,
    consumos: [],
  },
]

// LAB 11 - EJ 10: CITAS del PANEL ADMINISTRATIVO, con la forma de la respuesta de /api/citas/.
export const citasPanel = [
  { id: 1, mascota: 'Firulais', dueno: 'Marta Quispe', servicio: 'Vacunacion', hora: '09:00', estado: 'Atendida' },
  { id: 2, mascota: 'Michi', dueno: 'Jorge Paredes', servicio: 'Consulta', hora: '10:30', estado: 'Confirmada' },
  { id: 3, mascota: 'Rocky', dueno: 'Carla Rios', servicio: 'Cirugia', hora: '15:00', estado: 'Pendiente' },
  { id: 4, mascota: 'Luna', dueno: 'Pedro Soto', servicio: 'Consulta', hora: '11:15', estado: 'Pendiente' },
  { id: 5, mascota: 'Toby', dueno: 'Rosa Medina', servicio: 'Vacunacion', hora: '16:30', estado: 'Confirmada' },
  { id: 6, mascota: 'Nala', dueno: 'Diego Salas', servicio: 'Consulta', hora: '08:45', estado: 'Pendiente' },
]
