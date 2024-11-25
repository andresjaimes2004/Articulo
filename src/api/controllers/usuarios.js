import UserModel from '../models/sqlite/Usuarios.js'
import { validarRegistro, validarNumeroDocumento } from '../schema/validaciones.js'
import SearchDataUserForRegister from '../interface/scraping/SearchUser.js'
import SearchCriminalRecord from '../interface/scraping/antecedentes.js'
class UsuariosController {
  #Modelo
  constructor ({ Modelo }) {
    this.#Modelo = Modelo
  }

  getById = async (req, res) => {
    const id = req.params.id
    const NumeroDocumento = validarNumeroDocumento(id)
    const a = await UserModel.searchUserById({ NumeroDocumento })
    console.log(a)
  }

  getAll = async (_, res) => {
    const data = await UserModel.listUsers()
    console.log(data)
  }

  create = async (req, res) => {
    const result = await validarRegistro(req.params)
    if (result.sucess === false) {
      return res.status(400).json({ error: JSON.parse(result.error.message) })
    }
    const { numeroDocumento, tipoDocumento, direccionImagen } = result.data
    const antecedentes = await SearchCriminalRecord(numeroDocumento)
    const { nombres, apellidos, municipo, departamento } = await SearchDataUserForRegister(numeroDocumento)
    const user = { antecedentes, tipoDocumento, direccionImagen, nombres, apellidos, municipo, departamento }
    const datos = UserModel.insertUser(user)
    console.log(datos)
  }
}

export default UsuariosController
