import { Router } from 'express'
import UserController from '../controllers/usuarios.js'
const createRouterUsuarios = ({ Modelo }) => {
  const router = Router()
  const controler = UserController({ Modelo })
  router.get('/:id', controler.getById)
  router.get('/list', controler.getAll)
  router.post('/', controler.create)
  return Router
}
export default createRouterUsuarios
