import { z } from 'zod'
import { tiposDocumentos, valorMaximoNumeroDocumento, valorMinimoNumeroDocumento } from './constantesValidaciones.js'
// Validación para números de documento
const numeroDocumento = z
  .number()
  .int()
  .positive()
  .min(valorMinimoNumeroDocumento, { message: 'El número debe tener al menos 8 dígitos' })
  .max(valorMaximoNumeroDocumento, { message: 'El número no puede tener más de 10 dígitos' })

// Validación para texto (nombres)
const textoNombres = z
  .string()
  .min(1, { message: 'El nombre no puede estar vacío' })
  .refine((value) => !/\d/.test(value), {
    message: 'El texto no debe contener números'
  })

// Validación para la dirección de una imagen
const direccionImagen = z
  .string()
  .min(1, { message: 'La dirección de la imagen no puede estar vacía' })

const tipoDocumento = z
  .enum(tiposDocumentos)

const user = z.object(
  numeroDocumento,
  tipoDocumento,
  direccionImagen
)
export const validarRegistro = (value) => user.parseAsync(value)
export const validarNumeroDocumento = (value) => numeroDocumento.parseAsync(value)
export const validarTipoDocumento = (value) => tipoDocumento.parseAsync(value)
export const validarNombre = (value) => textoNombres.parseAsync(value)
