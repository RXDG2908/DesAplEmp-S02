// Datos escritos a mano con la forma de /api/insumos/ y /api/citas/ (Semana 8).

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
