// ==================================================================
// ARCHIVO  : main.jsx
// ROL      : PUNTO DE ENTRADA de React.
// ------------------------------------------------------------------
// LAB 9 - EJ 3: ESTRUCTURA del proyecto Vite -> MONTA <App /> dentro del
//               <div id="root"> de ../index.html.
// CADENA   : ../index.html -> main.jsx -> ./App.jsx -> ./Vet.jsx y los paneles
// NOTA     : <StrictMode> en desarrollo ejecuta los efectos DOS VECES (Lab 11 - EJ 8).
// ------------------------------------------------------------------
// DOCS     : ../../docs/guiones/GUION-Lab09-Parte1.md
// ==================================================================
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
