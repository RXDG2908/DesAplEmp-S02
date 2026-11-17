// ==================================================================
// GUIA: ARCHIVO  main.jsx  (punto de entrada de React)
// LAB     : 09 Ej.3 (estructura del proyecto Vite)
// QUE HACE : monta <App /> dentro del <div id="root"> de ../index.html.
// CADENA  : ../index.html -> main.jsx -> ./App.jsx -> ./Vet.jsx (y los componentes de Lab 10)
// DOCS    : ../../docs/guiones/GUION-Lab09-Parte1.md
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
